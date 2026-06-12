import os
import sys
import time
from contextlib import closing
from decimal import Decimal
from datetime import datetime

os.environ["ODBCINI"] = "/etc/odbc.ini"
os.environ["ODBCSYSINI"] = "/etc"
os.environ["DBMAKER"] = "/home/dbmaker/5.4"
os.environ["DM_HOME"] = "/home/dbmaker/5.4"
os.environ["DB_CLILCODE"] = "1"
os.environ["DB_CLIOCODE"] = "1"
os.environ["DB_LCODE"] = "1"
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

LOG_FILE = "/app/logs/import_faturamento_detalhado.log"


def log(msg: str):
    linha = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(linha, flush=True)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(linha + "\n")


def validate_config():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL nao configurada.")


def parse_data_chave(valor):
    if valor is None:
        return None

    texto = str(valor).strip()

    if texto in ("", "0", "00000000"):
        return None

    texto = texto.zfill(8)

    try:
        return datetime.strptime(texto, "%Y%m%d").date()
    except ValueError:
        return None


def parse_texto(valor):
    if valor is None:
        return None

    return str(valor).strip()


def to_int(valor):
    if valor is None:
        return None

    texto = str(valor).strip()

    if texto == "":
        return None

    try:
        return int(texto)
    except ValueError:
        return None


def to_decimal(valor):
    if valor is None:
        return None

    texto = str(valor).strip()

    if texto == "":
        return None

    return Decimal(texto)


def conectar_dbmaker():
    try:
        log("Tentando conectar DBMaker via DSN...")
        return pyodbc.connect(
            f"DSN={DBMAKER_DSN};UID={DBMAKER_USER}",
            autocommit=True,
        )
    except Exception as exc:
        log(f"Falha via DSN: {repr(exc)}")
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


QUERY_ASSOCIACAO_LOJAS = """
SELECT
    BI038_DATACHAVE,
    BI038_DEPARTAMENTO,
    BI038_ASSOCIACAO,
    BI038_ATUALIZACAO,
    BI038_FATURAMENTO,
    BI038_REPFATURAMENTO,
    BI038_PROJECAO,
    BI038_MARGEM,
    BI038_PRECOMEDIO,
    BI038_TICKETMEDIO,
    BI038_METAALCANCADA,
    BI038_JUROS
FROM A_BI038
"""

QUERY_FILIAL_LOJAS = """
SELECT
    BI039_DATACHAVE,
    BI039_DEPARTAMENTO,
    BI039_IDFILIAL,
    BI039_ATUALIZACAO,
    BI039_FILIAL,
    BI039_FATURAMENTO,
    BI039_REPFATURAMENTO,
    BI039_PROJECAO,
    BI039_MARGEM,
    BI039_PRECOMEDIO,
    BI039_TICKETMEDIO,
    BI039_METAALCANCADA,
    BI039_JUROS
FROM A_BI039
"""

QUERY_ASSOCIACAO_NATUROVOS = """
SELECT
    BI036_DATACHAVE,
    BI036_DEPARTAMENTO,
    BI036_ASSOCIACAO,
    BI036_ATUALIZACAO,
    BI036_FATURAMENTO,
    BI036_REPFATURAMENTO,
    BI036_PROJECAO,
    BI036_MARGEM,
    BI036_PRECOMEDIO,
    BI036_TICKETMEDIO,
    BI036_METAALCANCADA
FROM A_BI036
"""

QUERY_FILIAL_NATUROVOS = """
SELECT
    BI035_DATACHAVE,
    BI035_DEPARTAMENTO,
    BI035_IDFILIAL,
    BI035_ATUALIZACAO,
    BI035_FILIAL,
    BI035_FATURAMENTO,
    BI035_REPFATURAMENTO,
    BI035_PROJECAO,
    BI035_MARGEM,
    BI035_PRECOMEDIO,
    BI035_TICKETMEDIO,
    BI035_METAALCANCADA
FROM A_BI035
"""


UPSERT_ASSOCIACAO = """
INSERT INTO fato_faturamento_associacao (
    data_chave,
    data_referencia,
    departamento,
    associacao,
    atualizacao,
    faturamento,
    rep_faturamento,
    projecao,
    margem,
    preco_medio,
    ticket_medio,
    meta_alcancada,
    juros,
    updated_at
)
VALUES (
    %(data_chave)s,
    %(data_referencia)s,
    %(departamento)s,
    %(associacao)s,
    %(atualizacao)s,
    %(faturamento)s,
    %(rep_faturamento)s,
    %(projecao)s,
    %(margem)s,
    %(preco_medio)s,
    %(ticket_medio)s,
    %(meta_alcancada)s,
    %(juros)s,
    NOW()
)
ON CONFLICT (data_chave, departamento, associacao)
DO UPDATE SET
    data_referencia = EXCLUDED.data_referencia,
    atualizacao = EXCLUDED.atualizacao,
    faturamento = EXCLUDED.faturamento,
    rep_faturamento = EXCLUDED.rep_faturamento,
    projecao = EXCLUDED.projecao,
    margem = EXCLUDED.margem,
    preco_medio = EXCLUDED.preco_medio,
    ticket_medio = EXCLUDED.ticket_medio,
    meta_alcancada = EXCLUDED.meta_alcancada,
    juros = EXCLUDED.juros,
    updated_at = NOW()
"""

UPSERT_FILIAL = """
INSERT INTO fato_faturamento_filial (
    data_chave,
    data_referencia,
    departamento,
    id_filial,
    atualizacao,
    filial,
    faturamento,
    rep_faturamento,
    projecao,
    margem,
    preco_medio,
    ticket_medio,
    meta_alcancada,
    juros,
    updated_at
)
VALUES (
    %(data_chave)s,
    %(data_referencia)s,
    %(departamento)s,
    %(id_filial)s,
    %(atualizacao)s,
    %(filial)s,
    %(faturamento)s,
    %(rep_faturamento)s,
    %(projecao)s,
    %(margem)s,
    %(preco_medio)s,
    %(ticket_medio)s,
    %(meta_alcancada)s,
    %(juros)s,
    NOW()
)
ON CONFLICT (data_chave, departamento, id_filial)
DO UPDATE SET
    data_referencia = EXCLUDED.data_referencia,
    atualizacao = EXCLUDED.atualizacao,
    filial = EXCLUDED.filial,
    faturamento = EXCLUDED.faturamento,
    rep_faturamento = EXCLUDED.rep_faturamento,
    projecao = EXCLUDED.projecao,
    margem = EXCLUDED.margem,
    preco_medio = EXCLUDED.preco_medio,
    ticket_medio = EXCLUDED.ticket_medio,
    meta_alcancada = EXCLUDED.meta_alcancada,
    juros = EXCLUDED.juros,
    updated_at = NOW()
"""


def importar_associacao_lojas(src, dst):
    log("Importando faturamento por associacao Lojas...")

    src.execute(QUERY_ASSOCIACAO_LOJAS)
    rows = src.fetchall()

    total = 0
    ignorados = 0

    for r in rows:
        item = {
            "data_chave": to_int(r.BI038_DATACHAVE),
            "data_referencia": parse_data_chave(r.BI038_DATACHAVE),
            "departamento": to_int(r.BI038_DEPARTAMENTO) or 1,
            "associacao": parse_texto(r.BI038_ASSOCIACAO),
            "atualizacao": parse_texto(r.BI038_ATUALIZACAO),
            "faturamento": to_decimal(r.BI038_FATURAMENTO),
            "rep_faturamento": to_decimal(r.BI038_REPFATURAMENTO),
            "projecao": to_decimal(r.BI038_PROJECAO),
            "margem": to_decimal(r.BI038_MARGEM),
            "preco_medio": to_decimal(r.BI038_PRECOMEDIO),
            "ticket_medio": to_decimal(r.BI038_TICKETMEDIO),
            "meta_alcancada": to_decimal(r.BI038_METAALCANCADA),
            "juros": to_decimal(r.BI038_JUROS),
        }

        if (
            item["data_chave"] is None
            or item["data_referencia"] is None
            or item["departamento"] is None
            or item["associacao"] is None
        ):
            ignorados += 1
            continue

        dst.execute(UPSERT_ASSOCIACAO, item)
        total += 1

    log(f"Associacao Lojas importada: {total} registro(s), ignorados: {ignorados}")


def importar_filial_lojas(src, dst):
    log("Importando faturamento por filial Lojas...")

    src.execute(QUERY_FILIAL_LOJAS)
    rows = src.fetchall()

    total = 0
    ignorados = 0

    for r in rows:
        item = {
            "data_chave": to_int(r.BI039_DATACHAVE),
            "data_referencia": parse_data_chave(r.BI039_DATACHAVE),
            "departamento": to_int(r.BI039_DEPARTAMENTO) or 1,
            "id_filial": to_int(r.BI039_IDFILIAL),
            "atualizacao": parse_texto(r.BI039_ATUALIZACAO),
            "filial": parse_texto(r.BI039_FILIAL),
            "faturamento": to_decimal(r.BI039_FATURAMENTO),
            "rep_faturamento": to_decimal(r.BI039_REPFATURAMENTO),
            "projecao": to_decimal(r.BI039_PROJECAO),
            "margem": to_decimal(r.BI039_MARGEM),
            "preco_medio": to_decimal(r.BI039_PRECOMEDIO),
            "ticket_medio": to_decimal(r.BI039_TICKETMEDIO),
            "meta_alcancada": to_decimal(r.BI039_METAALCANCADA),
            "juros": to_decimal(r.BI039_JUROS),
        }

        if (
            item["data_chave"] is None
            or item["data_referencia"] is None
            or item["departamento"] is None
            or item["id_filial"] is None
        ):
            ignorados += 1
            continue

        dst.execute(UPSERT_FILIAL, item)
        total += 1

    log(f"Filial Lojas importada: {total} registro(s), ignorados: {ignorados}")


def importar_associacao_naturovos(src, dst):
    log("Importando faturamento por associacao Naturovos...")

    src.execute(QUERY_ASSOCIACAO_NATUROVOS)
    rows = src.fetchall()

    total = 0
    ignorados = 0

    for r in rows:
        item = {
            "data_chave": to_int(r.BI036_DATACHAVE),
            "data_referencia": parse_data_chave(r.BI036_DATACHAVE),
            "departamento": to_int(r.BI036_DEPARTAMENTO) or 5,
            "associacao": parse_texto(r.BI036_ASSOCIACAO),
            "atualizacao": parse_texto(r.BI036_ATUALIZACAO),
            "faturamento": to_decimal(r.BI036_FATURAMENTO),
            "rep_faturamento": to_decimal(r.BI036_REPFATURAMENTO),
            "projecao": to_decimal(r.BI036_PROJECAO),
            "margem": to_decimal(r.BI036_MARGEM),
            "preco_medio": to_decimal(r.BI036_PRECOMEDIO),
            "ticket_medio": to_decimal(r.BI036_TICKETMEDIO),
            "meta_alcancada": to_decimal(r.BI036_METAALCANCADA),
            "juros": None,
        }

        if (
            item["data_chave"] is None
            or item["data_referencia"] is None
            or item["departamento"] is None
            or item["associacao"] is None
        ):
            ignorados += 1
            continue

        dst.execute(UPSERT_ASSOCIACAO, item)
        total += 1

    log(f"Associacao Naturovos importada: {total} registro(s), ignorados: {ignorados}")


def importar_filial_naturovos(src, dst):
    log("Importando faturamento por filial Naturovos...")

    src.execute(QUERY_FILIAL_NATUROVOS)
    rows = src.fetchall()

    total = 0
    ignorados = 0

    for r in rows:
        item = {
            "data_chave": to_int(r.BI035_DATACHAVE),
            "data_referencia": parse_data_chave(r.BI035_DATACHAVE),
            "departamento": to_int(r.BI035_DEPARTAMENTO) or 5,
            "id_filial": to_int(r.BI035_IDFILIAL),
            "atualizacao": parse_texto(r.BI035_ATUALIZACAO),
            "filial": parse_texto(r.BI035_FILIAL),
            "faturamento": to_decimal(r.BI035_FATURAMENTO),
            "rep_faturamento": to_decimal(r.BI035_REPFATURAMENTO),
            "projecao": to_decimal(r.BI035_PROJECAO),
            "margem": to_decimal(r.BI035_MARGEM),
            "preco_medio": to_decimal(r.BI035_PRECOMEDIO),
            "ticket_medio": to_decimal(r.BI035_TICKETMEDIO),
            "meta_alcancada": to_decimal(r.BI035_METAALCANCADA),
            "juros": None,
        }

        if (
            item["data_chave"] is None
            or item["data_referencia"] is None
            or item["departamento"] is None
            or item["id_filial"] is None
        ):
            ignorados += 1
            continue

        dst.execute(UPSERT_FILIAL, item)
        total += 1

    log(f"Filial Naturovos importada: {total} registro(s), ignorados: {ignorados}")


def main():
    inicio = time.time()
    validate_config()

    log("Iniciando importacao de faturamento detalhado")
    log(f"DSN DBMaker: {DBMAKER_DSN}")

    with closing(conectar_dbmaker()) as dbmaker_conn, closing(
        psycopg.connect(DATABASE_URL)
    ) as pg_conn:
        with closing(dbmaker_conn.cursor()) as src, closing(pg_conn.cursor()) as dst:
            importar_associacao_lojas(src, dst)
            importar_filial_lojas(src, dst)
            importar_associacao_naturovos(src, dst)
            importar_filial_naturovos(src, dst)

            pg_conn.commit()

    tempo = round(time.time() - inicio, 2)
    log(f"Importacao concluida com sucesso em {tempo}s")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        log(f"Falha na importacao: {repr(exc)}")
        sys.exit(1)