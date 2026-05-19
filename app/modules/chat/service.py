from app.modules.chat.parsers.intent_parser import parse_intent_hibrido

from app.modules.chat.handlers.resumo_total_handler import (
    responder_resumo_total,
)

SELECOES_PENDENTES = {}


def gerar_opcoes_departamento() -> list[dict]:
    return [
        {"id": "1", "label": "Grupo", "value": "grupo", "message": "1"},
        {"id": "2", "label": "Lojas", "value": "lojas", "message": "2"},
        {"id": "3", "label": "Naturovos", "value": "naturovos", "message": "3"},
    ]


def precisa_selecionar_departamento(intent: dict) -> bool:
    return intent.get("modulo") == "resumo_total" and intent.get("departamento") is None


def responder_selecao_departamento(intent: dict, session_id: str = "default") -> dict:
    SELECOES_PENDENTES[session_id] = {
        "tipo": "departamento",
        "intent": intent,
    }

    return {
        "success": True,
        "type": "selection",
        "answer": "Selecione uma opção:\n\n1️⃣ Grupo\n2️⃣ Lojas\n3️⃣ Naturovos",
        "intent": intent,
        "requires_selection": True,
        "selection_type": "departamento",
        "options": gerar_opcoes_departamento(),
    }


def resolver_selecao_pendente(message: str, session_id: str = "default"):
    pendente = SELECOES_PENDENTES.get(session_id)
    texto = message.strip().lower()

    mapa = {
        "1": (0, "Grupo"),
        "grupo": (0, "Grupo"),
        "2": (1, "Lojas"),
        "lojas": (1, "Lojas"),
        "loja": (1, "Lojas"),
        "3": (5, "Naturovos"),
        "naturovos": (5, "Naturovos"),
        "naturovo": (5, "Naturovos"),
    }

    if texto not in mapa:
        return None

    if not pendente:
        return "__SEM_CONTEXTO__"

    departamento, departamento_nome = mapa[texto]

    intent = pendente.get("intent", {}).copy()
    intent["departamento"] = departamento
    intent["departamento_nome"] = departamento_nome

    # Não remove o contexto.
    # Assim o usuário pode continuar clicando 1, 2 ou 3 para comparar.
    return intent


def responder_com_intent(intent: dict) -> dict:
    modulo = intent.get("modulo")

    if modulo == "resumo_total":
        resposta = responder_resumo_total(intent)

        return {
            "success": True,
            "answer": resposta,
            "intent": intent,
            "options": gerar_opcoes_departamento(),
        }

    return {
        "success": False,
        "answer": "Não consegui entender sua pergunta.",
        "intent": intent,
    }


def processar_chat(message: str, session_id: str = "default"):
    print("MESSAGE:", message)
    print("SESSION_ID:", session_id)
    print("SELECOES_PENDENTES:", SELECOES_PENDENTES)

    selecao_resolvida = resolver_selecao_pendente(message, session_id)

    if selecao_resolvida == "__SEM_CONTEXTO__":
        return {
            "success": False,
            "answer": "Não encontrei uma seleção pendente. Por favor, refaça a pergunta.",
            "intent": None,
        }

    if isinstance(selecao_resolvida, dict):
        return responder_com_intent(selecao_resolvida)

    intent = parse_intent_hibrido(message)

    if precisa_selecionar_departamento(intent):
        return responder_selecao_departamento(intent, session_id)

    # Pergunta nova com departamento definido atualiza o contexto base.
    if intent.get("modulo") == "resumo_total":
        SELECOES_PENDENTES[session_id] = {
            "tipo": "departamento",
            "intent": intent,
        }

    return responder_com_intent(intent)