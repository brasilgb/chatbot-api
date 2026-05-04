from app.modules.chat.ollama_service import reescrever_resposta


pergunta = "qual foi o faturamento de ontem?"

resposta_base = """
O faturamento do dia 2026-05-03 foi de R$ 120.000,00 em 35 notas.
"""

resposta = reescrever_resposta(pergunta, resposta_base)

print("Resposta base:")
print(resposta_base)

print("\nResposta IA:")
print(resposta)