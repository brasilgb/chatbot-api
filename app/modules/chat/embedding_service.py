import requests
from app.core.config import settings


def _ollama_embed_url() -> str:
    return f"{settings.ollama_base_url.rstrip('/')}/api/embed"


def gerar_embedding(texto: str) -> list[float]:
    texto = texto.strip()
    if not texto:
        raise ValueError("Texto vazio não pode gerar embedding.")

    response = requests.post(
        _ollama_embed_url(),
        json={
            "model": settings.ollama_embed_model,
            "input": texto,
        },
        timeout=settings.ollama_timeout_seconds,
    )

    response.raise_for_status()
    data = response.json()

    embeddings = data.get("embeddings")

    if not embeddings:
        raise ValueError("Ollama não retornou embedding.")

    return embeddings[0]
