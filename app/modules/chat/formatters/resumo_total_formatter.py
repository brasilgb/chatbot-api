from app.modules.chat.formatters.numero_formatter import (
    formatar_moeda,
    formatar_percentual,
    formatar_data,
)


def nome_departamento(departamento: int | None) -> str:
    if departamento == 1:
        return "Lojas"

    if departamento == 5:
        return "Naturovos"

    return "Grupo Solar"


def tem_valor(dados: dict, campo: str) -> bool:
    valor = dados.get(campo)
    return valor is not None


def adicionar_linha(resposta: str, label: str, valor: str) -> str:
    return resposta + f"\n{label}: {valor}"


def formatar_resumo_lojas(dados: dict) -> str:
    resposta = f"""📊 Resumo - Lojas

Data: {formatar_data(dados.get("data_referencia"))}
"""

    if tem_valor(dados, "venda_agora"):
        resposta = adicionar_linha(
            resposta,
            "Venda mês",
            formatar_moeda(dados.get("venda_agora")),
        )

    if tem_valor(dados, "venda_dia"):
        resposta = adicionar_linha(
            resposta,
            "Vendas dia",
            formatar_moeda(dados.get("venda_dia")),
        )

    if tem_valor(dados, "juros_agora"):
        resposta = adicionar_linha(
            resposta,
            "Juros dia",
            formatar_moeda(dados.get("juros_agora")),
        )

    if tem_valor(dados, "meta"):
        resposta = adicionar_linha(
            resposta,
            "Meta",
            formatar_moeda(dados.get("meta")),
        )

    if tem_valor(dados, "faturamento"):
        resposta = adicionar_linha(
            resposta,
            "Faturamento",
            formatar_moeda(dados.get("faturamento")),
        )

    if tem_valor(dados, "meta_alcancada"):
        resposta = adicionar_linha(
            resposta,
            "Meta %",
            formatar_percentual(dados.get("meta_alcancada")),
        )

    if tem_valor(dados, "margem"):
        resposta = adicionar_linha(
            resposta,
            "Margem %",
            formatar_percentual(dados.get("margem")),
        )

    if tem_valor(dados, "projecao"):
        resposta = adicionar_linha(
            resposta,
            "Projeção %",
            formatar_percentual(dados.get("projecao")),
        )

    if tem_valor(dados, "margem_media_ano"):
        resposta = adicionar_linha(
            resposta,
            "Margem média do período %",
            formatar_percentual(dados.get("margem_media_ano")),
        )

    if tem_valor(dados, "juros_medio_ano"):
        resposta = adicionar_linha(
            resposta,
            "Juro médio período %",
            formatar_percentual(dados.get("juros_medio_ano")),
        )

    return adicionar_atualizacao(resposta, dados)


def formatar_resumo_naturovos(dados: dict) -> str:
    resposta = f"""📊 Resumo - Naturovos

Data: {formatar_data(dados.get("data_referencia"))}
"""

    if tem_valor(dados, "meta"):
        resposta = adicionar_linha(
            resposta,
            "Meta",
            formatar_moeda(dados.get("meta")),
        )

    if tem_valor(dados, "faturamento"):
        resposta = adicionar_linha(
            resposta,
            "Faturamento",
            formatar_moeda(dados.get("faturamento")),
        )

    if tem_valor(dados, "preco_medio"):
        resposta = adicionar_linha(
            resposta,
            "Preço médio",
            formatar_moeda(dados.get("preco_medio")),
        )

    if tem_valor(dados, "margem"):
        resposta = adicionar_linha(
            resposta,
            "Margem %",
            formatar_percentual(dados.get("margem")),
        )

    if tem_valor(dados, "projecao"):
        resposta = adicionar_linha(
            resposta,
            "Projeção %",
            formatar_percentual(dados.get("projecao")),
        )

    return adicionar_atualizacao(resposta, dados)


def formatar_resumo_grupo(dados: dict) -> str:
    resposta = f"""📊 Resumo - Grupo Solar

Data: {formatar_data(dados.get("data_referencia"))}
"""

    if tem_valor(dados, "faturamento"):
        resposta = adicionar_linha(
            resposta,
            "Faturamento",
            formatar_moeda(dados.get("faturamento")),
        )

    return adicionar_atualizacao(resposta, dados)


def adicionar_atualizacao(resposta: str, dados: dict) -> str:
    if dados.get("atualizacao"):
        resposta += f"\n\nAtualização: {dados.get('atualizacao')}"

    return resposta


def formatar_resumo_total(dados: dict | None) -> str:
    if not dados:
        return "Não encontrei dados para o período solicitado."

    departamento = dados.get("departamento")

    if departamento == 1:
        return formatar_resumo_lojas(dados)

    if departamento == 5:
        return formatar_resumo_naturovos(dados)

    return formatar_resumo_grupo(dados)