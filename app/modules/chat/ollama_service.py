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
                "options": {
                    "num_predict": 120,
                    "temperature": 0.2,
                },
            },
            timeout=8,
        )

        response.raise_for_status()

        data = response.json()
        resposta = data.get("response", "").strip()

        return resposta or resposta_base

    except Exception as e:
        print(f"[OLLAMA FALLBACK] {e}")
        return resposta_base