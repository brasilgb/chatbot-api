from sqlalchemy import text
from app.core.database import engine


def get_faturamento_por_data(data: str):
    sql = text("""
        SELECT
            data_emissao,
            SUM(total_nota) AS total_faturamento,
            COUNT(DISTINCT departamento || '-' || filial_nota || '-' || serie_nota || '-' || numero_nota) AS total_notas
        FROM faturamento_loja
        WHERE data_emissao = :data
        GROUP BY data_emissao
    """)

    with engine.connect() as conn:
        result = conn.execute(sql, {"data": data}).mappings().first()

    return result


def get_faturamento_por_filial(data: str):
    sql = text("""
        SELECT
            filial_nota,
            SUM(total_nota) AS total_faturamento,
            COUNT(DISTINCT departamento || '-' || filial_nota || '-' || serie_nota || '-' || numero_nota) AS total_notas
        FROM faturamento_loja
        WHERE data_emissao = :data
        GROUP BY filial_nota
        ORDER BY total_faturamento DESC
    """)

    with engine.connect() as conn:
        result = conn.execute(sql, {"data": data}).mappings().all()

    return result


def get_faturamento_vendedores(data: str):
    sql = text("""
        SELECT
            codigo_vendedor,
            SUM(total_nota) AS total_faturamento,
            COUNT(DISTINCT departamento || '-' || filial_nota || '-' || serie_nota || '-' || numero_nota) AS total_notas
        FROM faturamento_loja
        WHERE data_emissao = :data
        GROUP BY codigo_vendedor
        ORDER BY total_faturamento DESC
    """)

    with engine.connect() as conn:
        result = conn.execute(sql, {"data": data}).mappings().all()

    return result


def get_faturamento_produtos(data: str):
    sql = text("""
        SELECT
            codigo_item,
            descricao_item,
            SUM(quantidade) AS quantidade_total,
            SUM(quantidade * valor_unitario) AS valor_total
        FROM faturamento_loja
        WHERE data_emissao = :data
        GROUP BY codigo_item, descricao_item
        ORDER BY quantidade_total DESC
    """)

    with engine.connect() as conn:
        result = conn.execute(sql, {"data": data}).mappings().all()

    return result


def get_resumo_por_periodo(inicio: str, fim: str):
    sql = text("""
        SELECT
            SUM(total_nota) AS total_faturamento,
            COUNT(DISTINCT departamento || '-' || filial_nota || '-' || serie_nota || '-' || numero_nota) AS total_notas
        FROM faturamento_loja
        WHERE data_emissao BETWEEN :inicio AND :fim
    """)

    with engine.connect() as conn:
        result = conn.execute(sql, {"inicio": inicio, "fim": fim}).mappings().first()

    return result


def get_filiais_por_periodo(inicio: str, fim: str):
    sql = text("""
        SELECT
            filial_nota,
            SUM(total_nota) AS total_faturamento,
            COUNT(DISTINCT departamento || '-' || filial_nota || '-' || serie_nota || '-' || numero_nota) AS total_notas
        FROM faturamento_loja
        WHERE data_emissao BETWEEN :inicio AND :fim
        GROUP BY filial_nota
        ORDER BY total_faturamento DESC
    """)

    with engine.connect() as conn:
        result = conn.execute(sql, {"inicio": inicio, "fim": fim}).mappings().all()

    return result


def get_vendedores_por_periodo(inicio: str, fim: str):
    sql = text("""
        SELECT
            codigo_vendedor,
            SUM(total_nota) AS total_faturamento,
            COUNT(DISTINCT departamento || '-' || filial_nota || '-' || serie_nota || '-' || numero_nota) AS total_notas
        FROM faturamento_loja
        WHERE data_emissao BETWEEN :inicio AND :fim
        GROUP BY codigo_vendedor
        ORDER BY total_faturamento DESC
    """)

    with engine.connect() as conn:
        result = conn.execute(sql, {"inicio": inicio, "fim": fim}).mappings().all()

    return result


def get_produtos_por_periodo(inicio: str, fim: str):
    sql = text("""
        SELECT
            codigo_item,
            descricao_item,
            SUM(quantidade) AS quantidade_total,
            SUM(quantidade * valor_unitario) AS valor_total
        FROM faturamento_loja
        WHERE data_emissao BETWEEN :inicio AND :fim
        GROUP BY codigo_item, descricao_item
        ORDER BY quantidade_total DESC
    """)

    with engine.connect() as conn:
        result = conn.execute(sql, {"inicio": inicio, "fim": fim}).mappings().all()

    return result
