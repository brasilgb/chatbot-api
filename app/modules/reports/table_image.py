import os
from datetime import datetime

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import pandas as pd
import matplotlib.pyplot as plt


def gerar_tabela_ranking_vendedores(
    dados: list[dict], titulo: str = "Ranking de Vendedores"
) -> str:
    os.makedirs("storage/reports", exist_ok=True)

    df = pd.DataFrame(dados)

    fig, ax = plt.subplots(figsize=(7, 3.8))
    ax.axis("off")

    tabela = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc="center",
        loc="center",
    )

    tabela.auto_set_font_size(False)
    tabela.set_fontsize(8)
    tabela.scale(1, 1.2)

    for (row, col), cell in tabela.get_celld().items():
        if row == 0:
            cell.set_text_props(weight="bold", color="white")
            cell.set_facecolor("#2563EB")
        else:
            cell.set_facecolor("#F3F4F6" if row % 2 == 0 else "#FFFFFF")

    ax.set_title(titulo, fontsize=16, fontweight="bold", pad=20)

    nome_arquivo = f"ranking_vendedores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    caminho = f"storage/reports/{nome_arquivo}"

    plt.savefig(caminho, dpi=120, bbox_inches="tight", pad_inches=0.5)
    plt.close()

    return f"/storage/reports/{nome_arquivo}"
