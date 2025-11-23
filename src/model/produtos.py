class Produto:
    def __init__(self, 
                 codigo:int=None, 
                 descricao:str=None,
                 quantidade_atual:float=0,
                 quantidade_minima:float=0,
                 quantidade_maxima:float=0,
                 preco_custo:float=0,
                 preco_venda:float=0,
                 codigo_categoria:int=None,
                 codigo_localizacao:int=None,
                 data_ultima_movimentacao:str=None
                 ):
        self.codigo = codigo
        self.descricao = descricao
        self.quantidade_atual = quantidade_atual
        self.quantidade_minima = quantidade_minima
        self.quantidade_maxima = quantidade_maxima
        self.preco_custo = preco_custo
        self.preco_venda = preco_venda
        self.codigo_categoria = codigo_categoria
        self.codigo_localizacao = codigo_localizacao
        self.data_ultima_movimentacao = data_ultima_movimentacao


    def set_codigo(self, codigo:int):
        self.codigo = codigo

    def set_descricao(self, descricao:str):
        self.descricao = descricao

    def get_codigo(self) -> int:
        return self.codigo

    def get_descricao(self) -> str:
        return self.descricao

    def to_string(self) -> str:
        return f"Código: {self.codigo} | Descrição: {self.descricao} | Qtd Atual: {self.quantidade_atual}"