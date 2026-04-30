import os
import pyodbc
import psycopg
from dotenv import load_dotenv

load_dotenv()

DBMAKER_DSN = os.getenv("DBMAKER_DSN", "GRUPOSOLARDB")
DBMAKER_USER = os.getenv("DBMAKER_USER", "usuario")
DBMAKER_PASSWORD = os.getenv("DBMAKER_PASSWORD", "senha")

DATABASE_URL = os.getenv("DATABASE_URL")


QUERY_DBMAKER = """
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
    "1052anoem" = 2026 
    AND "0031letbi" = 'V'
"""


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


def main():
    print("Conectando ao DBMaker...")

    dbmaker_conn = pyodbc.connect(
        f"DSN={DBMAKER_DSN};UID={DBMAKER_USER};PWD={DBMAKER_PASSWORD}"
    )

    print("Conectando ao PostgreSQL...")

    pg_conn = psycopg.connect(DATABASE_URL)

    src = dbmaker_conn.cursor()
    dst = pg_conn.cursor()

    print("Executando query no DBMaker...")
    src.execute(QUERY_DBMAKER)

    total = 0

    print("Importando dados para faturamento_loja...")

    for row in src.fetchall():
        dst.execute(INSERT_POSTGRES, tuple(row))
        total += 1

        if total % 1000 == 0:
            pg_conn.commit()
            print(f"{total} registros importados...")

    pg_conn.commit()

    src.close()
    dst.close()
    dbmaker_conn.close()
    pg_conn.close()

    print(f"Importação concluída. Total: {total} registros.")


if __name__ == "__main__":
    main()