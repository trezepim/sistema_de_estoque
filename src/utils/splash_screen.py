from conexion.oracle_queries import OracleQueries
from utils import config

class SplashScreen:

    def __init__(self):
        # Consultas de contagem de registros - inicio
        self.qry_total_produtos = config.QUERY_COUNT.format(tabela="produtos")
        self.qry_total_categorias = config.QUERY_COUNT.format(tabela="categorias")
        self.qry_total_fornecedores = config.QUERY_COUNT.format(tabela="fornecedores")
        self.qry_total_localizacoes = config.QUERY_COUNT.format(tabela="localizacoes")
        self.qry_total_movimentacoes = config.QUERY_COUNT.format(tabela="movimentacoes")
        # Consultas de contagem de registros - fim

        # Nome(s) do(s) criador(es)
        self.created_by = "Marcos Fernandes, Rafael Pim, Miguel Amm"
        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2025/2"

    def get_total_produtos(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_produtos)["total_produtos"].values[0]

    def get_total_categorias(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_categorias)["total_categorias"].values[0]

    def get_total_fornecedores(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_fornecedores)["total_fornecedores"].values[0]

    def get_total_localizacoes(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_localizacoes)["total_localizacoes"].values[0]

    def get_total_movimentacoes(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_movimentacoes)["total_movimentacoes"].values[0]

    def get_updated_screen(self):
        total_width = 79
        return f"""
{'#' * total_width}
#{' SISTEMA DE GERENCIAMENTO DE ESTOQUE '.center(total_width-2)}#
#{''.center(total_width-2)}#
#{'TOTAL DE REGISTROS:'.center(total_width-2)}#
#{f'1 - PRODUTOS:         {str(self.get_total_produtos()).rjust(5)}'.center(total_width-2)}#
#{f'2 - CATEGORIAS:       {str(self.get_total_categorias()).rjust(5)}'.center(total_width-2)}#
#{f'3 - FORNECEDORES:     {str(self.get_total_fornecedores()).rjust(5)}'.center(total_width-2)}#
#{f'4 - LOCALIZAÇÕES:     {str(self.get_total_localizacoes()).rjust(5)}'.center(total_width-2)}#
#{f'5 - MOVIMENTAÇÕES:    {str(self.get_total_movimentacoes()).rjust(5)}'.center(total_width-2)}#
#{''.center(total_width-2)}#
#{f'CRIADO POR: {self.created_by}'.center(total_width-2)}#
#{''.center(total_width-2)}#
#{f'PROFESSOR: {self.professor}'.center(total_width-2)}#
#{''.center(total_width-2)}#
#{f'DISCIPLINA: {self.disciplina}'.center(total_width-2)}#
#{self.semestre.center(total_width-2)}#
{'#' * total_width}
        """