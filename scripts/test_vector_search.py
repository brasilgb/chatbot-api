from app.rag.embeddings import gerar_embedding
from app.rag.vector_repository import buscar_embeddings_similares


def main():
    pergunta = "quanto vendeu ontem nas lojas?"

    embedding = gerar_embedding(pergunta)

    resultados = buscar_embeddings_similares(
        embedding=embedding,
        origem="intent",
        limite=5,
    )

    print(f"\nPergunta: {pergunta}\n")

    for item in resultados:
        print("ID:", item["id"])
        print("Texto:", item["texto"])
        print("Origem:", item["origem"])
        print("Similaridade:", round(item["similaridade"], 4))
        print("-" * 50)


if __name__ == "__main__":
    main()