from decimal import Decimal


def formatar_moeda(valor) -> str:
    if valor is None:
        return "R$ 0,00"

    valor = Decimal(str(valor))

    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")

    return f"R$ {texto}"


def formatar_percentual(valor) -> str:
    if valor is None:
        return "0,00%"

    valor = Decimal(str(valor)) * 100

    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")

    return f"{texto}%"