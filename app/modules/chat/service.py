from datetime import date, datetime, timedelta

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
from app.modules.chat.intent_vector_service import detectar_intent_vetorial
from app.modules.lojas.faturamento.service import montar_dados_ranking_vendedores
from app.modules.reports.table_image import gerar_tabela_ranking_vendedores
from app.modules.lojas.faturamento.repository import get_faturamento_evolucao_periodo
from app.modules.lojas.faturamento.service import montar_dados_evolucao
from app.modules.reports.charts import gerar_grafico_evolucao_vendas


def formatar_data_br(data: str) -> str:
    try:
        return datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
    except Exception:
        return data


def format_money(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def calcular_data_anterior(data: str) -> str:
    data_obj = datetime.strptime(data, "%Y-%m-%d").date()
    return (data_obj - timedelta(days=1)).isoformat()


def finalizar_resposta(
    message: str,
    intent: dict,
    answer_base: str,
    sucesso: bool = True,
    source: str = "service",
) -> dict:
    answer = answer_base

    try:
        answer = reescrever_resposta(message, answer_base)
    except Exception as e:
        print(f"[IA DESATIVADA TEMPORARIAMENTE] {e}")
        answer = answer_base

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
        "source": source,
    }


def get_range_mes(periodo: str):
    hoje = date.today()

    if periodo == "anterior":
        primeiro_dia_mes = hoje.replace(day=1)
        ultimo_mes_anterior = primeiro_dia_mes - timedelta(days=1)

        inicio = ultimo_mes_anterior.replace(day=1)
        fim = ultimo_mes_anterior
    else:
        inicio = hoje.replace(day=1)
        fim = hoje

    return inicio, fim


async def process_chat(message: str) -> dict:
    intent = parse_intent(message) or {}
    aprendizado = procurar_aprendizado(message)

    if aprendizado and intent.get("tipo") != "vendedores":
        intent_aprendizado = aprendizado.get("intent") or {}

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
            "source": "aprendizado",
        }

    departamento = intent.get("departamento") or 1
    source = "parser"

    parser_invalido = intent.get("modulo") != "faturamento" or not intent.get("tipo")

    if parser_invalido:
        try:
            intent_vetorial = detectar_intent_vetorial(
                mensagem=message,
                departamento=departamento,
            )

            print("INTENT VETORIAL:", intent_vetorial)

            if intent_vetorial:
                intent = intent_vetorial
                departamento = intent.get("departamento") or departamento
                source = "vetorial"

        except Exception as e:
            print(f"[ERRO VETORIZAÇÃO] {e}")

    if intent.get("modulo") != "faturamento":
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
            "source": source,
        }

    data = intent.get("data")
    tipo = intent.get("tipo")
    departamento = intent.get("departamento") or departamento
    print("INTENT:", intent)
    print("TIPO:", tipo)

    if tipo == "evolucao":
        print("ENTROU NO BLOCO EVOLUCAO")

        periodo = intent.get("periodo", "atual")
        print("PERIODO:", periodo)

        inicio, fim = get_range_mes(periodo)
        print("RANGE:", inicio, fim)

        rows = get_faturamento_evolucao_periodo(
            data_inicio=str(inicio),
            data_fim=str(fim),
            departamento=departamento,
        )
        print("ROWS:", rows)

        dados = montar_dados_evolucao(rows)
        print("DADOS:", dados)

        imagem = gerar_grafico_evolucao_vendas(
            dados,
            f"Evolução de Vendas - {inicio.strftime('%d/%m')} até {fim.strftime('%d/%m')}",
        )
        print("IMAGE PATH:", imagem)

        return {
            "success": True,
            "answer": "Segue a evolução de vendas no período.",
            "intent": intent,
            "source": "parser",
            "image_path": imagem,
        }

    if tipo == "resumo":
        result = resumo_faturamento(data, departamento)

        data_anterior = calcular_data_anterior(data)
        result_anterior = resumo_faturamento(data_anterior, departamento)

        total = result.get("total_faturamento", 0)
        notas = result.get("total_notas", 0)
        total_anterior = result_anterior.get("total_faturamento", 0)

        if total_anterior > 0:
            variacao = ((total - total_anterior) / total_anterior) * 100
            tendencia = "aumentou" if variacao > 0 else "diminuiu"
            alerta = gerar_alerta_variacao(variacao)

            comparativo = (
                f"{tendencia.capitalize()} {abs(variacao):.1f}% "
                f"em relação ao dia anterior ({formatar_data_br(data_anterior)}). "
                f"{alerta}"
            )
        else:
            comparativo = (
                f"Não há dados suficientes do dia anterior "
                f"({formatar_data_br(data_anterior)}) para comparação."
            )

        answer_base = (
            f"O faturamento do dia {formatar_data_br(data)} foi de "
            f"{format_money(total)} em {notas} notas. {comparativo}"
        )

        return finalizar_resposta(message, intent, answer_base, source=source)

    if tipo == "filiais":
        rows = faturamento_filiais(data, departamento)

        linhas = [f"Ranking de filiais em {formatar_data_br(data)}:"]

        total_geral = sum(item.get("total_faturamento", 0) for item in rows)
        top = rows[0] if rows else None

        for index, item in enumerate(rows[:10], start=1):
            filial = item.get("filial_nota", "N/D")
            total = item.get("total_faturamento", 0)
            linhas.append(f"{index}. Filial {filial}: {format_money(total)}")

        destaque = ""

        if top and total_geral > 0:
            filial_top = top.get("filial_nota", "N/D")
            total_top = top.get("total_faturamento", 0)
            percentual = (total_top / total_geral) * 100

            destaque = (
                f"\n\nA filial {filial_top} liderou com "
                f"{format_money(total_top)}, representando "
                f"{percentual:.1f}% do faturamento entre as filiais listadas."
            )

        answer_base = "\n".join(linhas) + destaque

        return finalizar_resposta(message, intent, answer_base, source=source)

    if tipo == "vendedores":
        print("ENTROU NO BLOCO VENDEDORES")
        rows = faturamento_vendedores(data, departamento)

        dados = montar_dados_ranking_vendedores(rows)
        dados = dados[:10]

        imagem = gerar_tabela_ranking_vendedores(
            dados, f"Top 10 Vendedores - {formatar_data_br(data)}"
        )

        return {
            "success": True,
            "answer": f"Segue o top 10 vendedores em {formatar_data_br(data)}.",
            "intent": intent,
            "source": source,
            "image_path": imagem,
        }

    if tipo == "produtos":
        rows = faturamento_produtos(data, departamento)

        linhas = [f"Produtos mais vendidos em {formatar_data_br(data)}:"]

        for item in rows[:10]:
            produto = item.get("descricao_item", "N/D")
            quantidade = item.get("quantidade_total", 0)
            total = item.get("valor_total", 0)

            linhas.append(f"{produto}: {quantidade} unidades - {format_money(total)}")

        answer_base = "\n".join(linhas)

        return finalizar_resposta(message, intent, answer_base, source=source)

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
        "source": source,
    }
