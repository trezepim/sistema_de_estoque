class Movimentacao:
    def __init__(self,
                 codigo_movimentacao:int=None,
                 codigo_produto:int=None,
                 tipo_movimentacao:str=None,
                 quantidade:float=0,
                 data_movimentacao:str=None,
                 cnpj_fornecedor:str=None,
                 motivo:str=None,
                 numero_nota:str=None
                 ):
        self.codigo_movimentacao = codigo_movimentacao
        self.codigo_produto = codigo_produto
        self.tipo_movimentacao = tipo_movimentacao
        self.quantidade = quantidade
        self.data_movimentacao = data_movimentacao
        self.cnpj_fornecedor = cnpj_fornecedor
        self.motivo = motivo
        self.numero_nota = numero_nota

    def to_string(self) -> str:
        return f"Código: {self.codigo_movimentacao} | Produto: {self.codigo_produto} | Tipo: {self.tipo_movimentacao} | Qtd: {self.quantidade}"