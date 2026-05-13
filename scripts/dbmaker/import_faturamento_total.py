import os
import sys
import time
from contextlib import closing
from decimal import Decimal
from datetime import datetime

# força ambiente DBMaker/ODBC antes do pyodbc conectar
os.environ["ODBCINI"] = "/etc/odbc.ini"
os.environ["ODBCSYSINI"] = "/etc"
os.environ["DBMAKER"] = "/home/dbmaker/5.4"
os.environ["DM_HOME"] = "/home/dbmaker/5.4"
os.environ["LD_LIBRARY_PATH"] = "/home/dbmaker/5.4/lib/so:" + os.environ.get(
    "LD_LIBRARY_PATH", ""
)

import pyodbc
import psycopg
from dotenv import load_dotenv

load_dotenv()

DBMAKER_DSN = os.getenv("DBMAKER_DSN", "QLICKDB")
DBMAKER_USER = os.getenv("DBMAKER_USER", "SYSADM")
DBMAKER_PASSWORD = os.getenv("DBMAKER_PASSWORD", "")

DBMAKER_HOST = os.getenv("DBMAKER_HOST", "172.16.1.85")
DBMAKER_PORT = os.getenv("DBMAKER_PORT", "6525")
DBMAKER_NAME = os.getenv("DBMAKER_NAME", "QLICKDB")

DATABASE_URL = os.getenv("DATABASE_URL", "").replace(
    "postgresql+psycopg://", "postgresql://"
)


def parse_data_chave(valor):
    if not valor:
        return None

    valor = str(valor)

    return datetime.strptime(valor, "%Y%m%d").date()


def log(msg: str):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")


def validate_config():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL nao configurada.")

def parse_atualizacao(valor):
    if valor is None:
        return None

    return str(valor).strip()

def conectar_dbmaker():
    """
    1) tenta conexão igual ao isql: DSN + UID
    2) se falhar, tenta conexão completa informando DB_PTNUM
    """

    try:
        log("Tentando conectar DBMaker via DSN...")
        return pyodbc.connect(
            f"DSN={DBMAKER_DSN};UID={DBMAKER_USER}",
            autocommit=True,
        )
    except Exception as exc:
        log(f"Falha via DSN: {exc}")
        log("Tentando conectar DBMaker com string completa...")

        conn_str = (
            "DRIVER=DBMAKER;"
            f"database={DBMAKER_NAME};"
            f"Host={DBMAKER_HOST};"
            f"Port={DBMAKER_PORT};"
            f"DB_PTNUM={DBMAKER_PORT};"
            f"DB_SVADR={DBMAKER_HOST};"
            f"DB_NAME={DBMAKER_NAME};"
            f"UID={DBMAKER_USER}"
        )

        if DBMAKER_PASSWORD:
            conn_str += f";PWD={DBMAKER_PASSWORD}"

        return pyodbc.connect(conn_str, autocommit=True)


def to_decimal(valor):
    if valor is None:
        return None
    return Decimal(str(valor))


UPSERT_POSTGRES = """
INSERT INTO fato_faturamento_total (
    data_chave,
    data_referencia,
    departamento,
    departamento_nome,
    atualizacao,
    dia_atual,
    dia_anterior,
    faturamento_dia,
    margem_dia,
    faturamento_anterior,
    margem_anterior,
    faturamento_semana,
    margem_semana,
    faturamento_mes,
    margem_mes,
    representatividade_faturamento,
    representatividade_sem_faturamento,
    meta_mes,
    venda_mes,
    meta_parcial_mes,
    atingido_mes,
    percentual_faturamento_mes,
    meta_dia,
    venda_dia,
    percentual_meta_dia,
    juros_spm,
    juros_parcial_dia,
    percentual_juros_dia,
    preco_medio_kg,
    media_dia,
    origem_tabela,
    updated_at
)
VALUES (
    %(data_chave)s,
    %(data_referencia)s,
    %(departamento)s,
    %(departamento_nome)s,
    %(atualizacao)s,
    %(dia_atual)s,
    %(dia_anterior)s,
    %(faturamento_dia)s,
    %(margem_dia)s,
    %(faturamento_anterior)s,
    %(margem_anterior)s,
    %(faturamento_semana)s,
    %(margem_semana)s,
    %(faturamento_mes)s,
    %(margem_mes)s,
    %(representatividade_faturamento)s,
    %(representatividade_sem_faturamento)s,
    %(meta_mes)s,
    %(venda_mes)s,
    %(meta_parcial_mes)s,
    %(atingido_mes)s,
    %(percentual_faturamento_mes)s,
    %(meta_dia)s,
    %(venda_dia)s,
    %(percentual_meta_dia)s,
    %(juros_spm)s,
    %(juros_parcial_dia)s,
    %(percentual_juros_dia)s,
    %(preco_medio_kg)s,
    %(media_dia)s,
    %(origem_tabela)s,
    NOW()
)
ON CONFLICT (data_chave, departamento)
DO UPDATE SET
    data_referencia = EXCLUDED.data_referencia,
    departamento_nome = EXCLUDED.departamento_nome,
    atualizacao = EXCLUDED.atualizacao,
    dia_atual = EXCLUDED.dia_atual,
    dia_anterior = EXCLUDED.dia_anterior,
    faturamento_dia = EXCLUDED.faturamento_dia,
    margem_dia = EXCLUDED.margem_dia,
    faturamento_anterior = EXCLUDED.faturamento_anterior,
    margem_anterior = EXCLUDED.margem_anterior,
    faturamento_semana = EXCLUDED.faturamento_semana,
    margem_semana = EXCLUDED.margem_semana,
    faturamento_mes = EXCLUDED.faturamento_mes,
    margem_mes = EXCLUDED.margem_mes,
    representatividade_faturamento = EXCLUDED.representatividade_faturamento,
    representatividade_sem_faturamento = EXCLUDED.representatividade_sem_faturamento,
    meta_mes = EXCLUDED.meta_mes,
    venda_mes = EXCLUDED.venda_mes,
    meta_parcial_mes = EXCLUDED.meta_parcial_mes,
    atingido_mes = EXCLUDED.atingido_mes,
    percentual_faturamento_mes = EXCLUDED.percentual_faturamento_mes,
    meta_dia = EXCLUDED.meta_dia,
    venda_dia = EXCLUDED.venda_dia,
    percentual_meta_dia = EXCLUDED.percentual_meta_dia,
    juros_spm = EXCLUDED.juros_spm,
    juros_parcial_dia = EXCLUDED.juros_parcial_dia,
    percentual_juros_dia = EXCLUDED.percentual_juros_dia,
    preco_medio_kg = EXCLUDED.preco_medio_kg,
    media_dia = EXCLUDED.media_dia,
    origem_tabela = EXCLUDED.origem_tabela,
    updated_at = NOW()
"""


QUERY_LOJAS = """
SELECT
    BI007_DATACHAVE,
    BI007_ATUALIZACAO,
    BI007_DIAATUAL,
    BI007_DIAANTERIOR,
    BI007_FATUDIA,
    BI007_MARGEMDIA,
    BI007_FATUANTERIOR,
    BI007_MARGEMANTERIOR,
    BI007_FATUSEMANA,
    BI007_MARGEMSEMANA,
    BI007_FATUMES,
    BI007_MARGEMMES,
    BI007_REPFATU,
    BI007_REPSEMFATU,
    BI007_METAMES,
    BI007_VENDAMES,
    BI007_METAPARCMES,
    BI007_ATINGIDOMES,
    BI007_PERFATUALMES,
    BI007_METADIA,
    BI007_VENDADIA,
    BI007_PERFMETADIA,
    BI007_JUROSSPM,
    BI007_JURSPARCDIA,
    BI007_PERFJURDIA,
    BI007_MEDIADIA
FROM A_BI007
"""


QUERY_NATUROVOS = """
SELECT
    BI029_DATACHAVE,
    BI029_ATUALIZACAO,
    BI029_DIAATUAL,
    BI029_DIAVENDADIA,
    BI029_DIAMARGEMDIA,
    BI029_DIAVENDASEMANA,
    BI029_DIAMARGEMSEMANA,
    BI029_DIAVENDAMES,
    BI029_DIAMARGEMMES,
    BI029_DIAREPTOTAL,
    BI029_PMESFATURAMENTO,
    BI029_PMESMARGEM,
    BI029_PMESREPTOTAL,
    BI029_PMESPRECOMEDIOKG,
    BI029_PASSFATURAMENTO,
    BI029_PASSMARGEM,
    BI029_PASSREPTOTAL,
    BI029_PASSPRECOMEDIOKG,
    BI029_MEDIADIA
FROM A_BI029
"""


def importar_lojas(src, dst):
    log("Importando faturamento Lojas...")
    src.execute(QUERY_LOJAS)
    rows = src.fetchall()

    total = 0

    for r in rows:
        item = {
            "data_chave": r.BI007_DATACHAVE,
            "data_referencia": parse_data_chave(r.BI007_DATACHAVE),
            "departamento": 1,
            "departamento_nome": "lojas",
            "atualizacao": parse_atualizacao(r.BI007_ATUALIZACAO),
            "dia_atual": r.BI007_DIAATUAL,
            "dia_anterior": r.BI007_DIAANTERIOR,
            "faturamento_dia": to_decimal(r.BI007_FATUDIA),
            "margem_dia": to_decimal(r.BI007_MARGEMDIA),
            "faturamento_anterior": to_decimal(r.BI007_FATUANTERIOR),
            "margem_anterior": to_decimal(r.BI007_MARGEMANTERIOR),
            "faturamento_semana": to_decimal(r.BI007_FATUSEMANA),
            "margem_semana": to_decimal(r.BI007_MARGEMSEMANA),
            "faturamento_mes": to_decimal(r.BI007_FATUMES),
            "margem_mes": to_decimal(r.BI007_MARGEMMES),
            "representatividade_faturamento": to_decimal(r.BI007_REPFATU),
            "representatividade_sem_faturamento": to_decimal(r.BI007_REPSEMFATU),
            "meta_mes": to_decimal(r.BI007_METAMES),
            "venda_mes": to_decimal(r.BI007_VENDAMES),
            "meta_parcial_mes": to_decimal(r.BI007_METAPARCMES),
            "atingido_mes": to_decimal(r.BI007_ATINGIDOMES),
            "percentual_faturamento_mes": to_decimal(r.BI007_PERFATUALMES),
            "meta_dia": to_decimal(r.BI007_METADIA),
            "venda_dia": to_decimal(r.BI007_VENDADIA),
            "percentual_meta_dia": to_decimal(r.BI007_PERFMETADIA),
            "juros_spm": to_decimal(r.BI007_JUROSSPM),
            "juros_parcial_dia": to_decimal(r.BI007_JURSPARCDIA),
            "percentual_juros_dia": to_decimal(r.BI007_PERFJURDIA),
            "preco_medio_kg": None,
            "media_dia": to_decimal(r.BI007_MEDIADIA),
            "origem_tabela": "A_007",
        }

        dst.execute(UPSERT_POSTGRES, item)
        total += 1

    log(f"Lojas importado: {total} registro(s)")


def importar_naturovos(src, dst):
    log("Importando faturamento Naturovos...")
    src.execute(QUERY_NATUROVOS)
    rows = src.fetchall()

    total = 0

    for r in rows:
        item = {
            "data_chave": r.BI029_DATACHAVE,
            "data_referencia": parse_data_chave(r.BI029_DATACHAVE),
            "departamento": 5,
            "departamento_nome": "naturovos",
            "atualizacao": parse_atualizacao(r.BI029_ATUALIZACAO),
            "dia_atual": r.BI029_DIAATUAL,
            "dia_anterior": None,
            "faturamento_dia": to_decimal(r.BI029_DIAVENDADIA),
            "margem_dia": to_decimal(r.BI029_DIAMARGEMDIA),
            "faturamento_anterior": to_decimal(r.BI029_PASSFATURAMENTO),
            "margem_anterior": to_decimal(r.BI029_PASSMARGEM),
            "faturamento_semana": to_decimal(r.BI029_DIAVENDASEMANA),
            "margem_semana": to_decimal(r.BI029_DIAMARGEMSEMANA),
            "faturamento_mes": to_decimal(r.BI029_DIAVENDAMES),
            "margem_mes": to_decimal(r.BI029_DIAMARGEMMES),
            "representatividade_faturamento": to_decimal(r.BI029_DIAREPTOTAL),
            "representatividade_sem_faturamento": None,
            "meta_mes": None,
            "venda_mes": to_decimal(r.BI029_PMESFATURAMENTO),
            "meta_parcial_mes": None,
            "atingido_mes": None,
            "percentual_faturamento_mes": None,
            "meta_dia": None,
            "venda_dia": to_decimal(r.BI029_DIAVENDADIA),
            "percentual_meta_dia": None,
            "juros_spm": None,
            "juros_parcial_dia": None,
            "percentual_juros_dia": None,
            "preco_medio_kg": to_decimal(r.BI029_PMESPRECOMEDIOKG),
            "media_dia": to_decimal(r.BI029_MEDIADIA),
            "origem_tabela": "A_BI040",
        }

        dst.execute(UPSERT_POSTGRES, item)
        total += 1

    log(f"Naturovos importado: {total} registro(s)")


def main():
    inicio = time.time()
    validate_config()

    log("Iniciando importacao de fato_faturamento_total")
    log(f"DSN DBMaker: {DBMAKER_DSN}")

    with closing(conectar_dbmaker()) as dbmaker_conn, closing(
        psycopg.connect(DATABASE_URL)
    ) as pg_conn:
        with closing(dbmaker_conn.cursor()) as src, closing(pg_conn.cursor()) as dst:
            importar_lojas(src, dst)
            importar_naturovos(src, dst)

            pg_conn.commit()

    tempo = round(time.time() - inicio, 2)
    log(f"Importacao concluida com sucesso em {tempo}s")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        log(f"Falha na importacao: {exc}")
        sys.exit(1)
