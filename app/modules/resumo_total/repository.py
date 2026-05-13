from sqlalchemy import text
from app.core.database import engine


def get_ultimo_resumo(departamento: int | None = None):
    sql = """
        SELECT *
        FROM fato_resumo_total
        WHERE (:departamento IS NULL OR departamento = :departamento)
        ORDER BY data_referencia DESC, atualizacao DESC
        LIMIT 1
    """

    with engine.connect() as conn:
        row = conn.execute(
            text(sql),
            {"departamento": departamento},
        ).mappings().first()

    return dict(row) if row else None


def get_resumo_por_data(data: str, departamento: int | None = None):
    sql = """
        SELECT *
        FROM fato_resumo_total
        WHERE data_referencia = :data
          AND (:departamento IS NULL OR departamento = :departamento)
        ORDER BY departamento
    """

    with engine.connect() as conn:
        rows = conn.execute(
            text(sql),
            {
                "data": data,
                "departamento": departamento,
            },
        ).mappings().all()

    return [dict(row) for row in rows]


def get_resumo_periodo(
    data_inicio: str,
    data_fim: str,
    departamento: int | None = None,
):
    sql = """
        SELECT
            departamento,
            MIN(data_referencia) AS data_inicio,
            MAX(data_referencia) AS data_fim,

            SUM(meta) AS meta,
            SUM(faturamento) AS faturamento,
            SUM(faturamento_sem_brasil) AS faturamento_sem_brasil,
            SUM(venda_agora) AS venda_agora,
            SUM(venda_dia) AS venda_dia,
            SUM(juro_agora) AS juro_agora

        FROM fato_resumo_total
        WHERE data_referencia BETWEEN :data_inicio AND :data_fim
          AND (:departamento IS NULL OR departamento = :departamento)
        GROUP BY departamento
        ORDER BY departamento
    """

    with engine.connect() as conn:
        rows = conn.execute(
            text(sql),
            {
                "data_inicio": data_inicio,
                "data_fim": data_fim,
                "departamento": departamento,
            },
        ).mappings().all()

    return [dict(row) for row in rows]


def get_evolucao_faturamento(
    data_inicio: str,
    data_fim: str,
    departamento: int | None = None,
):
    sql = """
        SELECT
            data_referencia,
            departamento,
            faturamento,
            meta,
            projecao,
            margem,
            meta_alcancada,
            venda_agora,
            venda_dia
        FROM fato_resumo_total
        WHERE data_referencia BETWEEN :data_inicio AND :data_fim
          AND (:departamento IS NULL OR departamento = :departamento)
        ORDER BY data_referencia ASC, departamento ASC
    """

    with engine.connect() as conn:
        rows = conn.execute(
            text(sql),
            {
                "data_inicio": data_inicio,
                "data_fim": data_fim,
                "departamento": departamento,
            },
        ).mappings().all()

    return [dict(row) for row in rows]


def get_meta_vs_realizado(
    data: str,
    departamento: int | None = None,
):
    sql = """
        SELECT
            data_referencia,
            departamento,
            meta,
            faturamento,
            projecao,
            meta_alcancada
        FROM fato_resumo_total
        WHERE data_referencia = :data
          AND (:departamento IS NULL OR departamento = :departamento)
        ORDER BY departamento
    """

    with engine.connect() as conn:
        rows = conn.execute(
            text(sql),
            {
                "data": data,
                "departamento": departamento,
            },
        ).mappings().all()

    return [dict(row) for row in rows]