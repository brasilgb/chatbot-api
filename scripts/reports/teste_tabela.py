from app.modules.reports.table_image import gerar_tabela_ranking_vendedores


dados = [
    {"Posição": 1, "Vendedor": "João Silva", "Total": "R$ 125.430,50"},
    {"Posição": 2, "Vendedor": "Maria Souza", "Total": "R$ 98.210,00"},
    {"Posição": 3, "Vendedor": "Carlos Lima", "Total": "R$ 76.850,75"},
    {"Posição": 4, "Vendedor": "Ana Paula", "Total": "R$ 54.900,20"},
    {"Posição": 5, "Vendedor": "Pedro Santos", "Total": "R$ 41.300,00"},
]

caminho = gerar_tabela_ranking_vendedores(
    dados,
    "Ranking de Vendedores - 05/05/2026"
)

print("Imagem gerada em:", caminho)