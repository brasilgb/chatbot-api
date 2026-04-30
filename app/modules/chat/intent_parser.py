from app.modules.chat.date_parser import parse_date


def parse_intent(message: str) -> dict:
    text = message.lower()

    modulo = None
    tipo = "resumo"

    # Detecta tipo
    if any(word in text for word in ["filial", "filiais", "loja", "lojas"]):
        tipo = "filiais"

    elif any(word in text for word in ["vendedor", "vendedores"]):
        tipo = "vendedores"

    elif any(word in text for word in ["produto", "produtos", "item", "itens"]):
        tipo = "produtos"

    # Detecta módulo
    if any(
        word in text
        for word in [
            "faturamento",
            "venda",
            "vendas",
            "vendeu",
            "filial",
            "filiais",
            "loja",
            "lojas",
            "vendedor",
            "vendedores",
            "produto",
            "produtos",
            "item",
            "itens",
        ]
    ):
        modulo = "faturamento"

    return {
        "modulo": modulo,
        "tipo": tipo,
        "data": parse_date(message),
    }
