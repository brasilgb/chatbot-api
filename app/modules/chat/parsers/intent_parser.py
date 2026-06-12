from app.modules.chat.parsers.date_parser import parse_data, parse_periodo
from app.modules.chat.services.intent_vector_service import (
    buscar_intent_semantica,
)


def pergunta_tem_contexto_negocio(message: str) -> bool:
    texto = message.lower()

    palavras_validas = [
        "meta",
        "realizado",
        "atingido",
        "alcançada",
        "alcancada",
        "evolução",
        "evolucao",
        "gráfico",
        "grafico",
        "margem",
        "projeção",
        "projecao",
        "faturamento",
        "vendeu",
        "venda",
        "vendas",
        "resumo",
        "grupo",
        "lojas",
        "loja",
        "naturovos",
        "naturovo",
        "filial",
        "filiais",
        "vendedor",
        "vendedores",
        "produto",
        "produtos",
        "associação",
        "associacao",
        "associações",
        "associacoes",
        "ranking",
        "tabela",
        "tabelas",
    ]

    return any(p in texto for p in palavras_validas)


def detectar_faturamento_tabelas(texto: str) -> dict | None:
    texto = texto.lower().strip()

    if any(
        p in texto
        for p in [
            "filiais",
            "faturamento de filiais",
            "faturamento por filial",
            "faturamento por filiais",
            "faturamento filial",
            "faturamento filiais",
            "por filial",
            "tabela filiais",
            "tabela de filiais",
        ]
    ):
        return {
            "modulo": "faturamento_filiais",
            "tipo": "faturamento_filial",
        }

    if any(
        p in texto
        for p in [
            "associações",
            "associacoes",
            "faturamento de associações",
            "faturamento de associacoes",
            "faturamento por associação",
            "faturamento por associacao",
            "faturamento por associações",
            "faturamento por associacoes",
            "faturamento associação",
            "faturamento associacao",
            "faturamento associações",
            "faturamento associacoes",
            "por associação",
            "por associacao",
            "tabela associações",
            "tabela associacoes",
            "tabela de associações",
            "tabela de associacoes",
        ]
    ):
        return {
            "modulo": "faturamento_associacoes",
            "tipo": "faturamento_associacao",
        }

    return None


def detectar_departamento(message: str) -> tuple[int | None, str | None]:
    texto = message.lower()

    if "grupo solar" in texto or "grupo" in texto:
        return 0, "Grupo Solar"

    if "naturovos" in texto or "naturovo" in texto:
        return 5, "Naturovos"

    if "lojas" in texto or "loja" in texto:
        return 1, "Lojas"

    return None, None


def detectar_tipo(message: str) -> str:
    texto = message.lower()

    if (
        "associação" in texto
        or "associacao" in texto
        or "associações" in texto
        or "associacoes" in texto
    ):
        return "faturamento_associacao"

    if "filial" in texto or "filiais" in texto:
        return "faturamento_filial"

    if "meta" in texto and (
        "realizado" in texto
        or "atingido" in texto
        or "alcançada" in texto
        or "alcancada" in texto
    ):
        return "meta_vs_realizado"

    if (
        "evolução" in texto
        or "evolucao" in texto
        or "gráfico" in texto
        or "grafico" in texto
    ):
        return "evolucao"

    if "margem" in texto:
        return "margem"

    if "projeção" in texto or "projecao" in texto:
        return "projecao"

    if (
        "faturamento" in texto
        or "vendeu" in texto
        or "venda" in texto
        or "vendas" in texto
    ):
        return "faturamento"

    if "resumo" in texto:
        return "resumo"

    return "ultimo"


def intent_desconhecida(message: str, data, data_inicio, data_fim) -> dict:
    return {
        "modulo": "desconhecido",
        "tipo": "desconhecido",
        "departamento": None,
        "departamento_nome": None,
        "departamento_explicito": False,
        "data": data,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "pergunta": message,
    }


def parse_intent(message: str) -> dict:
    data = parse_data(message)
    data_inicio, data_fim = parse_periodo(message)

    if data and data_inicio != data:
        texto = message.lower()

        if any(
            p in texto
            for p in [
                "hoje",
                "ontem",
                "anteontem",
            ]
        ):
            data_inicio = data
            data_fim = data

    if not pergunta_tem_contexto_negocio(message):
        return intent_desconhecida(message, data, data_inicio, data_fim)

    departamento, departamento_nome = detectar_departamento(message)

    faturamento_tabela = detectar_faturamento_tabelas(message)
    if faturamento_tabela:
        return {
            "modulo": faturamento_tabela["modulo"],
            "tipo": faturamento_tabela["tipo"],
            "departamento": departamento,
            "departamento_nome": departamento_nome,
            "departamento_explicito": departamento is not None,
            "data": data,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "pergunta": message,
        }

    tipo = detectar_tipo(message)

    return {
        "modulo": "resumo_total",
        "tipo": tipo,
        "departamento": departamento,
        "departamento_nome": departamento_nome,
        "departamento_explicito": departamento is not None,
        "data": data,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "pergunta": message,
    }


def parse_intent_hibrido(message: str) -> dict:
    intent_regras = parse_intent(message)

    if intent_regras.get("modulo") in [
        "faturamento_filiais",
        "faturamento_associacoes",
    ]:
        intent_regras["origem"] = "regras"
        intent_regras["score_vetorial"] = 0
        return intent_regras

    if intent_regras.get("modulo") == "desconhecido":
        intent_regras["origem"] = "regras"
        intent_regras["score_vetorial"] = 0
        return intent_regras

    intent_vetorial = buscar_intent_semantica(message)

    if not intent_vetorial:
        intent_regras["origem"] = "regras"
        return intent_regras

    score = intent_vetorial.get("score") or 0

    if score < 0.70 and intent_regras.get("tipo") == "ultimo":
        intent_regras["modulo"] = "desconhecido"
        intent_regras["tipo"] = "desconhecido"
        intent_regras["origem"] = "desconhecido"
        intent_regras["score_vetorial"] = score
        return intent_regras

    tipo_regras = intent_regras.get("tipo")
    tipo_vetorial = intent_vetorial.get("tipo")

    if tipo_vetorial and tipo_regras in ["ultimo", "resumo"]:
        intent_regras["tipo"] = tipo_vetorial

    intent_regras["origem"] = "hibrido"
    intent_regras["score_vetorial"] = score
    intent_regras["pergunta_base"] = intent_vetorial.get("pergunta_base")

    return intent_regras
