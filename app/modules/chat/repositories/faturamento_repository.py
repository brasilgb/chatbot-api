from sqlalchemy import text

from app.core.database import engine


def buscar_faturamento_filiais(
    data_inicio: str,
    data_fim: str,
    departamento: int | None = None,
):
    params = {
        "data_referencia": data_fim,
        "departamento": departamento,
    }

    sql = text("""
        SELECT
            id_filial,
            filial,
            faturamento,
            rep_faturamento,
            projecao,
            margem,
            meta_alcancada,
            preco_medio,
            juros
        FROM fato_faturamento_filial
        WHERE data_referencia = :data_referencia
          AND departamento = :departamento
        ORDER BY faturamento DESC
    """)

    with engine.connect() as conn:
        result = conn.execute(sql, params)
        return [dict(row._mapping) for row in result]


def buscar_faturamento_associacoes(
    data_inicio: str,
    data_fim: str,
    departamento: int | None = None,
):
    params = {
        "data_referencia": data_fim,
        "departamento": departamento,
    }

    sql = text("""
        SELECT
            associacao,
            faturamento,
            rep_faturamento,
            projecao,
            margem,
            meta_alcancada,
            preco_medio,
            juros
        FROM fato_faturamento_associacao
        WHERE data_referencia = :data_referencia
          AND departamento = :departamento
        ORDER BY faturamento DESC
    """)

    with engine.connect() as conn:
        result = conn.execute(sql, params)
        return [dict(row._mapping) for row in result]

def buscar_resumo_departamento(
    data_inicio: str,
    data_fim: str,
    departamento: int | None = None,
):
    params = {
        "data_referencia": data_fim,
        "departamento": departamento,
    }

    sql = text("""
        SELECT
            departamento,
            departamento_nome,
            meta,
            faturamento,
            projecao,
            margem,
            meta_alcancada,
            preco_medio,
            venda_agora,
            venda_dia,
            juros_agora
        FROM fato_resumo_total
        WHERE data_referencia = :data_referencia
          AND departamento = :departamento
        LIMIT 1
    """)

    with engine.connect() as conn:
        result = conn.execute(sql, params)
        row = result.fetchone()
        return dict(row._mapping) if row else None