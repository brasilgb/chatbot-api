from app.modules.chat.parsers.intent_parser import parse_intent

from app.modules.chat.handlers.resumo_total_handler import (
    responder_resumo_total,
)


def processar_chat(message: str):
    intent = parse_intent(message)

    modulo = intent.get("modulo")

    if modulo == "resumo_total":
        resposta = responder_resumo_total(intent)

        return {
            "success": True,
            "answer": resposta,
            "intent": intent,
        }

    return {
        "success": False,
        "answer": "Não consegui entender sua pergunta.",
        "intent": intent,
    }