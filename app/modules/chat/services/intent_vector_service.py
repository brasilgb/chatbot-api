from sqlalchemy import text
from app.core.database import engine
from app.rag.embeddings import gerar_embedding


LIMITE_SCORE_INTENT = 0.75


def buscar_intent_semantica(pergunta: str):
    embedding = gerar_embedding(pergunta)

    sql = text("""
        SELECT
            pergunta,
            modulo,
            tipo,
            departamento,
            departamento_nome,
            1 - (embedding <=> :embedding) AS score
        FROM intent_embeddings
        WHERE ativo = true
        ORDER BY embedding <=> :embedding
        LIMIT 1
    """)

    with engine.connect() as conn:
        row = conn.execute(sql, {"embedding": str(embedding)}).mappings().first()

    if not row:
        return None

    score = float(row["score"] or 0)

    if score < LIMITE_SCORE_INTENT:
        return None

    return {
        "modulo": row["modulo"],
        "tipo": row["tipo"],
        "departamento": row["departamento"],
        "departamento_nome": row["departamento_nome"],
        "origem": "vetorial",
        "score": score,
        "pergunta_base": row["pergunta"],
    }