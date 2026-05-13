from app.modules.resumo_total.service import (
    buscar_ultimo_resumo,
    buscar_resumo_por_data,
    buscar_resumo_periodo,
    buscar_evolucao_faturamento,
    buscar_meta_vs_realizado,
)

from app.modules.chat.formatters.resumo_total_formatter import (
    formatar_resumo_total,
)


def responder_resumo_total(intent: dict) -> str:
    tipo = intent.get("tipo")
    data = intent.get("data")
    data_inicio = intent.get("data_inicio")
    data_fim = intent.get("data_fim")
    departamento = intent.get("departamento")

    if tipo == "evolucao":
        dados = buscar_evolucao_faturamento(
            data_inicio=data_inicio,
            data_fim=data_fim,
            departamento=departamento,
        )

        if not dados:
            return "Não encontrei dados de evolução para o período solicitado."

        linhas = ["📈 Evolução de faturamento"]

        for item in dados:
            linhas.append(
                f"{item.get('data_referencia')} - "
                f"Depto {item.get('departamento')}: "
                f"R$ {item.get('faturamento')}"
            )

        return "\n".join(linhas)

    if tipo == "meta_vs_realizado":
        dados = buscar_meta_vs_realizado(
            data=data,
            departamento=departamento,
        )

        if not dados:
            return "Não encontrei dados de meta vs realizado para essa data."

        respostas = [formatar_resumo_total(item) for item in dados]
        return "\n\n---\n\n".join(respostas)

    if data:
        lista = buscar_resumo_por_data(
            data=data,
            departamento=departamento,
        )

        if lista:
            if departamento:
                return formatar_resumo_total(lista[0])

            respostas = [formatar_resumo_total(item) for item in lista]
            return "\n\n---\n\n".join(respostas)

    dados = buscar_ultimo_resumo(departamento=departamento)
    return formatar_resumo_total(dados)
