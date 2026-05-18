import requests


OLLAMA_URL = "http://chatbot_ollama:11434/api/embeddings"
MODEL_NAME = "nomic-embed-text"


def gerar_embedding(texto: str) -> list[float]:
    if not texto or not texto.strip():
        raise ValueError("Texto vazio para gerar embedding")

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": texto.strip(),
        },
        timeout=120,
    )

    response.raise_for_status()
    data = response.json()

    embedding = data.get("embedding")

    if not embedding:
        raise RuntimeError("Ollama não retornou embedding")

    return embedding