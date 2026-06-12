import os
from datetime import datetime
from decimal import Decimal
from pathlib import Path

# força ambiente DBMaker/ODBC antes do pyodbc conectar
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
from dotenv import load_dotenv
from sqlalchemy import text

from app.core.database import engine

load_dotenv()

DBMAKER_DSN = os.getenv("DBMAKER_DSN", "QLICKDB")
DBMAKER_USER = os.getenv("DBMAKER_USER", "SYSADM")
DBMAKER_PASSWORD = os.getenv("DBMAKER_PASSWORD", "")
DBMAKER_HOST = os.getenv("DBMAKER_HOST", "172.16.1.85")
DBMAKER_PORT = os.getenv("DBMAKER_PORT", "6525")
DBMAKER_NAME = os.getenv("DBMAKER_NAME", "QLICKDB")


QUERY_LOJAS = """
SELECT
    "BI040_DATACHAVE",
    "BI040_ATUALIZACAO",
    "BI040_META",
    "BI040_FATURAMENTO",
    "BI040_PROJECAO",
    "BI040_MARGEM",
    "BI040_PRECOMEDIO",
    "BI040_TICKETMEDIO",
    "BI040_METAALCANCADA",
    "BI040_FATUSEMBR",
    "BI040_MARGSEMBR",
    "BI040_PRECOMEDSEMBR",
    "BI040_VENDAAGORA",
    "BI040_VENDADIA",
    "BI040_MARGEMMEDIAANO",
    "BI040_JUROSMEDIOANO",
    "BI040_JUROS",
    "BI040_JUROAGORA"
FROM A_BI040
"""


QUERY_NATUROVOS = """
SELECT
    "BI037_DATACHAVE",
    "BI037_ATUALIZACAO",
    "BI037_META",
    "BI037_FATURAMENTO",
    "BI037_PROJECAO",
    "BI037_MARGEM",
    "BI037_PRECOMEDIO",
    "BI037_TICKETMEDIO",
    "BI037_METAALCANCADA",
    "BI037_FATUSEMBR",
    "BI037_MARGSEMBR",
    "BI037_PRECOMEDSEMBR",
    "BI037_VENDAAGORA"
FROM A_BI037
"""

QUERY_BI062 = """
SELECT
    "BI062_IDENTI",
    "BI062_ATUALIZACAO",
    "BI062_VLRVENCI",
    "BI062_REPVENCI",
    "BI062_VLRPERDA",
    "BI062_REPPERDA"
FROM A_BI062
"""

INSERT_SQL = text("""
    INSERT INTO fato_resumo_total (
        data_chave,
        data_referencia,
        departamento,
        departamento_nome,
        atualizacao,
        atualizacao_ts,
        meta,
        faturamento,
        projecao,
        margem,
        preco_medio,
        ticket_medio,
        meta_alcancada,
        faturamento_sem_br,
        margem_sem_br,
        preco_medio_sem_br,
        venda_agora,
        venda_dia,
        margem_media_ano,
        juros_medio_ano,
        juros,
        juros_agora,
        origem_tabela,
        valor_vencido,
        percentual_vencido,
        valor_perda,
        percentual_perda,
        created_at,
        updated_at
    )
    VALUES (
        :data_chave,
        :data_referencia,
        :departamento,
        :departamento_nome,
        :atualizacao,
        :atualizacao_ts,
        :meta,
        :faturamento,
        :projecao,
        :margem,
        :preco_medio,
        :ticket_medio,
        :meta_alcancada,
        :faturamento_sem_br,
        :margem_sem_br,
        :preco_medio_sem_br,
        :venda_agora,
        :venda_dia,
        :margem_media_ano,
        :juros_medio_ano,
        :juros,
        :juros_agora,
        :origem_tabela,
        :valor_vencido,
        :percentual_vencido,
        :valor_perda,
        :percentual_perda,
        now(),
        now()
    )
    ON CONFLICT (data_chave, departamento)
    DO UPDATE SET
        data_referencia = EXCLUDED.data_referencia,
        departamento_nome = EXCLUDED.departamento_nome,
        atualizacao = EXCLUDED.atualizacao,
        atualizacao_ts = EXCLUDED.atualizacao_ts,
        meta = EXCLUDED.meta,
        faturamento = EXCLUDED.faturamento,
        projecao = EXCLUDED.projecao,
        margem = EXCLUDED.margem,
        preco_medio = EXCLUDED.preco_medio,
        ticket_medio = EXCLUDED.ticket_medio,
        meta_alcancada = EXCLUDED.meta_alcancada,
        faturamento_sem_br = EXCLUDED.faturamento_sem_br,
        margem_sem_br = EXCLUDED.margem_sem_br,
        preco_medio_sem_br = EXCLUDED.preco_medio_sem_br,
        venda_agora = EXCLUDED.venda_agora,
        venda_dia = EXCLUDED.venda_dia,
        margem_media_ano = EXCLUDED.margem_media_ano,
        juros_medio_ano = EXCLUDED.juros_medio_ano,
        juros = EXCLUDED.juros,
        juros_agora = EXCLUDED.juros_agora,
        origem_tabela = EXCLUDED.origem_tabela,
        valor_vencido = EXCLUDED.valor_vencido,
        percentual_vencido = EXCLUDED.percentual_vencido,
        valor_perda = EXCLUDED.valor_perda,
        percentual_perda = EXCLUDED.percentual_perda,
        updated_at = now()
""")


def to_decimal(value):
    if value is None:
        return None

    if isinstance(value, Decimal):
        return value

    value = str(value).strip().replace(" ", "")

    if value == "" or value == "-":
        return None

    if "," in value and "." in value:
        if value.rfind(",") > value.rfind("."):
            value = value.replace(".", "").replace(",", ".")
        else:
            value = value.replace(",", "")
    elif "," in value:
        value = value.replace(",", ".")

    try:
        return Decimal(value)
    except Exception:
        return None


def parse_data_chave(value):
    if value is None:
        return None

    try:
        data_chave = int(value)
    except Exception:
        return None

    if data_chave <= 0:
        return None

    return data_chave


def parse_data_referencia(data_chave):
    if not data_chave:
        return None

    try:
        return datetime.strptime(str(data_chave), "%Y%m%d").date()
    except Exception:
        return None


def parse_atualizacao_ts(value):
    if value is None:
        return None

    if isinstance(value, datetime):
        return value

    value = str(value).strip()

    if value == "" or value == "-":
        return None

    for formato in ("%d/%m/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(value, formato)
        except Exception:
            pass

    return None


def get_value(row: dict, key: str):
    return row.get(key)


LOG_FILE = Path(os.getenv("IMPORT_RESUMO_TOTAL_LOG", "logs/import_resumo_total.log"))


def log(msg: str):
    linha = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"

    print(linha, flush=True)

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(linha + "\n")


def preparar_linha(row, prefixo, departamento, departamento_nome, origem_tabela):
    data_chave = parse_data_chave(get_value(row, f"{prefixo}_DATACHAVE"))
    data_referencia = parse_data_referencia(data_chave)

    if not data_chave or not data_referencia:
        return None

    atualizacao = get_value(row, f"{prefixo}_ATUALIZACAO")
    atualizacao = str(atualizacao).strip() if atualizacao is not None else None

    return {
        "data_chave": data_chave,
        "data_referencia": data_referencia,
        "departamento": departamento,
        "departamento_nome": departamento_nome,
        "atualizacao": atualizacao,
        "atualizacao_ts": parse_atualizacao_ts(atualizacao),
        "meta": to_decimal(get_value(row, f"{prefixo}_META")),
        "faturamento": to_decimal(get_value(row, f"{prefixo}_FATURAMENTO")),
        "projecao": to_decimal(get_value(row, f"{prefixo}_PROJECAO")),
        "margem": to_decimal(get_value(row, f"{prefixo}_MARGEM")),
        "preco_medio": to_decimal(get_value(row, f"{prefixo}_PRECOMEDIO")),
        "ticket_medio": to_decimal(get_value(row, f"{prefixo}_TICKETMEDIO")),
        "meta_alcancada": to_decimal(get_value(row, f"{prefixo}_METAALCANCADA")),
        "faturamento_sem_br": to_decimal(get_value(row, f"{prefixo}_FATUSEMBR")),
        "margem_sem_br": to_decimal(get_value(row, f"{prefixo}_MARGSEMBR")),
        "preco_medio_sem_br": to_decimal(get_value(row, f"{prefixo}_PRECOMEDSEMBR")),
        "venda_agora": to_decimal(get_value(row, f"{prefixo}_VENDAAGORA")),
        "venda_dia": to_decimal(get_value(row, f"{prefixo}_VENDADIA")),
        "margem_media_ano": to_decimal(get_value(row, f"{prefixo}_MARGEMMEDIAANO")),
        "juros_medio_ano": to_decimal(get_value(row, f"{prefixo}_JUROSMEDIOANO")),
        "juros": to_decimal(get_value(row, f"{prefixo}_JUROS")),
        # A_BI040 possui JUROAGORA.
        # A_BI037 aparentemente não possui, então ficará None.
        "juros_agora": to_decimal(get_value(row, f"{prefixo}_JUROAGORA")),
        "origem_tabela": origem_tabela,
        "valor_vencido": None,
        "percentual_vencido": None,
        "valor_perda": None,
        "percentual_perda": None,
    }


UPDATE_BI062_SQL = text("""
    UPDATE fato_resumo_total
    SET
        valor_vencido = :valor_vencido,
        percentual_vencido = :percentual_vencido,
        valor_perda = :valor_perda,
        percentual_perda = :percentual_perda,
        updated_at = now()
    WHERE departamento = :departamento
""")


def preparar_linha_bi062(row):
    identi = get_value(row, "BI062_IDENTI")

    if identi is None:
        return None

    try:
        departamento = int(identi)
    except Exception:
        return None

    return {
        "departamento": departamento,
        "valor_vencido": to_decimal(get_value(row, "BI062_VLRVENCI")),
        "percentual_vencido": to_decimal(get_value(row, "BI062_REPVENCI")),
        "valor_perda": to_decimal(get_value(row, "BI062_VLRPERDA")),
        "percentual_perda": to_decimal(get_value(row, "BI062_REPPERDA")),
    }


def importar_bi062(conn):
    log("Buscando dados: A_BI062")

    rows = buscar_dados_dbmaker(QUERY_BI062)
    log(f"Linhas encontradas: {len(rows)}")

    total_lidos = len(rows)
    total_importados = 0
    total_ignorados = 0

    for row in rows:
        dados = preparar_linha_bi062(row)

        if dados is None:
            total_ignorados += 1
            continue

        conn.execute(UPDATE_BI062_SQL, dados)
        total_importados += 1

    return total_lidos, total_importados, total_ignorados


def conectar_dbmaker():
    """
    Tenta primeiro o DSN configurado no ODBC. Se o container nao tiver o
    mesmo odbc.ini do host, usa uma string completa com host/porta/nome.
    """

    dsn_conn_str = f"DSN={DBMAKER_DSN};UID={DBMAKER_USER}"
    if DBMAKER_PASSWORD:
        dsn_conn_str += f";PWD={DBMAKER_PASSWORD}"

    try:

        return pyodbc.connect(dsn_conn_str, ansi=True, autocommit=True, timeout=30)

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

        return pyodbc.connect(conn_str, ansi=True, autocommit=True)


def buscar_dados_dbmaker(query):
    conn = conectar_dbmaker()
    conn.setdecoding(pyodbc.SQL_CHAR, encoding="latin1")
    conn.setdecoding(pyodbc.SQL_WCHAR, encoding="utf-16le")
    conn.setencoding(encoding="latin1")
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]

        rows = []
        for item in cursor.fetchall():
            rows.append(dict(zip(columns, item)))

        return rows

    finally:
        cursor.close()
        conn.close()


def limpar_registros_invalidos():
    sql = text("""
        DELETE FROM fato_resumo_total
        WHERE data_chave = 0
           OR data_referencia IS NULL
    """)

    with engine.begin() as conn:
        conn.execute(sql)


def importar_resumo_total():
    log("Iniciando importação fato_resumo_total...")
    limpar_registros_invalidos()

    total_lidos = 0
    total_importados = 0
    total_ignorados = 0

    cargas = [
        {
            "query": QUERY_LOJAS,
            "prefixo": "BI040",
            "departamento": 1,
            "departamento_nome": "lojas",
            "origem_tabela": "A_BI040",
        },
        {
            "query": QUERY_NATUROVOS,
            "prefixo": "BI037",
            "departamento": 5,
            "departamento_nome": "naturovos",
            "origem_tabela": "A_BI037",
        },
    ]

    with engine.begin() as conn:
        for carga in cargas:
            log(f"Buscando dados: {carga['origem_tabela']}")

            rows = buscar_dados_dbmaker(carga["query"])
            total_lidos += len(rows)

            log(f"Linhas encontradas: {len(rows)}")

            for row in rows:
                dados = preparar_linha(
                    row=row,
                    prefixo=carga["prefixo"],
                    departamento=carga["departamento"],
                    departamento_nome=carga["departamento_nome"],
                    origem_tabela=carga["origem_tabela"],
                )

                if dados is None:
                    total_ignorados += 1
                    continue

                conn.execute(INSERT_SQL, dados)
                total_importados += 1

        bi062_lidos, bi062_importados, bi062_ignorados = importar_bi062(conn)

        total_lidos += bi062_lidos
        total_importados += bi062_importados
        total_ignorados += bi062_ignorados

    log("Importação concluída.")
    log(f"Total lidos: {total_lidos}")
    log(f"Total importados/atualizados: {total_importados}")
    log(f"Total ignorados: {total_ignorados}")


if __name__ == "__main__":
    importar_resumo_total()
