import os
from datetime import datetime
import matplotlib.pyplot as plt


def gerar_grafico_evolucao_vendas(dados: list[dict], titulo: str) -> str:
    os.makedirs("storage/reports", exist_ok=True)

    datas = [d["data"] for d in dados]
    valores = [d["total"] for d in dados]

    # gráfico mais compacto
    fig, ax = plt.subplots(figsize=(7, 3.5))

    # barras
    ax.bar(datas, valores)

    # título e labels menores
    ax.set_title(titulo, fontsize=11, fontweight="bold")
    ax.set_xlabel("Dias", fontsize=9)
    ax.set_ylabel("Faturamento", fontsize=9)

    # tamanho das datas
    ax.tick_params(axis="x", labelsize=8)
    ax.tick_params(axis="y", labelsize=8)

    # gira datas
    plt.xticks(rotation=45)

    # compactação visual
    plt.tight_layout(pad=0.4)

    nome_arquivo = (
        f"evolucao_vendas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.webp"
    )

    caminho = f"storage/reports/{nome_arquivo}"

    # salva comprimido
    plt.savefig(
        caminho,
        format="webp",
        dpi=110,
        bbox_inches="tight",
        pad_inches=0.05,
    )

    plt.close()

    return f"/storage/reports/{nome_arquivo}"