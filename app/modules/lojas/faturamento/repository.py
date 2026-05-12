from sqlalchemy import text
from app.core.database import engine


def get_faturamento_por_data(data: str, departamento: int | None = None):
    sql = text("""
        WITH notas AS (
            SELECT DISTINCT
                departamento,
                filial_nota,
                serie_nota,
                numero_nota,
                total_nota
            FROM faturamento_loja
            WHERE data_emissao = CAST(:data AS date)
              AND departamento = :departamento
        )
        SELECT
            CAST(:data AS date) AS data_emissao,
            COALESCE(SUM(total_nota), 0) AS total_faturamento,
            COUNT(*) AS total_notas
        FROM notas
    """)

    with engine.connect() as conn:
        return (
            conn.execute(
                sql,
                {"data": data, "departamento": departamento},
            )
            .mappings()
            .first()
        )


def get_faturamento_por_filial(data: str, departamento: int | None = None):
    sql = text("""
        WITH notas AS (
            SELECT DISTINCT
                departamento,
                filial_nota,
                serie_nota,
                numero_nota,
                total_nota
            FROM faturamento_loja
            WHERE data_emissao = CAST(:data AS date)
              AND departamento = :departamento
        )
        SELECT
            filial_nota,
            COALESCE(SUM(total_nota), 0) AS total_faturamento,
            COUNT(*) AS total_notas
        FROM notas
        GROUP BY filial_nota
        ORDER BY total_faturamento DESC
    """)

    with engine.connect() as conn:
        return (
            conn.execute(
                sql,
                {"data": data, "departamento": departamento},
            )
            .mappings()
            .all()
        )


def get_faturamento_vendedores(data: str, departamento: int | None = None):
    sql = text("""
        WITH notas AS (
            SELECT DISTINCT
                departamento,
                filial_nota,
                serie_nota,
                numero_nota,
                codigo_vendedor,
                total_nota
            FROM faturamento_loja
            WHERE data_emissao = CAST(:data AS date)
              AND departamento = :departamento
        )
        SELECT
            codigo_vendedor,
            COALESCE(SUM(total_nota), 0) AS total_faturamento,
            COUNT(*) AS total_notas
        FROM notas
        GROUP BY codigo_vendedor
        ORDER BY total_faturamento DESC
    """)

    with engine.connect() as conn:
        return (
            conn.execute(
                sql,
                {"data": data, "departamento": departamento},
            )
            .mappings()
            .all()
        )


def get_faturamento_produtos(data: str, departamento: int | None = None):
    sql = text("""
        SELECT
            codigo_item,
            descricao_item,
            COALESCE(SUM(quantidade), 0) AS quantidade_total,
            COALESCE(SUM(quantidade * valor_unitario), 0) AS valor_total
        FROM faturamento_loja
        WHERE data_emissao = CAST(:data AS date)
          AND departamento = :departamento
        GROUP BY codigo_item, descricao_item
        ORDER BY quantidade_total DESC
    """)

    with engine.connect() as conn:
        return (
            conn.execute(
                sql,
                {"data": data, "departamento": departamento},
            )
            .mappings()
            .all()
        )


def get_resumo_por_periodo(
    inicio: str,
    fim: str,
    departamento: int | None = None,
):
    sql = text("""
        WITH notas AS (
            SELECT DISTINCT
                data_emissao,
                departamento,
                filial_nota,
                serie_nota,
                numero_nota,
                total_nota
            FROM faturamento_loja
            WHERE data_emissao BETWEEN CAST(:inicio AS date) AND CAST(:fim AS date)
              AND departamento = :departamento
        )
        SELECT
            COALESCE(SUM(total_nota), 0) AS total_faturamento,
            COUNT(*) AS total_notas
        FROM notas
    """)

    with engine.connect() as conn:
        return (
            conn.execute(
                sql,
                {
                    "inicio": inicio,
                    "fim": fim,
                    "departamento": departamento,
                },
            )
            .mappings()
            .first()
        )


def get_filiais_por_periodo(
    inicio: str,
    fim: str,
    departamento: int | None = None,
):
    sql = text("""
        WITH notas AS (
            SELECT DISTINCT
                data_emissao,
                departamento,
                filial_nota,
                serie_nota,
                numero_nota,
                total_nota
            FROM faturamento_loja
            WHERE data_emissao BETWEEN CAST(:inicio AS date) AND CAST(:fim AS date)
              AND departamento = :departamento
        )
        SELECT
            filial_nota,
            COALESCE(SUM(total_nota), 0) AS total_faturamento,
            COUNT(*) AS total_notas
        FROM notas
        GROUP BY filial_nota
        ORDER BY total_faturamento DESC
    """)

    with engine.connect() as conn:
        return (
            conn.execute(
                sql,
                {
                    "inicio": inicio,
                    "fim": fim,
                    "departamento": departamento,
                },
            )
            .mappings()
            .all()
        )


def get_vendedores_por_periodo(
    inicio: str,
    fim: str,
    departamento: int | None = None,
):
    sql = text("""
        WITH notas AS (
            SELECT DISTINCT
                data_emissao,
                departamento,
                filial_nota,
                serie_nota,
                numero_nota,
                codigo_vendedor,
                total_nota
            FROM faturamento_loja
            WHERE data_emissao BETWEEN CAST(:inicio AS date) AND CAST(:fim AS date)
              AND departamento = :departamento
        )
        SELECT
            codigo_vendedor,
            COALESCE(SUM(total_nota), 0) AS total_faturamento,
            COUNT(*) AS total_notas
        FROM notas
        GROUP BY codigo_vendedor
        ORDER BY total_faturamento DESC
    """)

    with engine.connect() as conn:
        return (
            conn.execute(
                sql,
                {
                    "inicio": inicio,
                    "fim": fim,
                    "departamento": departamento,
                },
            )
            .mappings()
            .all()
        )


def get_produtos_por_periodo(
    inicio: str,
    fim: str,
    departamento: int | None = None,
):
    sql = text("""
        SELECT
            codigo_item,
            descricao_item,
            COALESCE(SUM(quantidade), 0) AS quantidade_total,
            COALESCE(SUM(quantidade * valor_unitario), 0) AS valor_total
        FROM faturamento_loja
        WHERE data_emissao BETWEEN CAST(:inicio AS date) AND CAST(:fim AS date)
          AND departamento = :departamento
        GROUP BY codigo_item, descricao_item
        ORDER BY quantidade_total DESC
    """)

    with engine.connect() as conn:
        return (
            conn.execute(
                sql,
                {
                    "inicio": inicio,
                    "fim": fim,
                    "departamento": departamento,
                },
            )
            .mappings()
            .all()
        )


def get_faturamento_evolucao_periodo(
    data_inicio: str, data_fim: str, departamento: int
):
    sql = text("""
               SELECT
                   data_emissao,
                   SUM(total_nota) AS total_faturamento
               FROM faturamento_loja
               WHERE data_emissao BETWEEN :data_inicio AND :data_fim
                    AND departamento = :departamento
               GROUP BY data_emissao
               ORDER BY data_emissao
    """)

    with engine.connect() as conn:
        result = conn.execute(
            sql,
            {
                "data_inicio": data_inicio,
                "data_fim": data_fim,
                "departamento": departamento,
            },
        )

        return [dict(row._mapping) for row in result.fetchall()]
