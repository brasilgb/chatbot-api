from app.modules.lojas.faturamento.repository import get_faturamento_evolucao_periodo
from app.modules.lojas.faturamento.service import montar_dados_evolucao
from app.modules.reports.charts import gerar_grafico_evolucao_vendas

rows = get_faturamento_evolucao_periodo(
    data_inicio="2026-05-01",
    data_fim="2026-05-05",
    departamento=1,
)

print("ROWS:", rows)

dados = montar_dados_evolucao(rows)

print("DADOS FORMATADOS:", dados)

imagem = gerar_grafico_evolucao_vendas(
    dados,
    "Evolução de Vendas - Teste"
)

print("IMAGEM:", imagem)