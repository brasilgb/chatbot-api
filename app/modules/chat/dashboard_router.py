from datetime import date
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import text

from app.core.database import engine


router = APIRouter(
    prefix="/chat/dashboard",
    tags=["Chat Dashboard"],
)


class AprendizadoRequest(BaseModel):
    pergunta_original: str
    pergunta_chave: str
    resposta: str
    intent: dict | None = None


def filtros_data(inicio: Optional[date], fim: Optional[date]):
    where = []
    params = {}

    if inicio:
        where.append("created_at::date >= :inicio")
        params["inicio"] = inicio

    if fim:
        where.append("created_at::date <= :fim")
        params["fim"] = fim

    sql_where = "WHERE " + " AND ".join(where) if where else ""
    return sql_where, params


@router.get("/metricas")
def metricas(inicio: Optional[date] = None, fim: Optional[date] = None):
    sql_where, params = filtros_data(inicio, fim)

    sql = text(f"""
        SELECT
            COUNT(*) AS total_perguntas,
            COUNT(*) FILTER (WHERE sucesso = true) AS total_sucesso,
            COUNT(*) FILTER (WHERE sucesso = false) AS total_falhas
        FROM chat_logs
        {sql_where}
    """)

    with engine.connect() as conn:
        row = conn.execute(sql, params).mappings().first()

    return {"success": True, "data": dict(row or {})}


@router.get("/logs")
def logs(inicio: Optional[date] = None, fim: Optional[date] = None):
    sql_where, params = filtros_data(inicio, fim)

    sql = text(f"""
        SELECT id, pergunta, resposta, sucesso, created_at
        FROM chat_logs
        {sql_where}
        ORDER BY created_at DESC
        LIMIT 100
    """)

    with engine.connect() as conn:
        rows = conn.execute(sql, params).mappings().all()

    return {"success": True, "data": [dict(row) for row in rows]}


@router.get("/sem-resposta")
def sem_resposta(inicio: Optional[date] = None, fim: Optional[date] = None):
    sql_where, params = filtros_data(inicio, fim)

    sql = text(f"""
        SELECT
            id,
            pergunta,
            COALESCE(motivo, 'Sem resposta') AS resposta,
            false AS sucesso,
            created_at
        FROM chat_sem_resposta
        {sql_where}
        ORDER BY created_at DESC
        LIMIT 100
    """)

    with engine.connect() as conn:
        rows = conn.execute(sql, params).mappings().all()

    return {"success": True, "data": [dict(row) for row in rows]}


@router.get("/uso-por-dia")
def uso_por_dia(inicio: Optional[date] = None, fim: Optional[date] = None):
    sql_where, params = filtros_data(inicio, fim)

    sql = text(f"""
        SELECT
            created_at::date AS data,
            COUNT(*) AS total,
            COUNT(*) FILTER (WHERE sucesso = true) AS sucesso,
            COUNT(*) FILTER (WHERE sucesso = false) AS falhas
        FROM chat_logs
        {sql_where}
        GROUP BY created_at::date
        ORDER BY created_at::date
    """)

    with engine.connect() as conn:
        rows = conn.execute(sql, params).mappings().all()

    data = []
    for row in rows:
        item = dict(row)
        item["data"] = str(item["data"])
        data.append(item)

    return {"success": True, "data": data}


@router.get("/top-perguntas")
def top_perguntas(inicio: Optional[date] = None, fim: Optional[date] = None):
    sql_where, params = filtros_data(inicio, fim)

    sql = text(f"""
        SELECT LOWER(TRIM(pergunta)) AS pergunta, COUNT(*) AS total
        FROM chat_logs
        {sql_where}
        GROUP BY LOWER(TRIM(pergunta))
        ORDER BY total DESC
        LIMIT 10
    """)

    with engine.connect() as conn:
        rows = conn.execute(sql, params).mappings().all()

    return {"success": True, "data": [dict(row) for row in rows]}


@router.get("/ranking-intents")
def ranking_intents(inicio: Optional[date] = None, fim: Optional[date] = None):
    sql_where, params = filtros_data(inicio, fim)

    sql = text(f"""
        SELECT
            COALESCE(intent->>'modulo', 'desconhecido') AS intent,
            COUNT(*) AS total
        FROM chat_logs
        {sql_where}
        GROUP BY COALESCE(intent->>'modulo', 'desconhecido')
        ORDER BY total DESC
        LIMIT 10
    """)

    with engine.connect() as conn:
        rows = conn.execute(sql, params).mappings().all()

    return {"success": True, "data": [dict(row) for row in rows]}


@router.get("/top-sem-resposta")
def top_sem_resposta(inicio: Optional[date] = None, fim: Optional[date] = None):
    sql_where, params = filtros_data(inicio, fim)

    sql = text(f"""
        SELECT LOWER(TRIM(pergunta)) AS pergunta, COUNT(*) AS total
        FROM chat_sem_resposta
        {sql_where}
        GROUP BY LOWER(TRIM(pergunta))
        ORDER BY total DESC
        LIMIT 10
    """)

    with engine.connect() as conn:
        rows = conn.execute(sql, params).mappings().all()

    return {"success": True, "data": [dict(row) for row in rows]}


@router.post("/aprendizados")
def salvar_aprendizado(payload: AprendizadoRequest):
    sql = text("""
        INSERT INTO chat_aprendizados
            (pergunta_original, pergunta_chave, resposta, intent)
        VALUES
            (:pergunta_original, :pergunta_chave, :resposta, CAST(:intent AS jsonb))
    """)

    with engine.begin() as conn:
        conn.execute(sql, {
            "pergunta_original": payload.pergunta_original,
            "pergunta_chave": payload.pergunta_chave,
            "resposta": payload.resposta,
            "intent": __import__("json").dumps(payload.intent or {}),
        })

    return {"success": True}