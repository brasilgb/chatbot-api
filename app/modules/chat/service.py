from app.modules.chat.parsers.intent_parser import parse_intent_hibrido

from app.modules.chat.handlers.resumo_total_handler import (
    responder_resumo_total,
)

SELECOES_PENDENTES = {}


def precisa_selecionar_departamento(intent: dict) -> bool:
    modulo = intent.get("modulo")
    departamento = intent.get("departamento")

    if modulo != "resumo_total":
        return False

    if departamento is None:
        return True

    return False


def responder_selecao_departamento(intent: dict, session_id: str = "default") -> dict:
    pergunta = intent.get("pergunta") or ""

    SELECOES_PENDENTES[session_id] = {
        "tipo": "departamento",
        "pergunta": pergunta,
    }

    return {
        "success": True,
        "type": "selection",
        "answer": (
            "Selecione uma opção:\n\n" "1️⃣ Grupo\n" "2️⃣ Lojas\n" "3️⃣ Naturovos"
        ),
        "intent": intent,
        "requires_selection": True,
        "selection_type": "departamento",
        "options": [
            {
                "id": "1",
                "label": "Grupo",
                "value": "grupo",
                "message": f"{pergunta} do grupo",
            },
            {
                "id": "2",
                "label": "Lojas",
                "value": "lojas",
                "message": f"{pergunta} das lojas",
            },
            {
                "id": "3",
                "label": "Naturovos",
                "value": "naturovos",
                "message": f"{pergunta} da naturovos",
            },
        ],
    }


def resolver_selecao_pendente(message: str, session_id: str = "default") -> str | None:
    pendente = SELECOES_PENDENTES.get(session_id)
    texto = message.strip().lower()

    if not pendente:
        if texto in ["1", "2", "3"]:
            return "__SEM_CONTEXTO__"
        return None

    pergunta = pendente.get("pergunta")

    mapa = {
        "1": "do grupo",
        "grupo": "do grupo",
        "2": "das lojas",
        "lojas": "das lojas",
        "loja": "das lojas",
        "3": "da naturovos",
        "naturovos": "da naturovos",
        "naturovo": "da naturovos",
    }

    complemento = mapa.get(texto)

    if not complemento:
        SELECOES_PENDENTES.pop(session_id, None)
        return "__OPCAO_INVALIDA__"

    SELECOES_PENDENTES.pop(session_id, None)

    return f"{pergunta} {complemento}"


def processar_chat(message: str, session_id: str = "default"):

    mensagem_resolvida = resolver_selecao_pendente(message, session_id)

    if mensagem_resolvida == "__SEM_CONTEXTO__":
        return {
            "success": False,
            "answer": "Não encontrei uma seleção pendente. Por favor, refaça a pergunta.",
            "intent": None,
        }

    if mensagem_resolvida == "__OPCAO_INVALIDA__":
        return {
            "success": False,
            "answer": "Opção inválida ou contexto expirado. Por favor, refaça a pergunta.",
            "intent": None,
        }

    if mensagem_resolvida:
        message = mensagem_resolvida

    intent = parse_intent_hibrido(message)

    if precisa_selecionar_departamento(intent):
        return responder_selecao_departamento(intent, session_id)

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
