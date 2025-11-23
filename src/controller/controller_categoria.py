from model.categorias import Categoria
from conexion.oracle_queries import OracleQueries

class Controller_Categoria:
    def __init__(self):
        pass

    def inserir_categoria(self) -> Categoria:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        codigo = input("Código (Novo): ")
        nome = input("Nome (Novo): ")
        descricao = input("Descrição (Nova): ")

        oracle.write(f"insert into categorias values ({codigo}, '{nome}', '{descricao}')")
        df_categoria = oracle.sqlToDataFrame(f"select codigo, nome, descricao from categorias where codigo = {codigo}")
        
        nova_categoria = Categoria(df_categoria.codigo.values[0], df_categoria.nome.values[0], df_categoria.descricao.values[0])
        print(nova_categoria.to_string())
        return nova_categoria

    def atualizar_categoria(self) -> Categoria:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        codigo = int(input("Código da categoria que deseja alterar: "))
        nome = input("Nome (Novo): ")
        descricao = input("Descrição (Nova): ")

        oracle.write(f"update categorias set nome = '{nome}', descricao = '{descricao}' where codigo = {codigo}")
        df_categoria = oracle.sqlToDataFrame(f"select codigo, nome, descricao from categorias where codigo = {codigo}")
        
        categoria_atualizada = Categoria(df_categoria.codigo.values[0], df_categoria.nome.values[0], df_categoria.descricao.values[0])
        print(categoria_atualizada.to_string())
        return categoria_atualizada

    def excluir_categoria(self):
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        codigo = int(input("Código da categoria que deseja excluir: "))
        oracle.write(f"delete from categorias where codigo = {codigo}")
        print("Categoria excluída com sucesso!")