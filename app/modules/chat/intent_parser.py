from app.modules.chat.services.intent_vector_service import buscar_intent_semantica

def parse_intent_hibrido(pergunta: str):
    intent_regras = parse_intent(pergunta)
    intent_vetorial = buscar_intent_semantica(pergunta)

    if not intent_vetorial:
        intent_regras["origem"] = "regras"
        return intent_regras

    modulo_regras = intent_regras.get("modulo")
    tipo_regras = intent_regras.get("tipo")

    # Se o parser por regras não entendeu bem, usa vetorial
    if not modulo_regras:
        return intent_vetorial

    # Se os dois concordam no módulo, pode usar o vetorial para melhorar o tipo
    if modulo_regras == intent_vetorial.get("modulo"):
        intent_final = {
            **intent_regras,
            "tipo": intent_vetorial.get("tipo") or intent_regras.get("tipo"),
            "origem": "hibrido",
            "score_vetorial": intent_vetorial.get("score"),
            "pergunta_base": intent_vetorial.get("pergunta_base"),
        }
        return intent_final

    # Se divergem, mantém regras por segurança
    intent_regras["origem"] = "regras"
    intent_regras["score_vetorial"] = intent_vetorial.get("score")
    intent_regras["intent_vetorial_descartada"] = intent_vetorial
    return intent_regras