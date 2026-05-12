from app.modules.chat.embedding_service import gerar_embedding
from app.modules.chat.intent_vector_repository import salvar_intent_embedding


INTENTS = [
    {
        "pergunta": "Qual foi o faturamento de ontem das lojas?",
        "intent": {
            "modulo": "faturamento",
            "tipo": "resumo",
            "departamento": 1,
        },
    },
    {
        "pergunta": "Me mostre o faturamento por filial das lojas ontem",
        "intent": {
            "modulo": "faturamento",
            "tipo": "filiais",
            "departamento": 1,
        },
    },
    {
        "pergunta": "Ranking de vendedores das lojas ontem",
        "intent": {
            "modulo": "faturamento",
            "tipo": "vendedores",
            "departamento": 1,
        },
    },
    {
        "pergunta": "Produtos mais vendidos nas lojas ontem",
        "intent": {
            "modulo": "faturamento",
            "tipo": "produtos",
            "departamento": 1,
        },
    },
    {
        "pergunta": "Qual foi o faturamento de ontem da Naturovos?",
        "intent": {
            "modulo": "faturamento",
            "tipo": "resumo",
            "departamento": 5,
        },
    },
    {
        "pergunta": "Faturamento por filial da Naturovos",
        "intent": {
            "modulo": "faturamento",
            "tipo": "filiais",
            "departamento": 5,
        },
    },
    {
        "pergunta": "Vendas por vendedor da Naturovos",
        "intent": {
            "modulo": "faturamento",
            "tipo": "vendedores",
            "departamento": 5,
        },
    },
    {
        "pergunta": "Produtos vendidos da Naturovos",
        "intent": {
            "modulo": "faturamento",
            "tipo": "produtos",
            "departamento": 5,
        },
    },
]


def main():
    for item in INTENTS:
        pergunta = item["pergunta"]
        intent = item["intent"]

        embedding = gerar_embedding(pergunta)

        salvar_intent_embedding(
            pergunta_exemplo=pergunta,
            modulo=intent["modulo"],
            tipo=intent["tipo"],
            departamento=intent["departamento"],
            intent=intent,
            embedding=embedding,
        )

        print(f"OK: {pergunta}")


if __name__ == "__main__":
    main()