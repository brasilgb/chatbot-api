from app.modules.chat.embedding_service import gerar_embedding
from app.modules.chat.intent_vector_repository import buscar_intent_por_embedding

SIMILARIDADE_MINIMA = 0.72


def detectar_intent_vetorial(
    mensagem: str,
    departamento: int | None = None,
) -> dict | None:
    embedding = gerar_embedding(mensagem)

    resultados = buscar_intent_por_embedding(
        embedding=embedding,
        departamento=departamento,
        limite=1,
    )

    if not resultados:
        return None

    melhor = resultados[0]

    if melhor["similaridade"] < SIMILARIDADE_MINIMA:
        return None

    intent = melhor["intent"]

    if isinstance(intent, str):
        import json

        intent = json.loads(intent)

    intent["_origem"] = "vetorial"
    intent["_similaridade"] = float(melhor["similaridade"])
    intent["_pergunta_base"] = melhor["pergunta_exemplo"]

    return intent
