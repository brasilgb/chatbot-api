from sqlalchemy import text
from app.core.database import SessionLocal


def buscar_faturamento_por_associacao(data_inicio, data_fim, departamento=None, limite=100):
    sql = """
        SELECT
            data_referencia,
            departamento,
            associacao,
            COALESCE(faturamento, 0) AS faturamento,
            COALESCE(rep_faturamento, 0) AS rep_faturamento,
            COALESCE(projecao, 0) AS projecao,
            COALESCE(margem, 0) AS margem,
            COALESCE(meta_alcancada, 0) AS meta_alcancada,
            COALESCE(preco_medio, 0) AS preco_medio,
            COALESCE(juros, 0) AS juros
        FROM fato_faturamento_associacao
        WHERE data_referencia = :data_fim
    """

    params = {
        "data_fim": data_fim,
        "limite": limite,
    }

    if departamento is not None:
        sql += " AND departamento = :departamento"
        params["departamento"] = departamento

    sql += """
        ORDER BY associacao
        LIMIT :limite
    """

    with SessionLocal() as db:
        result = db.execute(text(sql), params)
        return [dict(row._mapping) for row in result]


def buscar_faturamento_por_filial(data_inicio, data_fim, departamento=None, limite=100):
    sql = """
        SELECT
            data_referencia,
            departamento,
            id_filial,
            filial,
            COALESCE(faturamento, 0) AS faturamento,
            COALESCE(rep_faturamento, 0) AS rep_faturamento,
            COALESCE(projecao, 0) AS projecao,
            COALESCE(margem, 0) AS margem,
            COALESCE(meta_alcancada, 0) AS meta_alcancada,
            COALESCE(preco_medio, 0) AS preco_medio,
            COALESCE(juros, 0) AS juros
        FROM fato_faturamento_filial
        WHERE data_referencia = :data_fim
    """

    params = {
        "data_fim": data_fim,
        "limite": limite,
    }

    if departamento is not None:
        sql += " AND departamento = :departamento"
        params["departamento"] = departamento

    sql += """
        ORDER BY filial
        LIMIT :limite
    """

    with SessionLocal() as db:
        result = db.execute(text(sql), params)
        return [dict(row._mapping) for row in result]