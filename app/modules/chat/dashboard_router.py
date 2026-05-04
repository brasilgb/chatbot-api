from fastapi import APIRouter, Query
from app.modules.chat.dashboard_service import (
    get_logs,
    get_logs_sem_resposta,
    get_metricas,
    get_uso_por_dia,
    top_perguntas,
    ranking_intents,
    top_sem_resposta,
)

router = APIRouter(prefix="/chat/dashboard", tags=["Chat Dashboard"])


@router.get("/logs")
def logs(
    limit: int = Query(50, ge=1, le=200),
    inicio: str | None = None,
    fim: str | None = None,
):
    return {
        "success": True,
        "data": get_logs(limit, inicio, fim),
    }


@router.get("/sem-resposta")
def sem_resposta(
    limit: int = Query(50, ge=1, le=200),
    inicio: str | None = None,
    fim: str | None = None,
):
    return {
        "success": True,
        "data": get_logs_sem_resposta(limit, inicio, fim),
    }


@router.get("/metricas")
def metricas(
    inicio: str | None = None,
    fim: str | None = None,
):
    return {
        "success": True,
        "data": get_metricas(inicio, fim),
    }


@router.get("/uso-por-dia")
def uso_por_dia(
    inicio: str | None = None,
    fim: str | None = None,
):
    return {
        "success": True,
        "data": get_uso_por_dia(inicio, fim),
    }


@router.get("/top-perguntas")
def get_top_perguntas(
    limit: int = Query(10),
    inicio: str | None = None,
    fim: str | None = None,
):
    return {
        "success": True,
        "data": top_perguntas(limit=limit, inicio=inicio, fim=fim),
    }


@router.get("/ranking-intents")
def get_ranking_intents(
    limit: int = Query(10),
    inicio: str | None = None,
    fim: str | None = None,
):
    return {
        "success": True,
        "data": ranking_intents(limit=limit, inicio=inicio, fim=fim),
    }

@router.get("/top-sem-resposta")
def get_top_sem_resposta(
    limit: int = Query(10),
    inicio: str | None = None,
    fim: str | None = None,
):
    return {
        "success": True,
        "data": top_sem_resposta(limit=limit, inicio=inicio, fim=fim),
    }
