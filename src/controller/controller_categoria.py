from model.categorias import Categoria
from conexion.mongodb_connection import MongoDBConnection

class Controller_Categoria:
    def __init__(self):
        self.db = MongoDBConnection().connect()
        self.collection = self.db["categorias"]

    def inserir_categoria(self) -> Categoria:
        codigo = int(input("Código (Novo): "))
        nome = input("Nome (Novo): ")
        descricao = input("Descrição (Nova): ")

        if self.collection.find_one({"_id": codigo}):
            print("❌ Já existe uma categoria com esse código!")
            return None

        self.collection.insert_one({
            "_id": codigo,
            "nome": nome,
            "descricao": descricao
        })

        nova_categoria = Categoria(codigo, nome, descricao)
        print("✔ Categoria inserida com sucesso!")
        print(nova_categoria.to_string())
        return nova_categoria

    def atualizar_categoria(self) -> Categoria:
        codigo = int(input("Código da categoria que deseja alterar: "))

        categoria = self.collection.find_one({"_id": codigo})
        if not categoria:
            print("❌ Categoria não encontrada!")
            return None

        nome = input("Nome (Novo): ")
        descricao = input("Descrição (Nova): ")

        self.collection.update_one(
            {"_id": codigo},
            {"$set": {"nome": nome, "descricao": descricao}}
        )

        categoria_atualizada = Categoria(codigo, nome, descricao)
        print("✔ Categoria atualizada!")
        print(categoria_atualizada.to_string())
        return categoria_atualizada

    def excluir_categoria(self):
        codigo = int(input("Código da categoria que deseja excluir: "))

        categoria = self.collection.find_one({"_id": codigo})
        if not categoria:
            print("❌ Categoria não encontrada!")
            return

        self.collection.delete_one({"_id": codigo})
        print("✔ Categoria excluída com sucesso!")

