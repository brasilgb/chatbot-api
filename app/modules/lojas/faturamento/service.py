from decimal import Decimal
from app.modules.lojas.faturamento.repository import (
    get_faturamento_por_data,
    get_faturamento_por_filial,
    get_faturamento_vendedores,
    get_faturamento_produtos,
    get_resumo_por_periodo,
    get_filiais_por_periodo,
    get_vendedores_por_periodo,
    get_produtos_por_periodo,
)


def decimal_to_float(value):
    if isinstance(value, Decimal):
        return float(value)
    return value


def resumo_faturamento(data: str):
    resumo = get_faturamento_por_data(data)
    filiais = get_faturamento_por_filial(data)

    if not resumo:
        return {
            "data": data,
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


def faturamento_filiais(data: str):
    filiais = get_faturamento_por_filial(data)

    return [
        {
            "filial_nota": item["filial_nota"],
            "total_faturamento": decimal_to_float(item["total_faturamento"]),
            "total_notas": int(item["total_notas"]),
        }
        for item in filiais
    ]

def faturamento_vendedores(data: str):
    vendedores = get_faturamento_vendedores(data)

    return [
        {
            "codigo_vendedor": item["codigo_vendedor"],
            "total_faturamento": decimal_to_float(item["total_faturamento"]),
            "total_notas": int(item["total_notas"]),
        }
        for item in vendedores
    ]

def faturamento_produtos(data: str):
    produtos = get_faturamento_produtos(data)

    return [
        {
            "codigo_item": item["codigo_item"],
            "descricao_item": item["descricao_item"],
            "quantidade_total": decimal_to_float(item["quantidade_total"]),
            "valor_total": decimal_to_float(item["valor_total"]),
        }
        for item in produtos
    ]

def resumo_faturamento_periodo(inicio: str, fim: str):
    resumo = get_resumo_por_periodo(inicio, fim)

    total_faturamento = decimal_to_float(resumo["total_faturamento"] or 0)
    total_notas = int(resumo["total_notas"] or 0)
    ticket_medio = total_faturamento / total_notas if total_notas else 0

    return {
        "inicio": inicio,
        "fim": fim,
        "total_faturamento": total_faturamento,
        "total_notas": total_notas,
        "ticket_medio": round(ticket_medio, 2),
    }

def faturamento_filiais_periodo(inicio: str, fim: str):
    filiais = get_filiais_por_periodo(inicio, fim)

    return [
        {
            "filial_nota": item["filial_nota"],
            "total_faturamento": decimal_to_float(item["total_faturamento"]),
            "total_notas": int(item["total_notas"]),
        }
        for item in filiais
    ]

def faturamento_vendedores_periodo(inicio: str, fim: str):
    vendedores = get_vendedores_por_periodo(inicio, fim)

    return [
        {
            "codigo_vendedor": item["codigo_vendedor"],
            "total_faturamento": decimal_to_float(item["total_faturamento"]),
            "total_notas": int(item["total_notas"]),
        }
        for item in vendedores
    ]

def faturamento_produtos_periodo(inicio: str, fim: str):
    produtos = get_produtos_por_periodo(inicio, fim)

    return [
        {
            "codigo_item": item["codigo_item"],
            "descricao_item": item["descricao_item"],
            "quantidade_total": decimal_to_float(item["quantidade_total"]),
            "valor_total": decimal_to_float(item["valor_total"]),
        }
        for item in produtos
    ]