from reports.relatorio_produtos import relatorio_produtos
from reports.relatorio_fornecedores import relatorio_fornecedores
from reports.relatorio_produtos_abaixo_minimo import relatorio_produtos_abaixo_minimo
from reports.relatorio_produtos_por_categoria import relatorio_produtos_por_categoria
from reports.relatorio_movimentacoes_periodo import relatorio_movimentacoes_periodo
from reports.relatorio_posicao_estoque import relatorio_posicao_estoque

class Relatorio:
    def __init__(self):
        pass

    def get_relatorio_produtos(self):
        relatorio_produtos()
        input("\nPressione Enter para sair do Relatório de Produtos")

    def get_relatorio_fornecedores(self):
        relatorio_fornecedores()
        input("\nPressione Enter para sair do Relatório de Fornecedores")

    def get_relatorio_produtos_abaixo_minimo(self):
        relatorio_produtos_abaixo_minimo()
        input("\nPressione Enter para sair do Relatório de Produtos Abaixo do Mínimo")

    def get_relatorio_produtos_por_categoria(self):
        relatorio_produtos_por_categoria()
        input("\nPressione Enter para sair do Relatório de Produtos por Categoria")

    def get_relatorio_movimentacoes_periodo(self):
        data_inicial = input("Digite a data inicial (DD/MM/YYYY): ")
        data_final = input("Digite a data final (DD/MM/YYYY): ")
        
        relatorio_movimentacoes_periodo(data_inicial, data_final)
        input("\nPressione Enter para sair do Relatório de Movimentações por Período")

    def get_relatorio_posicao_estoque(self):
        relatorio_posicao_estoque()
        input("\nPressione Enter para sair do Relatório de Posição de Estoque")

