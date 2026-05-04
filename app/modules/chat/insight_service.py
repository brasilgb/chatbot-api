def gerar_alerta_variacao(variacao: float) -> str:
    if variacao <= -15:
        return "Atenção: queda relevante no faturamento."

    if variacao >= 15:
        return "Resultado positivo, acima do esperado."

    return "Variação dentro de um comportamento normal."