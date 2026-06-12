import os
import uuid
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt


STORAGE_DIR = "storage/chatbot/tabelas"
PUBLIC_PREFIX = "/storage/chatbot/tabelas"


def gerar_imagem_tabela(
    titulo: str,
    dados: list[dict],
    colunas: list[str],
    nomes_colunas: list[str],
    nome_base: str = "tabela",
) -> str | None:
    if not dados:
        return None

    os.makedirs(STORAGE_DIR, exist_ok=True)

    linhas = [
        [item.get(coluna, "") for coluna in colunas]
        for item in dados
    ]

    df = pd.DataFrame(linhas, columns=nomes_colunas)

    altura = max(2.5, min(12, 1.2 + (len(df) * 0.45)))
    largura = max(8, len(nomes_colunas) * 2.3)

    fig, ax = plt.subplots(figsize=(largura, altura))
    ax.axis("off")

    ax.set_title(titulo, fontsize=16, fontweight="bold", pad=18)

    tabela = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc="center",
        loc="center",
    )

    tabela.auto_set_font_size(False)
    tabela.set_fontsize(10)
    tabela.scale(1, 1.4)

    for (row, col), cell in tabela.get_celld().items():
        cell.set_edgecolor("#D1D5DB")

        if row == 0:
            cell.set_text_props(weight="bold", color="white")
            cell.set_facecolor("#0F172A")
        else:
            cell.set_facecolor("#F8FAFC" if row % 2 == 0 else "#FFFFFF")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{nome_base}_{timestamp}_{uuid.uuid4().hex[:8]}.png"
    filepath = os.path.join(STORAGE_DIR, filename)

    plt.tight_layout()
    plt.savefig(filepath, dpi=180, bbox_inches="tight")
    plt.close(fig)

    return f"{PUBLIC_PREFIX}/{filename}"