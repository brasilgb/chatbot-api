import os
from decimal import Decimal, InvalidOperation

import pandas as pd
import matplotlib.pyplot as plt

STORAGE_DIR = "storage/chatbot/tabelas"
PUBLIC_PREFIX = "/storage/chatbot/tabelas"

COLUNAS_MOEDA = {
    "faturamento",
    "venda_agora",
    "venda_dia",
}

COLUNAS_PERCENTUAL = {
    "rep_faturamento",
    "projecao",
    "margem",
    "meta_alcancada",
    "juros",
    "juros_agora",
}

COLUNAS_DECIMAL = {
    "preco_medio",
}


def _to_decimal(valor):
    if valor is None or valor == "":
        return None

    try:
        return Decimal(str(valor))
    except (InvalidOperation, ValueError, TypeError):
        return None


def formatar_moeda(valor) -> str:
    numero = _to_decimal(valor)
    if numero is None:
        return "-"

    texto = f"{numero:,.2f}"
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_percentual(valor):
    numero = _to_decimal(valor)
    if numero is None:
        return "-"

    numero *= 100

    texto = f"{numero:,.2f}"

    return texto.replace(",", "X").replace(".", ",").replace("X", ".") + "%"


def formatar_decimal(valor) -> str:
    numero = _to_decimal(valor)
    if numero is None:
        return "-"

    texto = f"{numero:,.2f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_valor(coluna: str, valor):
    if coluna in COLUNAS_MOEDA:
        return formatar_moeda(valor)

    if coluna in COLUNAS_PERCENTUAL:
        return formatar_percentual(valor)

    if coluna in COLUNAS_DECIMAL:
        return formatar_decimal(valor)

    if valor is None or valor == "":
        return "-"

    return str(valor)


def obter_cor_titulo(nome_base: str, titulo: str) -> str:
    texto = f"{nome_base} {titulo}".lower()

    if "naturovos" in texto:
        return "#198754"

    if "associacao" in texto or "associação" in texto:
        return "#7C3AED"

    if "filial" in texto or "filiais" in texto:
        return "#0B5ED7"

    return "#0F172A"


def gerar_imagem_tabela(
    titulo: str,
    dados: list[dict],
    colunas: list[str],
    nomes_colunas: list[str],
    nome_base: str = "tabela",
    limite: int | None = None,
) -> str | None:
    if not dados:
        return None

    os.makedirs(STORAGE_DIR, exist_ok=True)


    if limite and len(dados) > limite:
        dados = dados[:limite]

    linhas = [
        [formatar_valor(coluna, item.get(coluna, "")) for coluna in colunas]
        for item in dados
    ]

    df = pd.DataFrame(linhas, columns=nomes_colunas)

    qtd_linhas = len(df)
    qtd_colunas = len(nomes_colunas)

    altura = max(3.5, min(14, 2.4 + (qtd_linhas * 0.45)))
    largura = max(10, qtd_colunas * 2.25)

    cor_header = obter_cor_titulo(nome_base, titulo)

    fig, ax = plt.subplots(figsize=(largura, altura))
    ax.axis("off")

    tabela = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc="center",
        loc="center",
    )

    tabela.auto_set_font_size(False)
    tabela.set_fontsize(9)
    tabela.scale(1, 1.45)

    for (row, col), cell in tabela.get_celld().items():
        cell.set_edgecolor("#CBD5E1")
        cell.set_linewidth(0.6)

        if row == 0:
            cell.set_text_props(weight="bold", color="white")
            cell.set_facecolor(cor_header)
            cell.set_height(0.065)
        else:
            cell.set_facecolor("#F8FAFC" if row % 2 == 0 else "#FFFFFF")
            cell.set_text_props(color="#0F172A")
            cell.set_height(0.055)

    
    filename = f"{nome_base}.png"
    filepath = os.path.join(STORAGE_DIR, filename)

    plt.tight_layout()
    plt.savefig(filepath, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    return f"{PUBLIC_PREFIX}/{filename}"
