from sqlalchemy import text
from app.core.database import SessionLocal
import json

def criar_aprendizado(
    pergunta_original: str,
    pergunta_chave: str,
    resposta: str,
    intent: dict | None = None,
):
    db = SessionLocal()

    try:
        result = db.execute(
            text("""
                INSERT INTO chat_aprendizados (
                    pergunta_original,
                    pergunta_chave,
                    resposta,
                    intent
                )
                VALUES (
                    :pergunta_original,
                    :pergunta_chave,
                    :resposta,
                    CAST(:intent AS jsonb)
                )
                RETURNING id, pergunta_original, pergunta_chave, resposta, intent, ativo, created_at
            """),
            {
                "pergunta_original": pergunta_original,
                "pergunta_chave": pergunta_chave.lower().strip(),
                "resposta": resposta,
                "intent": json.dumps(intent) if intent is not None else "{}",
            },
        )

        db.commit()
        return dict(result.fetchone()._mapping)

    finally:
        db.close()


def listar_aprendizados(limit: int = 50):
    db = SessionLocal()

    try:
        result = db.execute(
            text("""
                SELECT id, pergunta_original, pergunta_chave, resposta, intent, ativo, created_at
                FROM chat_aprendizados
                ORDER BY id DESC
                LIMIT :limit
            """),
            {"limit": limit},
        )

        return [dict(row._mapping) for row in result.fetchall()]

    finally:
        db.close()


def buscar_aprendizado(pergunta: str):
    db = SessionLocal()

    try:
        pergunta_normalizada = pergunta.lower().strip()

        result = db.execute(
            text("""
                SELECT id, resposta, intent
                FROM chat_aprendizados
                WHERE ativo = true
                  AND :pergunta ILIKE '%' || pergunta_chave || '%'
                ORDER BY id DESC
                LIMIT 1
            """),
            {"pergunta": pergunta_normalizada},
        )

        row = result.fetchone()
        return dict(row._mapping) if row else None

    finally:
        db.close()