import json
from sqlalchemy import text
from app.core.database import SessionLocal


def salvar_chat_log(pergunta: str, intent: dict, resposta: str, sucesso: bool):
    db = SessionLocal()

    try:
        db.execute(
            text("""
                INSERT INTO chat_logs (
                    pergunta,
                    intent,
                    resposta,
                    sucesso
                )
                VALUES (
                    :pergunta,
                    :intent,
                    :resposta,
                    :sucesso
                )
            """),
            {
                "pergunta": pergunta,
                "intent": json.dumps(intent),
                "resposta": resposta,
                "sucesso": sucesso,
            }
        )

        db.commit()

    finally:
        db.close()