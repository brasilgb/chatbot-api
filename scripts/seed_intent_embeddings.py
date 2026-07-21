from sqlalchemy import text

from app.core.database import engine
from app.rag.embeddings import gerar_embedding


INTENTS = [
    {
        "pergunta": "como foram as vendas hoje?",
        "intent": {
            "modulo": "resumo_total",
            "tipo": "faturamento",
            "departamento": 1,
            "departamento_nome": "lojas",
        },
    },
    {
        "pergunta": "quanto entrou hoje nas lojas?",
        "intent": {
            "modulo": "resumo_total",
            "tipo": "faturamento",
            "departamento": 1,
            "departamento_nome": "lojas",
        },
    },
    {
        "pergunta": "qual o faturamento de hoje?",
        "intent": {
            "modulo": "resumo_total",
            "tipo": "faturamento",
            "departamento": 1,
            "departamento_nome": "lojas",
        },
    },
    {
        "pergunta": "qual foi o faturamento de ontem das lojas?",
        "intent": {
            "modulo": "resumo_total",
            "tipo": "faturamento",
            "departamento": 1,
            "departamento_nome": "lojas",
        },
    },
    {
        "pergunta": "me mostre o faturamento por filial das lojas ontem",
        "intent": {
            "modulo": "faturamento_filiais",
            "tipo": "faturamento_filial",
            "departamento": 1,
            "departamento_nome": "lojas",
        },
    },
    {
        "pergunta": "ranking de filiais das lojas ontem",
        "intent": {
            "modulo": "faturamento_filiais",
            "tipo": "faturamento_filial",
            "departamento": 1,
            "departamento_nome": "lojas",
        },
    },
    {
        "pergunta": "ranking por associações das lojas ontem",
        "intent": {
            "modulo": "faturamento_associacoes",
            "tipo": "faturamento_associacao",
            "departamento": 1,
            "departamento_nome": "lojas",
        },
    },
    {
        "pergunta": "faturamento por associação das lojas ontem",
        "intent": {
            "modulo": "faturamento_associacoes",
            "tipo": "faturamento_associacao",
            "departamento": 1,
            "departamento_nome": "lojas",
        },
    },
    {
        "pergunta": "ranking de vendedores das lojas ontem",
        "intent": {
            "modulo": "resumo_total",
            "tipo": "vendedores",
            "departamento": 1,
            "departamento_nome": "lojas",
        },
    },
    {
        "pergunta": "produtos mais vendidos nas lojas ontem",
        "intent": {
            "modulo": "resumo_total",
            "tipo": "produtos",
            "departamento": 1,
            "departamento_nome": "lojas",
        },
    },
    {
        "pergunta": "me mostra a projeção das lojas",
        "intent": {
            "modulo": "resumo_total",
            "tipo": "projecao",
            "departamento": 1,
            "departamento_nome": "lojas",
        },
    },
    {
        "pergunta": "me mostra a margem das lojas",
        "intent": {
            "modulo": "resumo_total",
            "tipo": "margem",
            "departamento": 1,
            "departamento_nome": "lojas",
        },
    },
    {
        "pergunta": "evolução de vendas das lojas",
        "intent": {
            "modulo": "resumo_total",
            "tipo": "evolucao",
            "departamento": 1,
            "departamento_nome": "lojas",
        },
    },

    # Naturovos
    {
        "pergunta": "qual foi o faturamento de ontem da naturovos?",
        "intent": {
            "modulo": "resumo_total",
            "tipo": "faturamento",
            "departamento": 5,
            "departamento_nome": "naturovos",
        },
    },
    {
        "pergunta": "qual o faturamento da naturovos hoje?",
        "intent": {
            "modulo": "resumo_total",
            "tipo": "faturamento",
            "departamento": 5,
            "departamento_nome": "naturovos",
        },
    },
    {
        "pergunta": "me mostra a projeção da naturovos",
        "intent": {
            "modulo": "resumo_total",
            "tipo": "projecao",
            "departamento": 5,
            "departamento_nome": "naturovos",
        },
    },
    {
        "pergunta": "faturamento por filial da naturovos",
        "intent": {
            "modulo": "faturamento_filiais",
            "tipo": "faturamento_filial",
            "departamento": 5,
            "departamento_nome": "naturovos",
        },
    },
    {
        "pergunta": "ranking de filiais da naturovos",
        "intent": {
            "modulo": "faturamento_filiais",
            "tipo": "faturamento_filial",
            "departamento": 5,
            "departamento_nome": "naturovos",
        },
    },
    {
        "pergunta": "ranking por associações da naturovos",
        "intent": {
            "modulo": "faturamento_associacoes",
            "tipo": "faturamento_associacao",
            "departamento": 5,
            "departamento_nome": "naturovos",
        },
    },
    {
        "pergunta": "faturamento por associação da naturovos",
        "intent": {
            "modulo": "faturamento_associacoes",
            "tipo": "faturamento_associacao",
            "departamento": 5,
            "departamento_nome": "naturovos",
        },
    },
    {
        "pergunta": "vendas por vendedor da naturovos",
        "intent": {
            "modulo": "resumo_total",
            "tipo": "vendedores",
            "departamento": 5,
            "departamento_nome": "naturovos",
        },
    },
    {
        "pergunta": "produtos vendidos da naturovos",
        "intent": {
            "modulo": "resumo_total",
            "tipo": "produtos",
            "departamento": 5,
            "departamento_nome": "naturovos",
        },
    },
    {
        "pergunta": "me mostra a margem da naturovos",
        "intent": {
            "modulo": "resumo_total",
            "tipo": "margem",
            "departamento": 5,
            "departamento_nome": "naturovos",
        },
    },
    {
        "pergunta": "evolução de vendas da naturovos",
        "intent": {
            "modulo": "resumo_total",
            "tipo": "evolucao",
            "departamento": 5,
            "departamento_nome": "naturovos",
        },
    },
]


def main():
    sql = text("""
        INSERT INTO intent_embeddings (
            pergunta,
            modulo,
            tipo,
            departamento,
            departamento_nome,
            embedding,
            ativo
        )
        VALUES (
            :pergunta,
            :modulo,
            :tipo,
            :departamento,
            :departamento_nome,
            :embedding,
            true
        )
    """)

    with engine.begin() as conn:
        for item in INTENTS:
            pergunta = item["pergunta"]
            intent = item["intent"]

            embedding = gerar_embedding(pergunta)

            conn.execute(sql, {
                "pergunta": pergunta,
                "modulo": intent.get("modulo"),
                "tipo": intent.get("tipo"),
                "departamento": intent.get("departamento"),
                "departamento_nome": intent.get("departamento_nome"),
                "embedding": str(embedding),
            })

            print(f"OK: {pergunta}")


if __name__ == "__main__":
    main()
