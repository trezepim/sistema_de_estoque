from model.fornecedores import Fornecedor
from conexion.mongodb_connection import MongoDBConnection

class Controller_Fornecedor:
    def __init__(self):
        self.db = MongoDBConnection().connect()
        self.collection = self.db["fornecedores"]

    def inserir_fornecedor(self) -> Fornecedor:
        cnpj = input("CNPJ (Novo): ")

        if self.collection.find_one({"_id": cnpj}):
            print(f"❌ O CNPJ {cnpj} já está cadastrado.")
            return None

        razao_social = input("Razão Social (Nova): ")
        nome_fantasia = input("Nome Fantasia (Nova): ")

        self.collection.insert_one({
            "_id": cnpj,
            "razao_social": razao_social,
            "nome_fantasia": nome_fantasia
        })

        novo_fornecedor = Fornecedor(cnpj, razao_social, nome_fantasia)
        print("✔ Fornecedor inserido com sucesso!")
        print(novo_fornecedor.to_string())
        return novo_fornecedor

    def atualizar_fornecedor(self) -> Fornecedor:
        cnpj = input("CNPJ do fornecedor que deseja atualizar: ")

        fornecedor = self.collection.find_one({"_id": cnpj})
        if not fornecedor:
            print(f"❌ O CNPJ {cnpj} não existe.")
            return None

        razao_social = input("Razão Social (Nova): ")
        nome_fantasia = input("Nome Fantasia (Nova): ")

        self.collection.update_one(
            {"_id": cnpj},
            {"$set": {
                "razao_social": razao_social,
                "nome_fantasia": nome_fantasia
            }}
        )

        fornecedor_atualizado = Fornecedor(cnpj, razao_social, nome_fantasia)
        print("✔ Fornecedor atualizado com sucesso!")
        print(fornecedor_atualizado.to_string())
        return fornecedor_atualizado

    def excluir_fornecedor(self):
        cnpj = input("CNPJ do fornecedor que deseja excluir: ")

        fornecedor = self.collection.find_one({"_id": cnpj})
        if not fornecedor:
            print(f"❌ O CNPJ {cnpj} não existe.")
            return

        self.collection.delete_one({"_id": cnpj})

        fornecedor_excluido = Fornecedor(
            fornecedor["_id"],
            fornecedor["razao_social"],
            fornecedor["nome_fantasia"]
        )

        print("✔ Fornecedor removido com sucesso!")
        print(fornecedor_excluido.to_string())

