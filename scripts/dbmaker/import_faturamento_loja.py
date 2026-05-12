import os
import sys
import time
from contextlib import closing
from datetime import date, datetime

import pyodbc
import psycopg
from dotenv import load_dotenv

load_dotenv()

DBMAKER_DSN = os.getenv("DBMAKER_DSN", "GRUPOSOLARDB")
DBMAKER_USER = os.getenv("DBMAKER_USER", "SYSADM")
DBMAKER_PASSWORD = os.getenv("DBMAKER_PASSWORD", "")
IMPORT_YEAR = int(os.getenv("IMPORT_YEAR", "2026"))
IMPORT_DEPARTMENT = os.getenv("IMPORT_DEPARTMENT")
BATCH_SIZE = int(os.getenv("IMPORT_BATCH_SIZE", "1000"))

DATABASE_URL = os.getenv("DATABASE_URL", "").replace(
    "postgresql+psycopg://", "postgresql://"
)

QUERY_DBMAKER = f"""
SELECT 
    "1051datem", 
    "1051depto", 
    "1051orige", 
    "1051numnf", 
    "1051serie",
    "1051tipom",
    "0032descr",
    "1051vende",
    "1053codcl",
    "0172nomcl",
    "1051total",
    "4051itens",
    "0182descr",
    "4051quant",
    "4051unita",
    "4051unida",
    "4051cusre",
    "4051vldes",
    "4051vlicm",
    "4051vlpis",
    "4051vlcof"
FROM a_mnf105
INNER JOIN A_tab003 
    ON "0031ident" = 6 
    AND "0031codig" = "1051tipom"
INNER JOIN A_ITE405 
    ON "4051depto" = "1051depto" 
    AND "4051orige" = "1051orige" 
    AND "4051serie" = "1051serie" 
    AND "4051numnf" = "1051numnf"
INNER JOIN A_ITE018 
    ON "0181depto" = "1051depto" 
    AND "0181itens" = "4051itens"
INNER JOIN A_cli017 
    ON "0171CODCL" = FIX("1053CODCL" / 10)
WHERE 
    "1052anoem" = {IMPORT_YEAR}
    AND "0031letbi" = 'V'
"""

if IMPORT_DEPARTMENT:
    QUERY_DBMAKER += f'\n    AND "1051depto" = {int(IMPORT_DEPARTMENT)}'

INSERT_POSTGRES = """
INSERT INTO faturamento_loja (
    data_emissao,
    departamento,
    filial_nota,
    numero_nota,
    serie_nota,
    tipo_movimento,
    descricao_movimento,
    codigo_vendedor,
    codigo_cliente,
    nome_cliente,
    total_nota,
    codigo_item,
    descricao_item,
    quantidade,
    valor_unitario,
    unidade_medida,
    custo_real,
    valor_desconto,
    valor_icms,
    valor_pis,
    valor_cofins
)
VALUES (
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s
)
"""

DELETE_POSTGRES = """
DELETE FROM faturamento_loja
WHERE EXTRACT(YEAR FROM data_emissao) = %s
"""

if IMPORT_DEPARTMENT:
    DELETE_POSTGRES += " AND departamento = %s"


def log(msg: str):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")


def parse_dbmaker_date(value) -> date:
    data_str = str(value).zfill(8)
    return datetime.strptime(data_str, "%d%m%Y").date()


def validate_config():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL nao configurada.")

    if BATCH_SIZE <= 0:
        raise RuntimeError("IMPORT_BATCH_SIZE deve ser maior que zero.")


def main():
    inicio = time.time()
    validate_config()

    escopo = f"ano={IMPORT_YEAR}"
    if IMPORT_DEPARTMENT:
        escopo += f", departamento={IMPORT_DEPARTMENT}"

    log(f"Iniciando importacao de faturamento_loja ({escopo})")

    with closing(
        pyodbc.connect(f"DSN={DBMAKER_DSN};UID={DBMAKER_USER};PWD={DBMAKER_PASSWORD}")
    ) as dbmaker_conn, closing(psycopg.connect(DATABASE_URL)) as pg_conn:
        with closing(dbmaker_conn.cursor()) as src, closing(pg_conn.cursor()) as dst:
            src.execute(QUERY_DBMAKER)

            delete_params = [IMPORT_YEAR]
            if IMPORT_DEPARTMENT:
                delete_params.append(int(IMPORT_DEPARTMENT))

            dst.execute(DELETE_POSTGRES, delete_params)
            removidos = dst.rowcount
            log(f"Registros antigos removidos no PostgreSQL: {removidos:,}")

            total = 0

            while True:
                rows = src.fetchmany(BATCH_SIZE)
                if not rows:
                    break

                batch = []

                for row in rows:
                    row = list(row)
                    row[0] = parse_dbmaker_date(row[0])
                    batch.append(tuple(row))

                dst.executemany(INSERT_POSTGRES, batch)
                total += len(batch)

                if total % BATCH_SIZE == 0:
                    log(f"{total:,} registros processados")

            pg_conn.commit()

    tempo = round(time.time() - inicio, 2)

    log(f"Importacao concluida com sucesso: {total:,} registros em {tempo}s")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        log(f"Falha na importacao: {exc}")
        sys.exit(1)
