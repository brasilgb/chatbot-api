from datetime import date

from app.modules.resumo_total.repository import (
    get_ultimo_resumo,
    get_resumo_por_data,
    get_resumo_periodo,
    get_evolucao_faturamento,
    get_meta_vs_realizado,
)


def buscar_ultimo_resumo(departamento: int | None = None):
    return get_ultimo_resumo(departamento=departamento)


def buscar_resumo_por_data(
    data: str | date,
    departamento: int | None = None,
):
    return get_resumo_por_data(
        data=str(data),
        departamento=departamento,
    )


def buscar_resumo_periodo(
    data_inicio: str | date,
    data_fim: str | date,
    departamento: int | None = None,
):
    return get_resumo_periodo(
        data_inicio=str(data_inicio),
        data_fim=str(data_fim),
        departamento=departamento,
    )


def buscar_evolucao_faturamento(
    data_inicio: str | date,
    data_fim: str | date,
    departamento: int | None = None,
):
    return get_evolucao_faturamento(
        data_inicio=str(data_inicio),
        data_fim=str(data_fim),
        departamento=departamento,
    )


def buscar_meta_vs_realizado(
    data: str | date,
    departamento: int | None = None,
):
    return get_meta_vs_realizado(
        data=str(data),
        departamento=departamento,
    )

