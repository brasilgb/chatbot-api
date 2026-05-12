import requests
from app.core.config import settings


OLLAMA_URL = getattr(settings, "ollama_url", "http://127.0.0.1:11434")
EMBEDDING_MODEL = getattr(settings, "embedding_model", "nomic-embed-text")


def gerar_embedding(texto: str) -> list[float]:
    response = requests.post(
        f"{OLLAMA_URL}/api/embed",
        json={
            "model": EMBEDDING_MODEL,
            "input": texto,
        },
        timeout=30,
    )

    response.raise_for_status()
    data = response.json()

    embeddings = data.get("embeddings")

    if not embeddings:
        raise ValueError("Ollama não retornou embedding.")

    return embeddings[0]