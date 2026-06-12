from app.modules.chat.parsers.intent_parser import parse_intent_hibrido

from app.modules.chat.handlers.resumo_total_handler import (
    responder_resumo_total,
)

from app.modules.chat.repositories.chat_log_repository import (
    registrar_chat_log,
    registrar_sem_resposta,
)

from app.modules.chat.repositories.chat_context_repository import (
    salvar_contexto_chat,
    buscar_ultimo_contexto,
)

from app.modules.chat.repositories.faturamento_detalhado_repository import (
    buscar_faturamento_por_associacao,
    buscar_faturamento_por_filial,
)

from app.modules.chat.reports.tabela_faturamento_report import (
    gerar_png_tabela_faturamento,
)


MAPA_DEPARTAMENTOS = {
    "1": (0, "Grupo"),
    "grupo": (0, "Grupo"),
    "grupo solar": (0, "Grupo"),
    "2": (1, "Lojas"),
    "lojas": (1, "Lojas"),
    "loja": (1, "Lojas"),
    "3": (5, "Naturovos"),
    "naturovos": (5, "Naturovos"),
    "naturovo": (5, "Naturovos"),
}


FOLLOWUPS_CURTOS = [
    "e ontem?",
    "e ontem",
    "ontem?",
    "ontem",
    "e hoje?",
    "e hoje",
    "hoje?",
    "hoje",
    "e a margem?",
    "e a margem",
    "e margem?",
    "e margem",
    "margem?",
    "margem",
    "e a meta?",
    "e a meta",
    "e meta?",
    "e meta",
    "meta?",
    "meta",
    "e a projeção?",
    "e a projeção",
    "e projeção?",
    "e projeção",
    "projeção?",
    "projeção",
    "e a projecao?",
    "e a projecao",
    "e projecao?",
    "e projecao",
    "projecao?",
    "projecao",
    "e o faturamento?",
    "e o faturamento",
    "e faturamento?",
    "e faturamento",
    "faturamento?",
    "faturamento",
    "e lojas?",
    "e lojas",
    "lojas?",
    "lojas",
    "loja?",
    "loja",
    "e naturovos?",
    "e naturovos",
    "naturovos?",
    "naturovos",
    "naturovo?",
    "naturovo",
    "e grupo?",
    "e grupo",
    "grupo?",
    "grupo",
]


def normalizar_texto(texto: str) -> str:
    return (texto or "").strip().lower()


def gerar_opcoes_departamento(incluir_grupo: bool = True) -> list[dict]:
    opcoes = []

    if incluir_grupo:
        opcoes.append(
            {
                "id": "1",
                "label": "Grupo",
                "value": "grupo",
                "message": "1",
            }
        )

    opcoes.extend(
        [
            {
                "id": "2",
                "label": "Lojas",
                "value": "lojas",
                "message": "2",
            },
            {
                "id": "3",
                "label": "Naturovos",
                "value": "naturovos",
                "message": "3",
            },
        ]
    )

    return opcoes


def precisa_selecionar_departamento(intent: dict) -> bool:
    modulo = intent.get("modulo")
    departamento = intent.get("departamento")

    if departamento is not None:
        return False

    return modulo in [
        "resumo_total",
        "faturamento_filiais",
        "faturamento_associacoes",
    ]


def responder_selecao_departamento(intent: dict, session_id: str) -> dict:
    modulo = intent.get("modulo")
    tipo = intent.get("tipo")

    if modulo in [
        "faturamento_filiais",
        "faturamento_associacoes",
    ] or tipo in [
        "faturamento_filial",
        "faturamento_associacao",
    ]:
        resposta = "Selecione uma opção:\n\n2️⃣ Lojas\n3️⃣ Naturovos"
        opcoes = gerar_opcoes_departamento(False)
    else:
        resposta = "Selecione uma opção:\n\n1️⃣ Grupo\n2️⃣ Lojas\n3️⃣ Naturovos"
        opcoes = gerar_opcoes_departamento(True)

    salvar_contexto_chat(
        session_id=session_id,
        pergunta=intent.get("pergunta") or "",
        resposta=resposta,
        intent=intent,
        contexto={
            "type": "selection",
            "requires_selection": True,
            "selection_type": "departamento",
            "pending_selection": True,
            "tipo_atual": intent.get("tipo"),
            "modulo_atual": intent.get("modulo"),
            "departamento_atual": intent.get("departamento"),
            "departamento_nome_atual": intent.get("departamento_nome"),
            "data_atual": intent.get("data"),
            "data_inicio_atual": intent.get("data_inicio"),
            "data_fim_atual": intent.get("data_fim"),
        },
    )

    return {
        "success": True,
        "type": "selection",
        "answer": resposta,
        "intent": intent,
        "requires_selection": True,
        "selection_type": "departamento",
        "options": opcoes,
    }


def recuperar_contexto_selecao_pendente(session_id: str) -> dict | None:
    ultimo_contexto = buscar_ultimo_contexto(session_id)

    if not ultimo_contexto:
        return None

    contexto = ultimo_contexto.get("contexto") or {}

    if (
        contexto.get("pending_selection") is True
        and contexto.get("selection_type") == "departamento"
        and ultimo_contexto.get("intent")
    ):
        return {
            "tipo": "departamento",
            "intent": ultimo_contexto.get("intent"),
        }

    return None


def resolver_selecao_pendente(message: str, session_id: str = "default"):
    texto = normalizar_texto(message)

    if texto not in MAPA_DEPARTAMENTOS:
        return None

    pendente = recuperar_contexto_selecao_pendente(session_id)

    if not pendente:
        return "__SEM_CONTEXTO__"

    departamento, departamento_nome = MAPA_DEPARTAMENTOS[texto]

    intent = pendente.get("intent", {}).copy()
    intent["departamento"] = departamento
    intent["departamento_nome"] = departamento_nome
    intent["departamento_explicito"] = True
    intent["pergunta"] = pendente.get("intent", {}).get("pergunta")
    intent["origem"] = "selecao_departamento"

    return intent


def responder_faturamento_filiais(intent: dict) -> dict:
    dados = buscar_faturamento_por_filial(
        intent.get("data_inicio"),
        intent.get("data_fim"),
        intent.get("departamento"),
    )

    image_url = gerar_png_tabela_faturamento(
        dados=dados,
        titulo="Faturamento de Filiais",
        data_inicio=intent.get("data_inicio"),
        data_fim=intent.get("data_fim"),
        tipo_nome="filial",
    )

    return {
        "success": True,
        "answer": "📊 Faturamento de Filiais",
        "image_url": image_url,
        "image_path": image_url,
        "intent": intent,
    }


def responder_faturamento_associacoes(intent: dict) -> dict:
    dados = buscar_faturamento_por_associacao(
        intent.get("data_inicio"),
        intent.get("data_fim"),
        intent.get("departamento"),
    )

    image_url = gerar_png_tabela_faturamento(
        dados=dados,
        titulo="Faturamento de Associações",
        data_inicio=intent.get("data_inicio"),
        data_fim=intent.get("data_fim"),
        tipo_nome="associacao",
    )

    return {
        "success": True,
        "answer": "📊 Faturamento de Associações",
        "image_url": image_url,
        "image_path": image_url,
        "intent": intent,
    }


def responder_com_intent(intent: dict) -> dict:
    modulo = intent.get("modulo")
    tipo = intent.get("tipo")

    if modulo == "faturamento_filiais" or tipo == "faturamento_filial":
        return responder_faturamento_filiais(intent)

    if modulo == "faturamento_associacoes" or tipo == "faturamento_associacao":
        return responder_faturamento_associacoes(intent)

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


def eh_followup_curto(texto: str) -> bool:
    return normalizar_texto(texto) in FOLLOWUPS_CURTOS


def aplicar_contexto_persistido(
    message: str,
    intent: dict,
    ultimo_contexto: dict | None,
) -> dict:
    if not ultimo_contexto or not ultimo_contexto.get("intent"):
        return intent

    texto = normalizar_texto(message)

    if not eh_followup_curto(texto):
        return intent

    contexto = ultimo_contexto.get("contexto") or {}
    intent_anterior = ultimo_contexto["intent"].copy()

    if intent_anterior.get("modulo") == "desconhecido":
        return intent

    intent_anterior["pergunta"] = message

    if not intent_anterior.get("tipo"):
        intent_anterior["tipo"] = contexto.get("tipo_atual")

    if intent_anterior.get("departamento") is None:
        intent_anterior["departamento"] = contexto.get("departamento_atual")
        intent_anterior["departamento_nome"] = contexto.get("departamento_nome_atual")

    if not intent_anterior.get("data"):
        intent_anterior["data"] = contexto.get("data_atual")
        intent_anterior["data_inicio"] = contexto.get("data_inicio_atual")
        intent_anterior["data_fim"] = contexto.get("data_fim_atual")

    if intent.get("data"):
        intent_anterior["data"] = intent.get("data")
        intent_anterior["data_inicio"] = intent.get("data_inicio") or intent.get("data")
        intent_anterior["data_fim"] = intent.get("data_fim") or intent.get("data")

    if "margem" in texto:
        intent_anterior["tipo"] = "margem"

    elif "meta" in texto:
        intent_anterior["tipo"] = "meta_vs_realizado"

    elif "projeção" in texto or "projecao" in texto:
        intent_anterior["tipo"] = "projecao"

    elif "faturamento" in texto:
        intent_anterior["tipo"] = "faturamento"

    if "lojas" in texto or texto in ["loja", "loja?"]:
        intent_anterior["departamento"] = 1
        intent_anterior["departamento_nome"] = "Lojas"
        intent_anterior["departamento_explicito"] = True

    elif "naturovos" in texto or "naturovo" in texto:
        intent_anterior["departamento"] = 5
        intent_anterior["departamento_nome"] = "Naturovos"
        intent_anterior["departamento_explicito"] = True

    elif "grupo" in texto:
        intent_anterior["departamento"] = 0
        intent_anterior["departamento_nome"] = "Grupo"
        intent_anterior["departamento_explicito"] = True

    intent_anterior["origem"] = "contexto_persistido"

    return intent_anterior


def registrar_contexto_valido(
    session_id: str,
    pergunta: str,
    resposta_final: dict,
    intent: dict,
    contexto_extra: dict | None = None,
    usar_contexto: bool = True,
) -> None:
    contexto = {
        "type": resposta_final.get("type"),
        "requires_selection": resposta_final.get("requires_selection", False),
        "pending_selection": resposta_final.get("requires_selection", False),
        "selection_type": resposta_final.get("selection_type"),
        "tipo_atual": intent.get("tipo"),
        "modulo_atual": intent.get("modulo"),
        "departamento_atual": intent.get("departamento"),
        "departamento_nome_atual": intent.get("departamento_nome"),
        "data_atual": intent.get("data"),
        "data_inicio_atual": intent.get("data_inicio"),
        "data_fim_atual": intent.get("data_fim"),
    }

    if contexto_extra:
        contexto.update(contexto_extra)

    if usar_contexto and session_id:
        salvar_contexto_chat(
            session_id=session_id,
            pergunta=pergunta,
            resposta=resposta_final.get("answer"),
            intent=intent,
            contexto=contexto,
        )


def processar_chat(message: str, session_id: str | None = None):
    print("MESSAGE:", message)

    if not session_id:
        return {
            "success": False,
            "type": "error",
            "answer": "session_id é obrigatório para manter o contexto da conversa.",
            "intent": None,
        }

    selecao_resolvida = resolver_selecao_pendente(message, session_id)

    if selecao_resolvida == "__SEM_CONTEXTO__":
        resposta_final = {
            "success": False,
            "type": "selection_error",
            "answer": (
                "Não encontrei uma pergunta anterior para aplicar essa opção.\n\n"
                "Digite primeiro o que deseja consultar, por exemplo:\n"
                "• Faturamento\n"
                "• Meta\n"
                "• Margem\n"
                "• Evolução\n"
                "• Faturamento de filiais\n"
                "• Faturamento de associações"
            ),
            "intent": None,
        }

        registrar_chat_log(
            session_id=session_id,
            pergunta=message,
            resposta=resposta_final["answer"],
            intent=None,
            sucesso=False,
        )

        registrar_sem_resposta(
            session_id=session_id,
            pergunta=message,
            intent=None,
            motivo=resposta_final["answer"],
        )

        return resposta_final

    if isinstance(selecao_resolvida, dict):
        resposta_final = responder_com_intent(selecao_resolvida)

        registrar_chat_log(
            session_id=session_id,
            pergunta=message,
            resposta=resposta_final.get("answer"),
            intent=selecao_resolvida,
            sucesso=resposta_final.get("success", True),
        )

        registrar_contexto_valido(
            session_id=session_id,
            pergunta=message,
            resposta_final=resposta_final,
            intent=selecao_resolvida,
            contexto_extra={
                "pending_selection": False,
                "requires_selection": False,
                "selection_type": None,
            },
        )

        return resposta_final

    ultimo_contexto = buscar_ultimo_contexto(session_id)

    intent = parse_intent_hibrido(message)

    intent = aplicar_contexto_persistido(
        message=message,
        intent=intent,
        ultimo_contexto=ultimo_contexto,
    )

    if intent.get("modulo") == "desconhecido":
        resposta_final = {
            "success": True,
            "type": "unknown",
            "answer": (
                "Não entendi sua pergunta.\n\n"
                "Você pode perguntar sobre faturamento, meta, margem, "
                "projeção, evolução, vendedores, produtos, filiais ou associações."
            ),
            "intent": intent,
        }

        registrar_chat_log(
            session_id=session_id,
            pergunta=message,
            resposta=resposta_final["answer"],
            intent=intent,
            sucesso=False,
        )

        registrar_sem_resposta(
            session_id=session_id,
            pergunta=message,
            intent=intent,
            motivo="Intent desconhecida",
        )

        return resposta_final

    if precisa_selecionar_departamento(intent):
        resposta_final = responder_selecao_departamento(
            intent=intent,
            session_id=session_id,
        )

        registrar_chat_log(
            session_id=session_id,
            pergunta=message,
            resposta=resposta_final.get("answer"),
            intent=intent,
            sucesso=resposta_final.get("success", True),
        )

        return resposta_final

    resposta_final = responder_com_intent(intent)

    registrar_chat_log(
        session_id=session_id,
        pergunta=message,
        resposta=resposta_final.get("answer"),
        intent=intent,
        sucesso=resposta_final.get("success", True),
    )

    registrar_contexto_valido(
        session_id=session_id,
        pergunta=message,
        resposta_final=resposta_final,
        intent=intent,
        usar_contexto=True,
    )

    if "Não encontrei" in resposta_final.get("answer", ""):
        registrar_sem_resposta(
            session_id=session_id,
            pergunta=message,
            intent=intent,
            motivo=resposta_final.get("answer"),
        )

    return resposta_final
