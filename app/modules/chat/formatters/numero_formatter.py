from decimal import Decimal
from datetime import datetime, date


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


def formatar_data(valor) -> str:
    if valor is None:
        return ""

    if isinstance(valor, datetime):
        return valor.strftime("%d/%m/%Y")

    if isinstance(valor, date):
        return valor.strftime("%d/%m/%Y")

    try:
        return datetime.strptime(str(valor), "%Y-%m-%d").strftime("%d/%m/%Y")
    except Exception:
        return str(valor)