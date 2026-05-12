import logging

import requests

from app.core.config import settings

logger = logging.getLogger(__name__)


def _ollama_generate_url() -> str:
    return f"{settings.ollama_base_url_normalized}/api/generate"


def _build_rewrite_prompt(pergunta: str, resposta_base: str) -> str:
    return f"""
Você é um assistente empresarial objetivo.

Reescreva a resposta abaixo de forma natural, clara e curta.
Não invente dados.
Não altere valores, datas, quantidades ou nomes.
Não adicione explicações extras.
Se a resposta base já estiver clara, preserve o conteúdo com pequenas melhorias.

Pergunta do usuário:
{pergunta}

Resposta base:
{resposta_base}

Resposta final:
"""


def reescrever_resposta(pergunta: str, resposta_base: str) -> str:
    if not resposta_base or not resposta_base.strip():
        return resposta_base

    try:
        response = requests.post(
            _ollama_generate_url(),
            json={
                "model": settings.ollama_model,
                "prompt": _build_rewrite_prompt(pergunta, resposta_base),
                "stream": False,
                "options": {
                    "num_predict": settings.ollama_num_predict,
                    "temperature": settings.ollama_temperature,
                },
            },
            timeout=settings.ollama_rewrite_timeout_seconds,
        )

        response.raise_for_status()

        data = response.json()
        resposta = data.get("response", "").strip()

        return resposta or resposta_base

    except requests.RequestException:
        logger.exception("Falha ao consultar Ollama; usando resposta base.")
        return resposta_base
    except ValueError:
        logger.exception("Ollama retornou JSON inválido; usando resposta base.")
        return resposta_base
