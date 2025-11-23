from model.produtos import Produto
from conexion.mongodb_connection import MongoDBConnection
from datetime import datetime

class Controller_Produto:
    def __init__(self):
        self.db = MongoDBConnection().connect()
        self.col_prod = self.db["produtos"]
        self.col_cat = self.db["categorias"]
        self.col_loc = self.db["localizacoes"]
        self.col_mov = self.db["movimentacoes"]

    def _get_next_codigo(self) -> int:
        """Retorna o próximo código sequencial (_id)"""
        last = self.col_prod.find_one(sort=[("_id", -1)])
        if not last:
            return 1
        return int(last["_id"]) + 1

    def verifica_existencia_produto(self, codigo: int) -> bool:
        """Retorna True se o produto NÃO existe"""
        return self.col_prod.find_one({"_id": int(codigo)}) is None

    def inserir_produto(self) -> Produto:
        """Insere um novo produto no MongoDB"""

        codigo = self._get_next_codigo()
        descricao = input("Descrição do Produto: ")

        try:
            quantidade_minima = float(input("Quantidade Mínima: "))
            quantidade_maxima = float(input("Quantidade Máxima: "))
            preco_custo = float(input("Preço de Custo: "))
            preco_venda = float(input("Preço de Venda: "))
        except ValueError:
            print("Valor numérico inválido.")
            return None

        print("\nCategorias disponíveis:")
        for cat in self.col_cat.find().sort("_id", 1):
            print(f"Código: {cat['_id']} | Nome: {cat['nome_categoria']}")

        try:
            codigo_categoria = int(input("\nCódigo da Categoria: "))
        except ValueError:
            print("Código inválido.")
            return None

        if not self.col_cat.find_one({"_id": codigo_categoria}):
            print("Categoria não encontrada!")
            return None

        print("\nLocalizações disponíveis:")
        for loc in self.col_loc.find().sort("_id", 1):
            print(f"Código: {loc['_id']} | Nome: {loc['nome_localizacao']}")

        try:
            codigo_localizacao = int(input("\nCódigo da Localização: "))
        except ValueError:
            print("Código inválido.")
            return None

        if not self.col_loc.find_one({"_id": codigo_localizacao}):
            print("Localização não encontrada!")
            return None

        prod_doc = {
            "_id": codigo,
            "descricao_produto": descricao,
            "quantidade_atual": 0,
            "quantidade_minima": quantidade_minima,
            "quantidade_maxima": quantidade_maxima,
            "preco_custo": preco_custo,
            "preco_venda": preco_venda,
            "codigo_categoria": codigo_categoria,
            "codigo_localizacao": codigo_localizacao,
            "data_ultima_movimentacao": None
        }

        self.col_prod.insert_one(prod_doc)

        novo_produto = Produto(**prod_doc)
        print("\nProduto cadastrado com sucesso!")
        print(novo_produto.to_string())
        return novo_produto

    def atualizar_produto(self) -> Produto:
        """Atualiza um produto já existente"""

        try:
            codigo = int(input("Código do Produto que deseja alterar: "))
        except ValueError:
            print("Código inválido.")
            return None

        produto = self.col_prod.find_one({"_id": codigo})
        if not produto:
            print("Produto não encontrado!")
            return None

        print("\nDados atuais:")
        print(produto)

        descricao = input("\nDescrição do Produto (nova): ")

        try:
            quantidade_minima = float(input("Quantidade Mínima (nova): "))
            quantidade_maxima = float(input("Quantidade Máxima (nova): "))
            preco_custo = float(input("Preço de Custo (novo): "))
            preco_venda = float(input("Preço de Venda (novo): "))
        except ValueError:
            print("Valor numérico inválido.")
            return None

        print("\nCategorias disponíveis:")
        for cat in self.col_cat.find().sort("_id", 1):
            print(f"Código: {cat['_id']} | Nome: {cat['nome_categoria']}")
        codigo_categoria = int(input("\nCódigo da Categoria (nova): "))
        if not self.col_cat.find_one({"_id": codigo_categoria}):
            print("Categoria não encontrada!")
            return None

        print("\nLocalizações disponíveis:")
        for loc in self.col_loc.find().sort("_id", 1):
            print(f"Código: {loc['_id']} | Nome: {loc['nome_localizacao']}")
        codigo_localizacao = int(input("\nCódigo da Localização (nova): "))
        if not self.col_loc.find_one({"_id": codigo_localizacao}):
            print("Localização não encontrada!")
            return None

        self.col_prod.update_one(
            {"_id": codigo},
            {"$set": {
                "descricao_produto": descricao,
                "quantidade_minima": quantidade_minima,
                "quantidade_maxima": quantidade_maxima,
                "preco_custo": preco_custo,
                "preco_venda": preco_venda,
                "codigo_categoria": codigo_categoria,
                "codigo_localizacao": codigo_localizacao
            }}
        )

        prod_atualizado = self.col_prod.find_one({"_id": codigo})
        produto_obj = Produto(**prod_atualizado)

        print("\nProduto atualizado com sucesso!")
        print(produto_obj.to_string())
        return produto_obj

    def excluir_produto(self):
        """Exclui um produto se não houver movimentações"""

        try:
            codigo = int(input("Código do Produto que deseja excluir: "))
        except ValueError:
            print("Código inválido.")
            return

        produto = self.col_prod.find_one({"_id": codigo})
        if not produto:
            print("Produto não encontrado!")
            return

        mov_count = self.col_mov.count_documents({"codigo_produto": codigo})
        if mov_count > 0:
            print("\nNão é possível excluir: existem movimentações relacionadas.")
            return

        self.col_prod.delete_one({"_id": codigo})

        produto_obj = Produto(**produto)

        print("\nProduto excluído com sucesso!")
        print(produto_obj.to_string())

