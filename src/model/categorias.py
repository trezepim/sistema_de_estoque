class Categoria:
    def __init__(self,
                 codigo:int=None,
                 nome:str=None,
                 descricao:str=None
                 ):
        self.codigo = codigo
        self.nome = nome
        self.descricao = descricao

    def to_string(self) -> str:
        return f"Código: {self.codigo} | Nome: {self.nome} | Descrição: {self.descricao}"