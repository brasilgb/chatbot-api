from decimal import Decimal

from app.modules.chat.repositories.faturamento_repository import (
    buscar_faturamento_filiais as buscar_faturamento_por_filial,
    buscar_faturamento_associacoes as buscar_faturamento_por_associacao,
)

from app.modules.chat.services.tabela_imagem_service import gerar_imagem_tabela


def formatar_moeda(valor):
    if valor is None:
        valor = 0

    if isinstance(valor, Decimal):
        valor = float(valor)

    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_percentual(valor):
    if valor is None:
        valor = 0

    if isinstance(valor, Decimal):
        valor = float(valor)

    return f"{valor * 100:.2f}%".replace(".", ",")


def formatar_decimal(valor):
    if valor is None:
        valor = 0

    if isinstance(valor, Decimal):
        valor = float(valor)

    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def eh_naturovos(departamento):
    return int(departamento or 0) == 5


def montar_linha_base(item: dict, campo_nome: str, departamento: int | None):
    linha = {
        campo_nome: item.get(campo_nome),
        "faturamento": formatar_moeda(item.get("faturamento")),
        "rep_faturamento": formatar_percentual(item.get("rep_faturamento")),
        "projecao": formatar_percentual(item.get("projecao")),
        "margem": formatar_percentual(item.get("margem")),
        "meta": formatar_percentual(item.get("meta_alcancada")),
    }

    if eh_naturovos(departamento):
        linha["preco_medio"] = formatar_decimal(item.get("preco_medio"))
    else:
        linha["juros"] = formatar_percentual(item.get("juros"))

    return linha


def gerar_tabela_filiais(intent: dict) -> dict:
    departamento = intent.get("departamento")

    dados = buscar_faturamento_por_filial(
        data_inicio=intent.get("data_inicio"),
        data_fim=intent.get("data_fim"),
        departamento=departamento,
    )

    linhas = [
        montar_linha_base(item, "filial", departamento)
        for item in dados
    ]

    if eh_naturovos(departamento):
        colunas = ["filial", "faturamento", "rep_faturamento", "projecao", "margem", "meta", "preco_medio"]
        nomes = ["Filial", "Faturamento", "Rep. Fat.", "Projeção", "Margem", "Meta", "Preço Médio"]
    else:
        colunas = ["filial", "faturamento", "rep_faturamento", "projecao", "margem", "meta", "juros"]
        nomes = ["Filial", "Faturamento", "Rep. Fat.", "Projeção", "Margem", "Meta", "Juros"]

    imagem_url = gerar_imagem_tabela(
        titulo="",
        dados=linhas,
        colunas=colunas,
        nomes_colunas=nomes,
        nome_base="tabela_filiais",
    )

    return {
        "success": True,
        "type": "image",
        "answer": "Segue a tabela de faturamento por filial:",
        "image_url": imagem_url,
    }


def gerar_tabela_associacoes(intent: dict) -> dict:
    departamento = intent.get("departamento")

    dados = buscar_faturamento_por_associacao(
        data_inicio=intent.get("data_inicio"),
        data_fim=intent.get("data_fim"),
        departamento=departamento,
    )

    linhas = [
        montar_linha_base(item, "associacao", departamento)
        for item in dados
    ]

    if eh_naturovos(departamento):
        colunas = ["associacao", "faturamento", "rep_faturamento", "projecao", "margem", "meta", "preco_medio"]
        nomes = ["Associação", "Faturamento", "Rep. Fat.", "Projeção", "Margem", "Meta", "Preço Médio"]
    else:
        colunas = ["associacao", "faturamento", "rep_faturamento", "projecao", "margem", "meta", "juros"]
        nomes = ["Associação", "Faturamento", "Rep. Fat.", "Projeção", "Margem", "Meta", "Juros"]

    imagem_url = gerar_imagem_tabela(
        titulo="",
        dados=linhas,
        colunas=colunas,
        nomes_colunas=nomes,
        nome_base="tabela_associacoes",
    )

    return {
        "success": True,
        "type": "image",
        "answer": "Segue a tabela de faturamento por associação:",
        "image_url": imagem_url,
    }
