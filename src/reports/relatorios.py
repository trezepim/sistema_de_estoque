from conexion.oracle_queries import OracleQueries
from datetime import datetime

class Relatorio:
    def __init__(self):
        with open("sql/relatorio_produtos.sql") as f:
            self.query_relatorio_produtos = f.read()

        with open("sql/relatorio_fornecedores.sql") as f:
            self.query_relatorio_fornecedores = f.read()

        with open("sql/relatorio_produtos_abaixo_minimo.sql") as f:
            self.query_relatorio_produtos_abaixo_minimo = f.read()

        with open("sql/relatorio_produtos_por_categoria.sql") as f:
            self.query_relatorio_produtos_por_categoria = f.read()

        with open("sql/relatorio_movimentacoes_periodo.sql") as f:
            self.query_relatorio_movimentacoes_periodo = f.read()

        with open("sql/relatorio_posicao_estoque.sql") as f:
            self.query_relatorio_posicao_estoque = f.read()

    def get_relatorio_produtos(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorio_produtos))
        input("Pressione Enter para Sair do Relatório de Produtos")

    def get_relatorio_fornecedores(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorio_fornecedores))
        input("Pressione Enter para Sair do Relatório de Fornecedores")

    def get_relatorio_produtos_abaixo_minimo(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorio_produtos_abaixo_minimo))
        input("Pressione Enter para Sair do Relatório de Produtos Abaixo do Mínimo")

    def get_relatorio_produtos_por_categoria(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorio_produtos_por_categoria))
        input("Pressione Enter para Sair do Relatório de Produtos por Categoria")

    def get_relatorio_movimentacoes_periodo(self):
        oracle = OracleQueries()
        oracle.connect()
        data_inicial = input("Digite a data inicial (DD/MM/YYYY): ")
        data_final = input("Digite a data final (DD/MM/YYYY): ")
        
        try:
            datetime.strptime(data_inicial, '%d/%m/%Y')
            datetime.strptime(data_final, '%d/%m/%Y')
        except ValueError:
            print("Data em formato inválido. Use DD/MM/YYYY")
            return
            
        query = self.query_relatorio_movimentacoes_periodo.replace('&data_inicial', data_inicial).replace('&data_final', data_final)
        print(oracle.sqlToDataFrame(query))
        input("Pressione Enter para Sair do Relatório de Movimentações")

    def get_relatorio_posicao_estoque(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorio_posicao_estoque))
        input("Pressione Enter para Sair do Relatório de Posição de Estoque")