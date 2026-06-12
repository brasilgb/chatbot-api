import os
from datetime import datetime
import matplotlib.pyplot as plt

from app.modules.chat.formatters.numero_formatter import formatar_moeda, formatar_percentual


REPORT_DIR = "/app/storage/reports"
PUBLIC_PREFIX = "/storage/reports"


def gerar_png_tabela_faturamento(
    dados: list[dict],
    titulo: str,
    data_inicio: str | None = None,
    data_fim: str | None = None,
    tipo_nome: str = "filial",
) -> str | None:
    if not dados:
        return None

    os.makedirs(REPORT_DIR, exist_ok=True)

    linhas = []
    total = 0

    for idx, item in enumerate(dados, start=1):
        nome = item.get(tipo_nome) or item.get("associacao") or f"Item {idx}"
        faturamento = item.get("faturamento") or 0
        total += float(faturamento)

        linhas.append([
            idx,
            str(nome)[:35],
            formatar_moeda(faturamento),
            formatar_moeda(item.get("ticket_medio")),
            formatar_percentual(item.get("margem")),
        ])

    periodo = str(data_inicio)
    if data_fim and data_fim != data_inicio:
        periodo = f"{data_inicio} até {data_fim}"

    linhas.append([
        "",
        "TOTAL",
        formatar_moeda(total),
        "",
        "",
    ])

    colunas = ["#", "Nome", "Faturamento", "Ticket Médio", "Margem"]

    altura = max(4, len(linhas) * 0.45 + 1.8)

    fig, ax = plt.subplots(figsize=(12, altura))
    ax.axis("off")

    ax.set_title(
        f"{titulo}\nPeríodo: {periodo}",
        fontsize=18,
        fontweight="bold",
        pad=20,
    )

    tabela = ax.table(
        cellText=linhas,
        colLabels=colunas,
        cellLoc="center",
        colLoc="center",
        loc="center",
    )

    tabela.auto_set_font_size(False)
    tabela.set_fontsize(11)
    tabela.scale(1, 1.6)

    for (row, col), cell in tabela.get_celld().items():
        if row == 0:
            cell.set_text_props(weight="bold")
            cell.set_height(0.08)

        if row == len(linhas):
            cell.set_text_props(weight="bold")

        if col == 1 and row > 0:
            cell.set_text_props(ha="left")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"tabela_{tipo_nome}_{timestamp}.png"
    filepath = os.path.join(REPORT_DIR, filename)

    plt.tight_layout()
    plt.savefig(filepath, dpi=160, bbox_inches="tight")
    plt.close(fig)

    return f"{PUBLIC_PREFIX}/{filename}"