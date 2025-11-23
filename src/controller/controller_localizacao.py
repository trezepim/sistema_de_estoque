from model.localizacoes import Localizacao
from conexion.oracle_queries import OracleQueries

class Controller_Localizacao:
    def __init__(self):
        pass

    def inserir_localizacao(self) -> Localizacao:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        codigo = input("Código (Novo): ")
        nome = input("Nome (Novo): ")
        descricao = input("Descrição (Nova): ")

        oracle.write(f"insert into localizacoes values ({codigo}, '{nome}', '{descricao}')")
        df_localizacao = oracle.sqlToDataFrame(f"select codigo, nome, descricao from localizacoes where codigo = {codigo}")
        
        nova_localizacao = Localizacao(df_localizacao.codigo.values[0], df_localizacao.nome.values[0], df_localizacao.descricao.values[0])
        print(nova_localizacao.to_string())
        return nova_localizacao

    def atualizar_localizacao(self) -> Localizacao:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        codigo = int(input("Código da localização que deseja alterar: "))
        nome = input("Nome (Novo): ")
        descricao = input("Descrição (Nova): ")

        oracle.write(f"update localizacoes set nome = '{nome}', descricao = '{descricao}' where codigo = {codigo}")
        df_localizacao = oracle.sqlToDataFrame(f"select codigo, nome, descricao from localizacoes where codigo = {codigo}")
        
        localizacao_atualizada = Localizacao(df_localizacao.codigo.values[0], df_localizacao.nome.values[0], df_localizacao.descricao.values[0])
        print(localizacao_atualizada.to_string())
        return localizacao_atualizada

    def excluir_localizacao(self):
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        codigo = int(input("Código da localização que deseja excluir: "))
        oracle.write(f"delete from localizacoes where codigo = {codigo}")
        print("Localização excluída com sucesso!")