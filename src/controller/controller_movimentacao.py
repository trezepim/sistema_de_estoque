from model.movimentacoes import Movimentacao
from conexion.mongodb_connection import MongoDBConnection
from datetime import datetime

class Controller_Movimentacao:
    def __init__(self):
        self.db = MongoDBConnection().connect()
        self.col_mov = self.db["movimentacoes"]
        self.col_prod = self.db["produtos"]
        self.col_for = self.db["fornecedores"]

    def _get_next_codigo(self) -> int:
        """Retorna o próximo código sequencial para movimentacao (_id)."""
        last = self.col_mov.find_one(sort=[("_id", -1)])
        if not last:
            return 1
        return int(last["_id"]) + 1

    def verifica_existencia_movimentacao(self, codigo: int) -> bool:
        """Verifica se uma movimentação existe no banco de dados"""
        return self.col_mov.find_one({"_id": int(codigo)}) is not None

    def registrar_entrada(self) -> Movimentacao:
        """Registra uma entrada de produto no estoque"""
        codigo = self._get_next_codigo()

        print("\nProdutos disponíveis:")
        produtos_cursor = self.col_prod.find({}, {"_id": 1, "descricao_produto": 1, "quantidade_atual": 1})
        produtos = list(produtos_cursor)
        if not produtos:
            print("Nenhum produto cadastrado.")
            return None
        for p in produtos:
            print(f"Código: {p['_id']} | {p.get('descricao_produto','-')} | Qtd: {p.get('quantidade_atual',0)}")

        try:
            codigo_produto = int(input("\nCódigo do Produto: "))
        except ValueError:
            print("Código inválido.")
            return None

        produto = self.col_prod.find_one({"_id": codigo_produto})
        if not produto:
            print("Produto não encontrado!")
            return None

        try:
            quantidade = float(input("Quantidade: "))
        except ValueError:
            print("Quantidade inválida.")
            return None

        print("\nFornecedores disponíveis:")
        fornecedores_cursor = self.col_for.find({}, {"_id": 1, "razao_social": 1})
        fornecedores = list(fornecedores_cursor)
        for f in fornecedores:
            print(f"CNPJ: {f['_id']} | {f.get('razao_social','-')}")

        cnpj_fornecedor = input("\nCNPJ do Fornecedor (ou deixe vazio se não houver): ").strip() or None
        if cnpj_fornecedor:
            if not self.col_for.find_one({"_id": cnpj_fornecedor}):
                print("Fornecedor não encontrado!")
                return None

        numero_nota = input("Número da Nota: ")
        motivo = input("Motivo: ")

        data_mov = datetime.now()

        mov_doc = {
            "_id": int(codigo),
            "codigo_produto": int(codigo_produto),
            "tipo_movimentacao": "E",
            "quantidade": float(quantidade),
            "data_movimentacao": data_mov,
            "cnpj_fornecedor": cnpj_fornecedor,
            "motivo": motivo,
            "numero_nota": numero_nota
        }
        self.col_mov.insert_one(mov_doc)

        self.col_prod.update_one(
            {"_id": codigo_produto},
            {"$inc": {"quantidade_atual": float(quantidade)},
             "$set": {"data_ultima_movimentacao": data_mov}}
        )

        nova_movimentacao = Movimentacao(
            codigo_movimentacao=mov_doc["_id"],
            codigo_produto=mov_doc["codigo_produto"],
            tipo_movimentacao=mov_doc["tipo_movimentacao"],
            quantidade=mov_doc["quantidade"],
            data_movimentacao=mov_doc["data_movimentacao"],
            cnpj_fornecedor=mov_doc["cnpj_fornecedor"],
            motivo=mov_doc["motivo"],
            numero_nota=mov_doc["numero_nota"]
        )

        print("\nMovimentação registrada com sucesso!")
        print(nova_movimentacao.to_string())
        return nova_movimentacao

    def registrar_saida(self) -> Movimentacao:
        """Registra uma saída de produto do estoque"""
        codigo = self._get_next_codigo()

        print("\nProdutos disponíveis (com estoque):")
        produtos_cursor = self.col_prod.find({"quantidade_atual": {"$gt": 0}},
                                            {"_id":1, "descricao_produto":1, "quantidade_atual":1, "quantidade_minima":1})
        produtos = list(produtos_cursor)
        if not produtos:
            print("Nenhum produto com estoque disponível.")
            return None
        for p in produtos:
            print(f"Código: {p['_id']} | {p.get('descricao_produto','-')} | Qtd: {p.get('quantidade_atual',0)} | Mín: {p.get('quantidade_minima',0)}")

        try:
            codigo_produto = int(input("\nCódigo do Produto: "))
        except ValueError:
            print("Código inválido.")
            return None

        produto = self.col_prod.find_one({"_id": codigo_produto})
        if not produto:
            print("Produto não encontrado!")
            return None

        try:
            quantidade = float(input("Quantidade: "))
        except ValueError:
            print("Quantidade inválida.")
            return None

        qtd_atual = float(produto.get("quantidade_atual", 0))
        if qtd_atual < quantidade:
            print(f"Quantidade insuficiente. Disponível: {qtd_atual}")
            return None

        qtd_minima = float(produto.get("quantidade_minima", 0))
        if (qtd_atual - quantidade) < qtd_minima:
            print(f"\nATENÇÃO: Esta saída deixará o produto abaixo da quantidade mínima ({qtd_minima})!")
            if input("Deseja continuar? (S/N) ").upper() != 'S':
                return None

        print("\nFornecedores disponíveis:")
        fornecedores_cursor = self.col_for.find({}, {"_id":1, "razao_social":1})
        for f in fornecedores_cursor:
            print(f"CNPJ: {f['_id']} | {f.get('razao_social','-')}")

        cnpj_fornecedor = input("\nCNPJ do Fornecedor (ou deixe vazio se não houver): ").strip() or None
        if cnpj_fornecedor and not self.col_for.find_one({"_id": cnpj_fornecedor}):
            print("Fornecedor não encontrado!")
            return None

        numero_nota = input("Número da Nota: ")
        motivo = input("Motivo: ")

        data_mov = datetime.now()

        mov_doc = {
            "_id": int(codigo),
            "codigo_produto": int(codigo_produto),
            "tipo_movimentacao": "S",
            "quantidade": float(quantidade),
            "data_movimentacao": data_mov,
            "cnpj_fornecedor": cnpj_fornecedor,
            "motivo": motivo,
            "numero_nota": numero_nota
        }
        self.col_mov.insert_one(mov_doc)

        self.col_prod.update_one(
            {"_id": codigo_produto},
            {"$inc": {"quantidade_atual": -float(quantidade)},
             "$set": {"data_ultima_movimentacao": data_mov}}
        )

        nova_movimentacao = Movimentacao(
            codigo_movimentacao=mov_doc["_id"],
            codigo_produto=mov_doc["codigo_produto"],
            tipo_movimentacao=mov_doc["tipo_movimentacao"],
            quantidade=mov_doc["quantidade"],
            data_movimentacao=mov_doc["data_movimentacao"],
            cnpj_fornecedor=mov_doc["cnpj_fornecedor"],
            motivo=mov_doc["motivo"],
            numero_nota=mov_doc["numero_nota"]
        )

        print("\nMovimentação registrada com sucesso!")
        print(nova_movimentacao.to_string())
        return nova_movimentacao

    def atualizar_movimentacao(self) -> Movimentacao:
        """Atualiza uma movimentação existente e ajusta o estoque"""
        try:
            codigo_movimentacao = int(input("Código da Movimentação: "))
        except ValueError:
            print("Código inválido.")
            return None

        mov = self.col_mov.find_one({"_id": codigo_movimentacao})
        if not mov:
            print("Movimentação não encontrada!")
            return None

        tipo_movimentacao = mov.get("tipo_movimentacao")
        quantidade_antiga = float(mov.get("quantidade", 0))
        codigo_produto = int(mov.get("codigo_produto"))

        try:
            quantidade = float(input("Nova Quantidade: "))
        except ValueError:
            print("Quantidade inválida.")
            return None

        motivo = input("Novo Motivo: ")
        numero_nota = input("Novo Número da Nota: ")

        self.col_mov.update_one(
            {"_id": codigo_movimentacao},
            {"$set": {
                "quantidade": quantidade,
                "motivo": motivo,
                "numero_nota": numero_nota
            }}
        )

        if tipo_movimentacao == 'E':
            diff = -quantidade_antiga + quantidade
        else:
            diff = quantidade_antiga - quantidade

        self.col_prod.update_one(
            {"_id": codigo_produto},
            {"$inc": {"quantidade_atual": float(diff)},
             "$set": {"data_ultima_movimentacao": datetime.now()}}
        )

        mov_atualizada = self.col_mov.find_one({"_id": codigo_movimentacao})

        movimentacao_atualizada = Movimentacao(
            codigo_movimentacao=mov_atualizada["_id"],
            codigo_produto=mov_atualizada["codigo_produto"],
            tipo_movimentacao=mov_atualizada["tipo_movimentacao"],
            quantidade=mov_atualizada["quantidade"],
            data_movimentacao=mov_atualizada.get("data_movimentacao"),
            cnpj_fornecedor=mov_atualizada.get("cnpj_fornecedor"),
            motivo=mov_atualizada.get("motivo"),
            numero_nota=mov_atualizada.get("numero_nota")
        )

        print("\nMovimentação atualizada com sucesso!")
        print(movimentacao_atualizada.to_string())
        return movimentacao_atualizada

