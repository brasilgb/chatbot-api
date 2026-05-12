from fastapi import APIRouter, Query
from app.modules.lojas.faturamento.service import (
    resumo_faturamento,
    faturamento_filiais,
    faturamento_vendedores,
    faturamento_produtos,
    resumo_faturamento_periodo,
    faturamento_filiais_periodo,
    faturamento_vendedores_periodo,
    faturamento_produtos_periodo,
)

router = APIRouter(
    prefix="/lojas/faturamento",
    tags=["Lojas - Faturamento"],
)


@router.get("/resumo")
def get_resumo_faturamento(data: str = Query(..., examples=["2026-01-27"])):
    return resumo_faturamento(data)


@router.get("/filiais")
def get_faturamento_filiais(data: str = Query(..., examples=["2026-01-27"])):
    return faturamento_filiais(data)


@router.get("/vendedores")
def get_faturamento_vendedores(data: str = Query(..., examples=["2026-01-27"])):
    return faturamento_vendedores(data)


@router.get("/produtos")
def get_faturamento_produtos(data: str = Query(..., examples=["2026-01-27"])):
    return faturamento_produtos(data)


@router.get("/periodo/resumo")
def get_resumo_faturamento_periodo(
    inicio: str = Query(..., examples=["2026-01-01"]),
    fim: str = Query(..., examples=["2026-01-31"]),
):
    return resumo_faturamento_periodo(inicio, fim)


@router.get("/periodo/filiais")
def get_faturamento_filiais_periodo(
    inicio: str = Query(..., examples=["2026-01-01"]),
    fim: str = Query(..., examples=["2026-01-31"]),
):
    return faturamento_filiais_periodo(inicio, fim)


@router.get("/periodo/vendedores")
def get_faturamento_vendedores_periodo(
    inicio: str = Query(..., examples=["2026-01-01"]),
    fim: str = Query(..., examples=["2026-01-31"]),
):
    return faturamento_vendedores_periodo(inicio, fim)


@router.get("/periodo/produtos")
def get_faturamento_produtos_periodo(
    inicio: str = Query(..., examples=["2026-01-01"]),
    fim: str = Query(..., examples=["2026-01-31"]),
):
    return faturamento_produtos_periodo(inicio, fim)
