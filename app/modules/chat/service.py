from datetime import datetime, timedelta

from app.modules.chat.intent_parser import parse_intent
from app.modules.lojas.faturamento.service import (
    resumo_faturamento,
    faturamento_filiais,
    faturamento_vendedores,
    faturamento_produtos,
)
from app.modules.chat.repository import salvar_chat_log
from app.modules.chat.ollama_service import reescrever_resposta
from app.modules.chat.aprendizado_service import procurar_aprendizado
from app.modules.chat.insight_service import gerar_alerta_variacao


def format_money(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def calcular_data_anterior(data: str) -> str:
    data_obj = datetime.strptime(data, "%Y-%m-%d").date()
    return (data_obj - timedelta(days=1)).isoformat()


def finalizar_resposta(
    message: str, intent: dict, answer_base: str, sucesso: bool = True
) -> dict:
    answer = reescrever_resposta(message, answer_base)
    # answer = answer_base
    salvar_chat_log(
        pergunta=message,
        intent=intent,
        resposta=answer,
        sucesso=sucesso,
    )

    return {
        "success": sucesso,
        "answer": answer,
        "intent": intent,
    }


async def process_chat(message: str) -> dict:
    aprendizado = procurar_aprendizado(message)

    if aprendizado:
        intent_aprendizado = aprendizado.get("intent") or {"origem": "aprendizado"}

        salvar_chat_log(
            pergunta=message,
            intent=intent_aprendizado,
            resposta=aprendizado["resposta"],
            sucesso=True,
        )

        return {
            "success": True,
            "answer": aprendizado["resposta"],
            "intent": intent_aprendizado,
        }

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
    tipo = intent["tipo"]

    if tipo == "resumo":
        result = resumo_faturamento(data)

        total = result.get("total_faturamento", 0)
        notas = result.get("quantidade_notas", 0)

        data_anterior = calcular_data_anterior(data)
        result_anterior = resumo_faturamento(data_anterior)
        total_anterior = result_anterior.get("total_faturamento", 0)

        if total_anterior > 0:
            variacao = ((total - total_anterior) / total_anterior) * 100
            tendencia = "aumentou" if variacao > 0 else "diminuiu"
            alerta = gerar_alerta_variacao(variacao)

            comparativo = (
                f"{tendencia.capitalize()} {abs(variacao):.1f}% "
                f"em relação ao dia anterior ({data_anterior}). "
                f"{alerta}"
            )
        else:
            comparativo = (
                f"Não há dados suficientes do dia anterior ({data_anterior}) "
                "para comparação."
            )

        answer_base = (
            f"O faturamento do dia {data} foi de {format_money(total)} "
            f"em {notas} notas. {comparativo}"
        )

        return finalizar_resposta(message, intent, answer_base)

    if tipo == "filiais":
        rows = faturamento_filiais(data)

        linhas = [f"Faturamento por filial em {data}:"]

        for item in rows[:10]:
            filial = item.get("filial", "N/D")
            total = item.get("total_faturamento", 0)
            linhas.append(f"Filial {filial}: {format_money(total)}")

        return finalizar_resposta(message, intent, "\n".join(linhas))

    if tipo == "vendedores":
        rows = faturamento_vendedores(data)

        linhas = [f"Faturamento por vendedor em {data}:"]

        for item in rows[:10]:
            vendedor = item.get("codigo_vendedor", "N/D")
            total = item.get("total_faturamento", 0)
            linhas.append(f"{vendedor}: {format_money(total)}")

        return finalizar_resposta(message, intent, "\n".join(linhas))

    if tipo == "produtos":
        rows = faturamento_produtos(data)

        linhas = [f"Produtos mais vendidos em {data}:"]

        for item in rows[:10]:
            produto = item.get("produto", "N/D")
            quantidade = item.get("quantidade", 0)
            total = item.get("total_faturamento", 0)

            linhas.append(f"{produto}: {quantidade} unidades - {format_money(total)}")

        return finalizar_resposta(message, intent, "\n".join(linhas))

    answer = f"Tipo '{tipo}' ainda não conectado."

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