import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "gemma3:4b"


def reescrever_resposta(pergunta: str, resposta_base: str) -> str:
    prompt = f"""
Você é um assistente empresarial objetivo.

Reescreva a resposta abaixo de forma natural, clara e curta.
Não invente dados.
Não altere valores, datas, quantidades ou nomes.
Não adicione explicações extras.

Pergunta do usuário:
{pergunta}

Resposta base:
{resposta_base}

Resposta final:
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()
        return data.get("response", resposta_base).strip() or resposta_base

    except Exception:
        return resposta_base
