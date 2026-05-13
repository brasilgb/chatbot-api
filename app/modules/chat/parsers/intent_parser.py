from app.modules.chat.parsers.date_parser import parse_data, parse_periodo


def detectar_departamento(message: str) -> tuple[int | None, str | None]:
    texto = message.lower()

    if "naturovos" in texto or "naturovo" in texto:
        return 5, "naturovos"

    if "lojas" in texto or "loja" in texto:
        return 1, "lojas"

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
        "data": data,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "pergunta": message,
    }