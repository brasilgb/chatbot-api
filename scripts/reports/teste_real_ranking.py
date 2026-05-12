import sys
import os

# 👉 importante para reconhecer o "app"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.modules.lojas.faturamento.service import (
    get_ranking_vendedores,
    montar_dados_ranking_vendedores,
)
from app.modules.reports.table_image import gerar_tabela_ranking_vendedores


# 🔹 1. Buscar dados reais
rows = get_ranking_vendedores("2026-05-05", 1)

# 🔹 2. Converter formato
dados = montar_dados_ranking_vendedores(rows)

# 🔹 3. Gerar imagem
caminho = gerar_tabela_ranking_vendedores(
    dados,
    "Ranking de Vendedores - 05/05/2026"
)

print("Imagem gerada em:", caminho)