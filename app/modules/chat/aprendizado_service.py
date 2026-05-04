from app.modules.chat.aprendizado_repository import (
    criar_aprendizado,
    listar_aprendizados,
    buscar_aprendizado,
)


def salvar_aprendizado(
    pergunta_original: str,
    pergunta_chave: str,
    resposta: str,
    intent: dict | None = None,
):
    return criar_aprendizado(
        pergunta_original=pergunta_original,
        pergunta_chave=pergunta_chave,
        resposta=resposta,
        intent=intent,
    )


def get_aprendizados(limit: int = 50):
    return listar_aprendizados(limit=limit)


def procurar_aprendizado(pergunta: str):
    return buscar_aprendizado(pergunta)