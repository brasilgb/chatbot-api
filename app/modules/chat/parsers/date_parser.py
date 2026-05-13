from datetime import date, timedelta


def parse_data(message: str) -> str:
    texto = message.lower()
    hoje = date.today()

    if "ontem" in texto:
        return (hoje - timedelta(days=1)).isoformat()

    if "hoje" in texto:
        return hoje.isoformat()

    # padrão inicial
    return hoje.isoformat()


def parse_periodo(message: str) -> tuple[str, str]:
    texto = message.lower()
    hoje = date.today()

    if "este mês" in texto or "esse mês" in texto or "mes atual" in texto or "mês atual" in texto:
        inicio = hoje.replace(day=1)
        return inicio.isoformat(), hoje.isoformat()

    if "últimos 7 dias" in texto or "ultimos 7 dias" in texto:
        inicio = hoje - timedelta(days=7)
        return inicio.isoformat(), hoje.isoformat()

    if "últimos 30 dias" in texto or "ultimos 30 dias" in texto:
        inicio = hoje - timedelta(days=30)
        return inicio.isoformat(), hoje.isoformat()

    return hoje.isoformat(), hoje.isoformat()