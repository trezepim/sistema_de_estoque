from model.localizacoes import Localizacao
from conexion.mongodb_connection import MongoDBConnection

class Controller_Localizacao:
    def __init__(self):
        self.db = MongoDBConnection().connect()
        self.collection = self.db["localizacoes"]

    def inserir_localizacao(self) -> Localizacao:
        codigo = int(input("Código (Novo): "))
        nome = input("Nome (Novo): ")
        descricao = input("Descrição (Nova): ")

        if self.collection.find_one({"_id": codigo}):
            print(f"❌ Já existe uma localização com o código {codigo}.")
            return None

        self.collection.insert_one({
            "_id": codigo,
            "nome": nome,
            "descricao": descricao
        })

        nova_localizacao = Localizacao(codigo, nome, descricao)
        print("✔ Localização cadastrada com sucesso!")
        print(nova_localizacao.to_string())
        return nova_localizacao

    def atualizar_localizacao(self) -> Localizacao:
        codigo = int(input("Código da localização que deseja alterar: "))

        localizacao = self.collection.find_one({"_id": codigo})
        if not localizacao:
            print(f"❌ A localização com código {codigo} não existe.")
            return None

        nome = input("Nome (Novo): ")
        descricao = input("Descrição (Nova): ")

        self.collection.update_one(
            {"_id": codigo},
            {"$set": {"nome": nome, "descricao": descricao}}
        )

        localizacao_atualizada = Localizacao(codigo, nome, descricao)
        print("✔ Localização atualizada com sucesso!")
        print(localizacao_atualizada.to_string())
        return localizacao_atualizada

    def excluir_localizacao(self):
        codigo = int(input("Código da localização que deseja excluir: "))

        localizacao = self.collection.find_one({"_id": codigo})
        if not localizacao:
            print(f"❌ A localização com código {codigo} não existe.")
            return

        self.collection.delete_one({"_id": codigo})

        localizacao_excluida = Localizacao(
            localizacao["_id"],
            localizacao["nome"],
            localizacao["descricao"]
        )

        print("✔ Localização excluída com sucesso!")
        print(localizacao_excluida.to_string())

