from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


def detectar_periodo_temporal(texto: str) -> dict | None:
    hoje = date.today()

    if "anteontem" in texto:
        d = hoje - timedelta(days=2)
        return {
            "data": str(d),
            "data_inicio": str(d),
            "data_fim": str(d),
        }

    if "ontem" in texto:
        d = hoje - timedelta(days=1)
        return {
            "data": str(d),
            "data_inicio": str(d),
            "data_fim": str(d),
        }

    if "semana passada" in texto:
        inicio = hoje - timedelta(days=hoje.weekday() + 7)
        fim = inicio + timedelta(days=6)
        return {
            "data": str(fim),
            "data_inicio": str(inicio),
            "data_fim": str(fim),
        }

    if "mês passado" in texto or "mes passado" in texto:
        mes_passado = hoje - relativedelta(months=1)
        inicio = mes_passado.replace(day=1)
        fim = hoje.replace(day=1) - timedelta(days=1)
        return {
            "data": str(fim),
            "data_inicio": str(inicio),
            "data_fim": str(fim),
        }

    return None


def detectar_departamento_contextual(texto: str) -> dict | None:
    if "lojas" in texto or "loja" in texto:
        return {
            "departamento": 1,
            "departamento_nome": "Lojas",
            "departamento_explicito": True,
        }

    if "naturovos" in texto or "naturovo" in texto:
        return {
            "departamento": 5,
            "departamento_nome": "Naturovos",
            "departamento_explicito": True,
        }

    if "grupo" in texto or "grupo solar" in texto:
        return {
            "departamento": 0,
            "departamento_nome": "Grupo Solar",
            "departamento_explicito": True,
        }

    return None


def detectar_tipo_contextual(texto: str, tipo_atual: str | None = None) -> str:
    palavras_faturamento = ["faturamento", "venda", "vendas", "valor vendido"]
    palavras_meta = ["meta", "atingiu", "alcançou", "alcancou", "realizado"]
    palavras_margem = ["margem", "lucratividade"]
    palavras_projecao = ["projeção", "projecao", "previsto", "tendência", "tendencia"]

    if any(p in texto for p in palavras_faturamento):
        return "faturamento"

    if any(p in texto for p in palavras_meta):
        return "meta_vs_realizado"

    if any(p in texto for p in palavras_margem):
        return "margem"

    if any(p in texto for p in palavras_projecao):
        return "projecao"

    return tipo_atual or "ultimo"


def parece_followup(texto: str) -> bool:
    gatilhos = [
        "e ",
        "também",
        "tambem",
        "agora",
        "mesmo",
        "mesma",
        "ontem",
        "anteontem",
        "semana passada",
        "mês passado",
        "mes passado",
        "lojas",
        "loja",
        "naturovos",
        "naturovo",
        "grupo",
        "faturamento",
        "vendas",
        "meta",
        "margem",
        "projeção",
        "projecao",
    ]

    return any(g in texto for g in gatilhos)


def detectar_followup_contextual(message: str, context_stack: list[dict]) -> dict | None:
    texto = (message or "").strip().lower()

    if not texto or not context_stack:
        return None

    if not parece_followup(texto):
        return None

    contexto_atual = context_stack[-1]

    modulo = contexto_atual.get("modulo") or "resumo_total"
    tipo_atual = contexto_atual.get("tipo") or "ultimo"

    novo_contexto = {
        "modulo": modulo,
        "tipo": detectar_tipo_contextual(texto, tipo_atual),
        "departamento": contexto_atual.get("departamento"),
        "departamento_nome": contexto_atual.get("departamento_nome"),
        "departamento_explicito": False,
        "data": contexto_atual.get("data"),
        "data_inicio": contexto_atual.get("data_inicio"),
        "data_fim": contexto_atual.get("data_fim"),
        "pergunta": message,
        "origem": "context_router",
    }

    departamento = detectar_departamento_contextual(texto)
    if departamento:
        novo_contexto.update(departamento)

    periodo = detectar_periodo_temporal(texto)
    if periodo:
        novo_contexto.update(periodo)

    return novo_contexto