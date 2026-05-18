from sqlalchemy import text
from app.core.database import engine


def _vector_to_sql(embedding: list[float]) -> str:
    return "[" + ",".join(str(x) for x in embedding) + "]"


def salvar_embedding(
    texto: str,
    origem: str,
    referencia_id: int | None,
    embedding: list[float],
):
    sql = text("""
        INSERT INTO chat_embeddings (
            texto,
            origem,
            referencia_id,
            embedding
        )
        VALUES (
            :texto,
            :origem,
            :referencia_id,
            :embedding
        )
    """)

    with engine.begin() as conn:
        conn.execute(
            sql,
            {
                "texto": texto,
                "origem": origem,
                "referencia_id": referencia_id,
                "embedding": _vector_to_sql(embedding),
            },
        )


def buscar_embeddings_similares(
    embedding: list[float],
    origem: str | None = None,
    limite: int = 5,
):
    params = {
        "embedding": _vector_to_sql(embedding),
        "limite": limite,
    }

    filtro_origem = ""

    if origem:
        filtro_origem = "WHERE origem = :origem"
        params["origem"] = origem

    sql = text(f"""
        SELECT
            id,
            texto,
            origem,
            referencia_id,
            1 - (embedding <=> :embedding) AS similaridade
        FROM chat_embeddings
        {filtro_origem}
        ORDER BY embedding <=> :embedding
        LIMIT :limite
    """)

    with engine.connect() as conn:
        return conn.execute(sql, params).mappings().all()