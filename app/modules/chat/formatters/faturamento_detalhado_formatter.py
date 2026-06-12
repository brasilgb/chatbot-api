from app.modules.chat.formatters.numero_formatter import (
    formatar_moeda,
    formatar_percentual,
)


def formatar_tabela_associacoes(dados, data_inicio=None, data_fim=None):
    if not dados:
        return "Não encontrei faturamento por associação para o período solicitado."

    periodo = str(data_inicio)
    if data_fim and data_fim != data_inicio:
        periodo = f"{data_inicio} até {data_fim}"

    linhas = [
        "📊 Faturamento por Associação",
        f"Período: {periodo}",
        "",
    ]

    for item in dados:
        associacao = item.get("associacao") or "Sem associação"
        faturamento = formatar_moeda(item.get("faturamento"))
        margem = formatar_percentual(item.get("margem"))
        ticket = formatar_moeda(item.get("ticket_medio"))
        juros = formatar_moeda(item.get("juros"))

        linhas.append(f"🏷️ {associacao}")
        linhas.append(f"Faturamento: {faturamento}")
        linhas.append(f"Margem: {margem}")
        linhas.append(f"Ticket médio: {ticket}")
        linhas.append(f"Juros: {juros}")
        linhas.append("")

    return "\n".join(linhas).strip()


def formatar_tabela_filiais(dados, data_inicio=None, data_fim=None):
    if not dados:
        return "Não encontrei faturamento por filial para o período solicitado."

    periodo = str(data_inicio)
    if data_fim and data_fim != data_inicio:
        periodo = f"{data_inicio} até {data_fim}"

    linhas = [
        "📊 Faturamento por Filial",
        f"Período: {periodo}",
        "",
    ]

    for item in dados:
        filial = item.get("filial") or f"Filial {item.get('id_filial')}"
        faturamento = formatar_moeda(item.get("faturamento"))
        margem = formatar_percentual(item.get("margem"))
        ticket = formatar_moeda(item.get("ticket_medio"))
        juros = formatar_moeda(item.get("juros"))

        linhas.append(f"🏬 {filial}")
        linhas.append(f"Faturamento: {faturamento}")
        linhas.append(f"Margem: {margem}")
        linhas.append(f"Ticket médio: {ticket}")
        linhas.append(f"Juros: {juros}")
        linhas.append("")

    return "\n".join(linhas).strip()