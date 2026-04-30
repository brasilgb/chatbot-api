from app.modules.chat.intent_parser import parse_intent
from app.modules.lojas.faturamento.service import (
    resumo_faturamento,
    faturamento_filiais,
    faturamento_vendedores,
    faturamento_produtos,
)
from app.modules.chat.repository import salvar_chat_log
from app.modules.chat.ollama_service import reescrever_resposta

def format_money(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


async def process_chat(message: str) -> dict:
    intent = parse_intent(message)

    if intent["modulo"] != "faturamento":
        answer = "Ainda não entendi essa pergunta."

        salvar_chat_log(
            pergunta=message,
            intent=intent,
            resposta=answer,
            sucesso=False,
        )

        return {
            "success": False,
            "answer": answer,
            "intent": intent,
        }

    data = intent["data"]

    if intent["tipo"] == "resumo":
        result = resumo_faturamento(data)

        total = result.get("total_faturamento", 0)
        notas = result.get("quantidade_notas", 0)

        answer_base = f"O faturamento do dia {data} foi de {format_money(total)} em {notas} notas."

        answer = reescrever_resposta(message, answer_base)

        salvar_chat_log(
            pergunta=message,
            intent=intent,
            resposta=answer,
            sucesso=True,
        )

        return {
            "success": True,
            "answer": answer,
            "intent": intent,
        }

    if intent["tipo"] == "filiais":
        rows = faturamento_filiais(data)

        linhas = [f"Faturamento por filial em {data}:"]

        for item in rows[:10]:
            filial = item.get("filial", "N/D")
            total = item.get("total_faturamento", 0)

            linhas.append(f"Filial {filial}: {format_money(total)}")

        answer_base = "\n".join(linhas)

        answer = reescrever_resposta(message, answer_base)

        salvar_chat_log(
            pergunta=message,
            intent=intent,
            resposta=answer,
            sucesso=True,
        )

        return {
            "success": True,
            "answer": answer,
            "intent": intent,
        }

    if intent["tipo"] == "vendedores":
        rows = faturamento_vendedores(data)

        linhas = [f"Faturamento por vendedor em {data}:"]

        for item in rows[:10]:
            vendedor = item.get("codigo_vendedor", "N/D")
            total = item.get("total_faturamento", 0)

            linhas.append(f"{vendedor}: {format_money(total)}")

        answer_base = "\n".join(linhas)

        answer = reescrever_resposta(message, answer_base)

        salvar_chat_log(
            pergunta=message,
            intent=intent,
            resposta=answer,
            sucesso=True,
        )

        return {
            "success": True,
            "answer": answer,
            "intent": intent,
        }

    if intent["tipo"] == "produtos":
        rows = faturamento_produtos(data)

        linhas = [f"Produtos mais vendidos em {data}:"]

        for item in rows[:10]:
            produto = item.get("produto", "N/D")
            quantidade = item.get("quantidade", 0)
            total = item.get("total_faturamento", 0)

            linhas.append(f"{produto}: {quantidade} unidades - {format_money(total)}")

        answer_base = "\n".join(linhas)

        answer = reescrever_resposta(message, answer_base)

        salvar_chat_log(
            pergunta=message,
            intent=intent,
            resposta=answer,
            sucesso=True,
        )

        return {
            "success": True,
            "answer": answer,
            "intent": intent,
        }

    return {
        "success": False,
        "answer": f"Tipo '{intent['tipo']}' ainda não conectado.",
        "intent": intent,
    }
