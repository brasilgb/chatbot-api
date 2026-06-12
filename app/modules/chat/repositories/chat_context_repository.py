import json
from app.core.database import engine
from sqlalchemy import text


def salvar_contexto_chat(
    session_id: str,
    pergunta: str,
    resposta: str | None,
    intent: dict | None,
    contexto: dict | None = None,
):
    if not intent:
        return

    sql = """
        INSERT INTO chat_context (
            session_id,
            modulo,
            tipo,
            departamento,
            departamento_nome,
            data_referencia,
            pergunta,
            resposta,
            intent,
            contexto,
            created_at
        )
        VALUES (
            :session_id,
            :modulo,
            :tipo,
            :departamento,
            :departamento_nome,
            :data_referencia,
            :pergunta,
            :resposta,
            CAST(:intent AS jsonb),
            CAST(:contexto AS jsonb),
            NOW()
        )
    """

    contexto_final = {
        "modulo_atual": intent.get("modulo"),
        "tipo_atual": intent.get("tipo"),
        "departamento_atual": intent.get("departamento"),
        "departamento_nome_atual": intent.get("departamento_nome"),
        "data_atual": intent.get("data"),
        "data_inicio_atual": intent.get("data_inicio"),
        "data_fim_atual": intent.get("data_fim"),
    }

    if contexto:
        contexto_final.update(contexto)

    params = {
        "session_id": session_id,
        "modulo": intent.get("modulo"),
        "tipo": intent.get("tipo"),
        "departamento": intent.get("departamento"),
        "departamento_nome": intent.get("departamento_nome"),
        "data_referencia": intent.get("data") or None,
        "pergunta": pergunta,
        "resposta": resposta,
        "intent": json.dumps(intent or {}, ensure_ascii=False),
        "contexto": json.dumps(contexto_final, ensure_ascii=False),
    }

    with engine.begin() as conn:
        conn.execute(text(sql), params)


def buscar_ultimo_contexto(session_id: str) -> dict | None:
    sql = """
        SELECT
            session_id,
            modulo,
            tipo,
            departamento,
            departamento_nome,
            data_referencia,
            pergunta,
            resposta,
            intent,
            contexto,
            created_at
        FROM chat_context
        WHERE session_id = :session_id
        AND created_at >= NOW() - INTERVAL '2 hours'
        ORDER BY created_at DESC
        LIMIT 1
    """

    with engine.begin() as conn:
        row = conn.execute(text(sql), {"session_id": session_id}).mappings().first()

    if not row:
        return None

    intent = row["intent"]
    contexto = row["contexto"]

    if isinstance(intent, str):
        intent = json.loads(intent)

    if isinstance(contexto, str):
        contexto = json.loads(contexto)

    return {
        "session_id": row["session_id"],
        "modulo": row["modulo"],
        "tipo": row["tipo"],
        "departamento": row["departamento"],
        "departamento_nome": row["departamento_nome"],
        "data_referencia": row["data_referencia"],
        "pergunta": row["pergunta"],
        "resposta": row["resposta"],
        "intent": intent,
        "contexto": contexto,
        "created_at": row["created_at"],
    }
