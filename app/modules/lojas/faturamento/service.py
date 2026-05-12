from decimal import Decimal
from sqlalchemy import text
from app.core.database import engine

from app.modules.lojas.faturamento.repository import (
    get_faturamento_por_data,
    get_faturamento_por_filial,
    get_faturamento_vendedores,
    get_faturamento_produtos,
    get_resumo_por_periodo,
    get_filiais_por_periodo,
    get_vendedores_por_periodo,
    get_produtos_por_periodo,
    get_faturamento_evolucao_periodo,
)


def decimal_to_float(value):
    if isinstance(value, Decimal):
        return float(value)
    return value


def resumo_faturamento(data: str, departamento: int = 1):
    resumo = get_faturamento_por_data(data, departamento)
    filiais = get_faturamento_por_filial(data, departamento)

    if not resumo:
        return {
            "data": data,
            "departamento": departamento,
            "total_faturamento": 0,
            "total_notas": 0,
            "ticket_medio": 0,
            "filiais": [],
        }

    total_faturamento = decimal_to_float(resumo["total_faturamento"])
    total_notas = int(resumo["total_notas"])
    ticket_medio = total_faturamento / total_notas if total_notas else 0

    return {
        "data": str(resumo["data_emissao"]),
        "departamento": departamento,
        "total_faturamento": total_faturamento,
        "total_notas": total_notas,
        "ticket_medio": round(ticket_medio, 2),
        "filiais": [
            {
                "filial_nota": item["filial_nota"],
                "total_faturamento": decimal_to_float(item["total_faturamento"]),
                "total_notas": int(item["total_notas"]),
            }
            for item in filiais
        ],
    }


def faturamento_filiais(data: str, departamento: int = 1):
    filiais = get_faturamento_por_filial(data, departamento)

    return [
        {
            "filial_nota": item["filial_nota"],
            "total_faturamento": decimal_to_float(item["total_faturamento"]),
            "total_notas": int(item["total_notas"]),
        }
        for item in filiais
    ]


def faturamento_vendedores(data: str, departamento: int = 1):
    vendedores = get_faturamento_vendedores(data, departamento)

    return [
        {
            "codigo_vendedor": item["codigo_vendedor"],
            "total_faturamento": decimal_to_float(item["total_faturamento"]),
            "total_notas": int(item["total_notas"]),
        }
        for item in vendedores
    ]


def faturamento_produtos(data: str, departamento: int = 1):
    produtos = get_faturamento_produtos(data, departamento)

    return [
        {
            "codigo_item": item["codigo_item"],
            "descricao_item": item["descricao_item"],
            "quantidade_total": decimal_to_float(item["quantidade_total"]),
            "valor_total": decimal_to_float(item["valor_total"]),
        }
        for item in produtos
    ]


def resumo_faturamento_periodo(inicio: str, fim: str, departamento: int = 1):
    resumo = get_resumo_por_periodo(inicio, fim, departamento)

    total_faturamento = decimal_to_float(resumo["total_faturamento"] or 0)
    total_notas = int(resumo["total_notas"] or 0)
    ticket_medio = total_faturamento / total_notas if total_notas else 0

    return {
        "inicio": inicio,
        "fim": fim,
        "departamento": departamento,
        "total_faturamento": total_faturamento,
        "total_notas": total_notas,
        "ticket_medio": round(ticket_medio, 2),
    }


def faturamento_filiais_periodo(inicio: str, fim: str, departamento: int = 1):
    filiais = get_filiais_por_periodo(inicio, fim, departamento)

    return [
        {
            "filial_nota": item["filial_nota"],
            "total_faturamento": decimal_to_float(item["total_faturamento"]),
            "total_notas": int(item["total_notas"]),
        }
        for item in filiais
    ]


def faturamento_vendedores_periodo(inicio: str, fim: str, departamento: int = 1):
    vendedores = get_vendedores_por_periodo(inicio, fim, departamento)

    return [
        {
            "codigo_vendedor": item["codigo_vendedor"],
            "total_faturamento": decimal_to_float(item["total_faturamento"]),
            "total_notas": int(item["total_notas"]),
        }
        for item in vendedores
    ]


def faturamento_produtos_periodo(inicio: str, fim: str, departamento: int = 1):
    produtos = get_produtos_por_periodo(inicio, fim, departamento)

    return [
        {
            "codigo_item": item["codigo_item"],
            "descricao_item": item["descricao_item"],
            "quantidade_total": decimal_to_float(item["quantidade_total"]),
            "valor_total": decimal_to_float(item["valor_total"]),
        }
        for item in produtos
    ]


def get_ranking_vendedores(data: str, departamento: int = 1):
    sql = text("""
        SELECT
            codigo_vendedor,
            SUM(total_nota) AS total_faturamento
        FROM faturamento_loja
        WHERE data_emissao = :data
          AND departamento = :departamento
        GROUP BY codigo_vendedor
        ORDER BY total_faturamento DESC
        LIMIT 10
    """)

    with engine.connect() as conn:
        result = (
            conn.execute(
                sql,
                {
                    "data": data,
                    "departamento": departamento,
                },
            )
            .mappings()
            .all()
        )

    return result


def montar_dados_ranking_vendedores(rows):
    dados = []

    for i, row in enumerate(rows, start=1):
        total = float(row["total_faturamento"])

        dados.append(
            {
                "Posição": i,
                "Vendedor": row["codigo_vendedor"],
                "Total": f"R$ {total:,.2f}".replace(",", "X")
                .replace(".", ",")
                .replace("X", "."),
            }
        )

    return dados


def montar_dados_evolucao(rows):
    dados = []

    for r in rows:
        dados.append(
            {
                "data": r["data_emissao"].strftime("%d/%m/%Y"),
                "total": float(r["total_faturamento"] or 0),
            }
        )
    return dados
