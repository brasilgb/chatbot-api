from app.modules.chat.formatters.numero_formatter import (
    formatar_moeda,
    formatar_percentual,
)


def nome_departamento(departamento: int | None) -> str:
    if departamento == 1:
        return "Lojas"

    if departamento == 5:
        return "Naturovos"

    return "Grupo Solar"


def formatar_resumo_total(dados: dict | None) -> str:
    if not dados:
        return "Não encontrei dados para o período solicitado."

    departamento = nome_departamento(dados.get("departamento"))

    resposta = f"""📊 Resumo - {departamento}

Data: {dados.get("data_referencia")}

Meta: {formatar_moeda(dados.get("meta"))}
Faturamento: {formatar_moeda(dados.get("faturamento"))}
Projeção: {formatar_percentual(dados.get("projecao"))}
Margem: {formatar_percentual(dados.get("margem"))}
Meta alcançada: {formatar_percentual(dados.get("meta_alcancada"))}
"""

    if dados.get("preco_medio"):
        resposta += f"\nPreço médio: {formatar_moeda(dados.get('preco_medio'))}"

    if dados.get("venda_agora"):
        resposta += f"\nVenda agora: {formatar_moeda(dados.get('venda_agora'))}"

    if dados.get("atualizacao"):
        resposta += f"\n\nAtualização: {dados.get('atualizacao')}"

    return resposta
