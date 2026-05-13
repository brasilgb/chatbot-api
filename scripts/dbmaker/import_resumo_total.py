import os
from datetime import datetime
from decimal import Decimal

# força ambiente DBMaker/ODBC antes do pyodbc conectar
os.environ["ODBCINI"] = "/etc/odbc.ini"
os.environ["ODBCSYSINI"] = "/etc"
os.environ["DBMAKER"] = "/home/dbmaker/5.4"
os.environ["DM_HOME"] = "/home/dbmaker/5.4"
os.environ["LD_LIBRARY_PATH"] = "/home/dbmaker/5.4/lib/so:" + os.environ.get(
    "LD_LIBRARY_PATH", ""
)

import pyodbc
from sqlalchemy import text

from app.core.database import engine

DSN = os.getenv("DBMAKER_DSN", "QLICKDB")


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
        updated_at = now()
""")


def to_decimal(value):
    if value is None:
        return None

    value = str(value).strip()

    if value == "" or value == "-":
        return None

    try:
        return Decimal(value.replace(",", "."))
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

    value = str(value).strip()

    if value == "" or value == "-":
        return None

    try:
        return datetime.strptime(value, "%d/%m/%Y %H:%M:%S")
    except Exception:
        return None


def get_value(row: dict, key: str):
    return row.get(key)


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
    }


def buscar_dados_dbmaker(query):
    conn = pyodbc.connect(f"DSN={DSN}")
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
    print("Iniciando importação fato_resumo_total...")
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
            print(f"Buscando dados: {carga['origem_tabela']}")

            rows = buscar_dados_dbmaker(carga["query"])
            total_lidos += len(rows)

            print(f"Linhas encontradas: {len(rows)}")

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

    print("Importação concluída.")
    print(f"Total lidos: {total_lidos}")
    print(f"Total importados/atualizados: {total_importados}")
    print(f"Total ignorados: {total_ignorados}")


if __name__ == "__main__":
    importar_resumo_total()
