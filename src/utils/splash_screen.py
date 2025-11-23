from utils.config import count_documents

class SplashScreen:

    def __init__(self):
        self.created_by = "Marcos Fernandes, Miguel Amm, Rafael Pim"
        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2025/2"

    def get_total_produtos(self):
        return count_documents("produtos")

    def get_total_categorias(self):
        return count_documents("categorias")

    def get_total_fornecedores(self):
        return count_documents("fornecedores")

    def get_total_localizacoes(self):
        return count_documents("localizacoes")

    def get_total_movimentacoes(self):
        return count_documents("movimentacoes")

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

