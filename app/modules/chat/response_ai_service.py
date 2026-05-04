from app.modules.chat.ollama_service import reescrever_resposta


def gerar_resposta_ia(
    pergunta: str,
    resposta_base: str,
) -> str:
    """
    Usa IA para melhorar a resposta sem alterar dados.
    """

    resposta_ia = reescrever_resposta(pergunta, resposta_base)

    if not resposta_ia:
        return resposta_base

    return resposta_ia