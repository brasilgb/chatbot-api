import json
from app.core.database import engine
from sqlalchemy import text


def registrar_chat_log(
    session_id: str,
    pergunta: str,
    resposta: str | None,
    intent: dict | None = None,
    sucesso: bool = True,
):
    sql = """
        INSERT INTO chat_logs (
            session_id,
            pergunta,
            resposta,
            intent,
            sucesso,
            created_at
        )
        VALUES (
            :session_id,
            :pergunta,
            :resposta,
            CAST(:intent AS jsonb),
            :sucesso,
            NOW()
        )
    """

    params = {
        "session_id": session_id,
        "pergunta": pergunta,
        "resposta": resposta,
        "intent": json.dumps(intent or {}, ensure_ascii=False),
        "sucesso": sucesso,
    }

    with engine.begin() as conn:
        conn.execute(text(sql), params)


def registrar_sem_resposta(
    session_id: str,
    pergunta: str,
    intent: dict | None = None,
    motivo: str | None = None,
):
    sql = """
        INSERT INTO chat_sem_resposta (
            session_id,
            pergunta,
            intent,
            motivo,
            created_at
        )
        VALUES (
            :session_id,
            :pergunta,
            CAST(:intent AS jsonb),
            :motivo,
            NOW()
        )
    """

    params = {
        "session_id": session_id,
        "pergunta": pergunta,
        "intent": json.dumps(intent or {}, ensure_ascii=False),
        "motivo": motivo,
    }

    with engine.begin() as conn:
        conn.execute(text(sql), params)