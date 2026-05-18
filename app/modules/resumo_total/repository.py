from sqlalchemy import text
from app.core.database import engine


def aplicar_filtro_departamento(sql: str, params: dict, departamento: int | None):
    if departamento is None:
        return sql, params

    if departamento == 0:
        sql += " AND departamento IN (1, 5)"
        return sql, params

    sql += " AND departamento = :departamento"
    params["departamento"] = departamento

    return sql, params


def get_ultimo_resumo(departamento: int | None = None):
    if departamento == 0:
        sql_data = """
            SELECT MAX(data_referencia) AS data_referencia
            FROM fato_resumo_total
            WHERE departamento IN (1, 5)
        """

        with engine.connect() as conn:
            row_data = conn.execute(text(sql_data)).mappings().first()

        if not row_data or not row_data["data_referencia"]:
            return None

        lista = get_resumo_por_data(
            data=row_data["data_referencia"],
            departamento=0,
        )

        return lista[0] if lista else None

    sql = """
        SELECT *
        FROM fato_resumo_total
        WHERE 1=1
    """

    params = {}

    sql, params = aplicar_filtro_departamento(sql, params, departamento)

    sql += """
        ORDER BY data_referencia DESC, atualizacao DESC
        LIMIT 1
    """

    with engine.connect() as conn:
        row = conn.execute(text(sql), params).mappings().first()

    return dict(row) if row else None


def get_resumo_por_data(data: str, departamento: int | None = None):
    if departamento == 0:
        sql = """
            SELECT
                0 AS departamento,
                CAST(:data AS date) AS data_referencia,
                MAX(atualizacao) AS atualizacao,

                SUM(meta) AS meta,
                SUM(faturamento) AS faturamento,
                SUM(projecao) AS projecao,
                SUM(venda_agora) AS venda_agora,
                SUM(venda_dia) AS venda_dia,
                SUM(juros_agora) AS juros_agora,

                AVG(margem) AS margem,
                CASE 
                    WHEN SUM(meta) > 0 
                    THEN SUM(faturamento) / SUM(meta) * 100
                    ELSE 0
                END AS meta_alcancada
            FROM fato_resumo_total
            WHERE data_referencia = :data
            AND departamento IN (1, 5)
        """

        params = {"data": data}

        with engine.connect() as conn:
            row = conn.execute(text(sql), params).mappings().first()

        return [dict(row)] if row else []

    sql = """
        SELECT *
        FROM fato_resumo_total
        WHERE data_referencia = :data
    """

    params = {"data": data}

    sql, params = aplicar_filtro_departamento(sql, params, departamento)

    sql += """
        ORDER BY departamento
    """

    with engine.connect() as conn:
        rows = conn.execute(text(sql), params).mappings().all()

    return [dict(row) for row in rows]


def get_resumo_periodo(
    data_inicio: str,
    data_fim: str,
    departamento: int | None = None,
):
    sql = """
        SELECT
            CASE WHEN :departamento = 0 THEN 0 ELSE departamento END AS departamento,
            MIN(data_referencia) AS data_inicio,
            MAX(data_referencia) AS data_fim,

            SUM(meta) AS meta,
            SUM(faturamento) AS faturamento,
            SUM(venda_agora) AS venda_agora,
            SUM(venda_dia) AS venda_dia,
            SUM(juros_agora) AS juros_agora

        FROM fato_resumo_total
        WHERE data_referencia BETWEEN :data_inicio AND :data_fim
    """

    params = {
    "data_inicio": data_inicio,
    "data_fim": data_fim,
    "departamento": departamento or 0,
}

    sql, params = aplicar_filtro_departamento(sql, params, departamento)

    if departamento == 0:
        sql += """
        GROUP BY 1
        ORDER BY 1
    """
    else:
        sql += """
        GROUP BY departamento
        ORDER BY departamento
    """

    with engine.connect() as conn:
        rows = conn.execute(text(sql), params).mappings().all()

    return [dict(row) for row in rows]


def get_evolucao_faturamento(
    data_inicio: str,
    data_fim: str,
    departamento: int | None = None,
):
    if departamento == 0:
        sql = """
            SELECT
                data_referencia,
                0 AS departamento,
                SUM(faturamento) AS faturamento,
                SUM(meta) AS meta,
                SUM(projecao) AS projecao,
                AVG(margem) AS margem,
                CASE
                    WHEN SUM(meta) > 0
                    THEN SUM(faturamento) / SUM(meta) * 100
                    ELSE 0
                END AS meta_alcancada,
                SUM(venda_agora) AS venda_agora,
                SUM(venda_dia) AS venda_dia
            FROM fato_resumo_total
            WHERE data_referencia BETWEEN :data_inicio AND :data_fim
            AND departamento IN (1, 5)
            GROUP BY data_referencia
            ORDER BY data_referencia ASC
        """

        params = {
            "data_inicio": data_inicio,
            "data_fim": data_fim,
        }

        with engine.connect() as conn:
            rows = conn.execute(text(sql), params).mappings().all()

        return [dict(row) for row in rows]

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
    """

    params = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    sql, params = aplicar_filtro_departamento(sql, params, departamento)

    sql += """
        ORDER BY data_referencia ASC, departamento ASC
    """

    with engine.connect() as conn:
        rows = conn.execute(text(sql), params).mappings().all()

    return [dict(row) for row in rows]


def get_meta_vs_realizado(data: str, departamento: int | None = None):
    sql = """
        SELECT *
        FROM fato_resumo_total
        WHERE data_referencia = :data
    """

    params = {"data": data}

    sql, params = aplicar_filtro_departamento(sql, params, departamento)

    sql += """
        ORDER BY departamento
    """

    with engine.connect() as conn:
        rows = conn.execute(text(sql), params).mappings().all()

    return get_resumo_por_data(data=data, departamento=departamento)
