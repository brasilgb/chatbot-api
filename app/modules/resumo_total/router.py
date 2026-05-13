from fastapi import APIRouter, Query

from app.modules.resumo_total.schemas import (
    ResumoTotalBase,
    ResumoPeriodoResponse,
    EvolucaoFaturamentoResponse,
    MetaVsRealizadoResponse,
)

from app.modules.resumo_total.service import (
    buscar_ultimo_resumo,
    buscar_resumo_por_data,
    buscar_resumo_periodo,
    buscar_evolucao_faturamento,
    buscar_meta_vs_realizado,
)

router = APIRouter(
    prefix="/resumo-total",
    tags=["Resumo Total"],
)


@router.get(
    "/ultimo",
    response_model=ResumoTotalBase | None,
)
def ultimo_resumo(
    departamento: int | None = Query(default=None),
):
    return buscar_ultimo_resumo(
        departamento=departamento,
    )


@router.get(
    "/data",
    response_model=list[ResumoTotalBase],
)
def resumo_por_data(
    data: str,
    departamento: int | None = Query(default=None),
):
    return buscar_resumo_por_data(
        data=data,
        departamento=departamento,
    )


@router.get(
    "/periodo",
    response_model=list[ResumoPeriodoResponse],
)
def resumo_periodo(
    data_inicio: str,
    data_fim: str,
    departamento: int | None = Query(default=None),
):
    return buscar_resumo_periodo(
        data_inicio=data_inicio,
        data_fim=data_fim,
        departamento=departamento,
    )


@router.get(
    "/evolucao",
    response_model=list[EvolucaoFaturamentoResponse],
)
def evolucao_faturamento(
    data_inicio: str,
    data_fim: str,
    departamento: int | None = Query(default=None),
):
    return buscar_evolucao_faturamento(
        data_inicio=data_inicio,
        data_fim=data_fim,
        departamento=departamento,
    )


@router.get(
    "/meta-vs-realizado",
    response_model=list[MetaVsRealizadoResponse],
)
def meta_vs_realizado(
    data: str,
    departamento: int | None = Query(default=None),
):
    return buscar_meta_vs_realizado(
        data=data,
        departamento=departamento,
    )

