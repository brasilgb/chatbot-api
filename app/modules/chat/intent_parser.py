import re

from app.modules.chat.date_parser import parse_date

DEPARTAMENTOS = {
    "lojas": 1,
    "loja": 1,
    "naturovos": 5,
    "naturovo": 5,
}


def normalizar_texto(texto: str) -> str:
    texto = texto.lower().strip()
    texto = re.sub(r"\s+", " ", texto)
    return texto


def detectar_departamento(pergunta: str) -> dict:
    pergunta = normalizar_texto(pergunta)

    for nome, codigo in DEPARTAMENTOS.items():
        if nome in pergunta:
            return {
                "nome": "lojas" if codigo == 1 else "naturovos",
                "codigo": codigo,
            }

    return {
        "nome": "lojas",
        "codigo": 1,
    }


def detectar_modulo(pergunta: str) -> str | None:
    pergunta = normalizar_texto(pergunta)
    score_faturamento = 0

    palavras_fortes = [
        "faturamento",
        "faturou",
        "faturar",
        "venda",
        "vendas",
        "vendeu",
        "vendido",
        "vendidos",
        "receita",
        "evolucao",
        "evolução",
    ]

    palavras_tipo = [
        "vendedor",
        "vendedores",
        "produto",
        "produtos",
        "item",
        "itens",
        "filial",
        "filiais",
        "mais vendidos",
        "ranking vendedores",
        "evolucao",
        "evolução",
    ]

    palavras_contexto = [
        "quanto",
        "resultado",
        "total",
        "valor",
        "ontem",
        "hoje",
        "dia",
        "data",
        "mês",
        "mes",
        "semana",
        "este mês",
        "este mes",
        "mês anterior",
        "mes anterior",
    ]

    for palavra in palavras_fortes:
        if palavra in pergunta:
            score_faturamento += 3

    for palavra in palavras_tipo:
        if palavra in pergunta:
            score_faturamento += 2

    for palavra in palavras_contexto:
        if palavra in pergunta:
            score_faturamento += 1

    print("PERGUNTA:", pergunta)
    print("SCORE FATURAMENTO:", score_faturamento)

    if score_faturamento >= 3:
        return "faturamento"

    return None

def detectar_tipo(pergunta: str) -> str:
    pergunta = normalizar_texto(pergunta)

    if any(p in pergunta for p in ["evolucao", "evolução"]):
        return "evolucao"

    if any(
        p in pergunta
        for p in [
            "vendedor",
            "vendedores",
            "ranking vendedores",
            "ranking de vendedores",
        ]
    ):
        return "vendedores"

    if any(
        p in pergunta
        for p in [
            "produto",
            "produtos",
            "item",
            "itens",
            "mais vendidos",
            "mais vendido",
        ]
    ):
        return "produtos"

    if any(p in pergunta for p in ["por filial", "por filiais", "filial", "filiais"]):
        return "filiais"

    return "resumo"

def detectar_periodo(pergunta: str) -> str:
    pergunta = normalizar_texto(pergunta)

    if any(
        p in pergunta
        for p in ["mês anterior", "mes anterior", "mês passado", "mes passado"]
    ):
        return "anterior"

    return "atual"


def parse_intent(pergunta: str) -> dict:
    pergunta_normalizada = normalizar_texto(pergunta)

    departamento = detectar_departamento(pergunta_normalizada)
    modulo = detectar_modulo(pergunta_normalizada)
    tipo = detectar_tipo(pergunta_normalizada)
    data = parse_date(pergunta_normalizada)
    periodo = detectar_periodo(pergunta_normalizada)

    return {
        "modulo": modulo,
        "tipo": tipo,
        "data": data,
        "periodo": periodo,
        "departamento": departamento["codigo"],
        "departamento_nome": departamento["nome"],
        "pergunta": pergunta,
    }
