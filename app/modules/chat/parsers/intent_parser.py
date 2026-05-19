from app.modules.chat.parsers.date_parser import parse_data, parse_periodo
from app.modules.chat.services.intent_vector_service import (
    buscar_intent_semantica,
)

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

    if "meta" in texto and ("realizado" in texto or "atingido" in texto or "alcançada" in texto):
        return "meta_vs_realizado"

    if "evolução" in texto or "evolucao" in texto or "gráfico" in texto or "grafico" in texto:
        return "evolucao"

    if "margem" in texto:
        return "margem"

    if "projeção" in texto or "projecao" in texto:
        return "projecao"

    if "faturamento" in texto or "vendeu" in texto or "venda" in texto:
        return "faturamento"

    if "resumo" in texto:
        return "resumo"

    return "ultimo"



def parse_intent(message: str) -> dict:
    departamento, departamento_nome = detectar_departamento(message)
    tipo = detectar_tipo(message)

    data = parse_data(message)
    data_inicio, data_fim = parse_periodo(message)

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

    intent_vetorial = buscar_intent_semantica(message)
    

    if not intent_vetorial:
        intent_regras["origem"] = "regras"
        return intent_regras

    tipo_regras = intent_regras.get("tipo")
    tipo_vetorial = intent_vetorial.get("tipo")

    if tipo_vetorial and tipo_regras in ["ultimo", "resumo"]:
        intent_regras["tipo"] = tipo_vetorial

    intent_regras["origem"] = "hibrido"
    intent_regras["score_vetorial"] = intent_vetorial.get("score")
    intent_regras["pergunta_base"] = intent_vetorial.get("pergunta_base")

    return intent_regras