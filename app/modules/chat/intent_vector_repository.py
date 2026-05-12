import json
from sqlalchemy import text
from app.core.database import engine


def salvar_intent_embedding(
    pergunta_exemplo: str,
    modulo: str,
    tipo: str,
    departamento: int,
    intent: dict,
    embedding: list[float],
):
    sql = text("""
        INSERT INTO chat_intent_embeddings (
            pergunta_exemplo,
            modulo,
            tipo,
            departamento,
            intent,
            embedding
        )
        VALUES (
            :pergunta_exemplo,
            :modulo,
            :tipo,
            :departamento,
            CAST(:intent AS jsonb),
            :embedding
        )
    """)

    with engine.begin() as conn:
        conn.execute(
            sql,
            {
                "pergunta_exemplo": pergunta_exemplo,
                "modulo": modulo,
                "tipo": tipo,
                "departamento": departamento,
                "intent": json.dumps(intent),
                "embedding": str(embedding),
            },
        )


def buscar_intent_por_embedding(
    embedding: list[float],
    departamento: int | None = None,
    limite: int = 1,
):
    where_departamento = ""
    params = {
        "embedding": str(embedding),
        "limite": limite,
    }

    if departamento:
        where_departamento = "AND departamento = :departamento"
        params["departamento"] = departamento

    sql = text(f"""
        SELECT
            id,
            pergunta_exemplo,
            modulo,
            tipo,
            departamento,
            intent,
            1 - (embedding <=> :embedding) AS similaridade
        FROM chat_intent_embeddings
        WHERE ativo = true
        {where_departamento}
        ORDER BY embedding <=> :embedding
        LIMIT :limite
    """)

    with engine.connect() as conn:
        result = conn.execute(sql, params).mappings().all()

    return [dict(row) for row in result]
