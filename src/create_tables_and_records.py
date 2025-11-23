from conexion.mongodb_connection import MongoDBConnection
from datetime import datetime

def drop_collections(db):
    collections = [
        "categorias",
        "fornecedores",
        "localizacoes",
        "produtos",
        "movimentacoes"
    ]

    for col in collections:
        if col in db.list_collection_names():
            db[col].drop()
            print(f"Coleção '{col}' removida.")
        else:
            print(f"Coleção '{col}' não existia.")

def create_collections(db):
    collections = [
        "categorias",
        "fornecedores",
        "localizacoes",
        "produtos",
        "movimentacoes"
    ]

    for col in collections:
        if col not in db.list_collection_names():
            db.create_collection(col)
            print(f"Coleção '{col}' criada.")
        else:
            print(f"Coleção '{col}' já existe.")

def insert_sample_records(db):
    categorias = [
        {"_id": 1, "nome_categoria": "Informática", "descricao": "Produtos de TI"},
        {"_id": 2, "nome_categoria": "Escritório", "descricao": "Material de escritório"},
        {"_id": 3, "nome_categoria": "Limpeza", "descricao": "Produtos de limpeza"}
    ]
    db.categorias.insert_many(categorias)
    print("Categorias inseridas!")

    fornecedores = [
        {"_id": "12345678000190", "razao_social": "Fornec Tech LTDA", "nome_fantasia": "FornecTech"},
        {"_id": "11223344000155", "razao_social": "Comercial XYZ", "nome_fantasia": "XYZ"}
    ]
    db.fornecedores.insert_many(fornecedores)
    print("Fornecedores inseridos!")

    localizacoes = [
        {"_id": 1, "nome_localizacao": "Depósito A", "descricao": "Área central"},
        {"_id": 2, "nome_localizacao": "Sala 5", "descricao": "Armário escritório"},
        {"_id": 3, "nome_localizacao": "Galpão 2", "descricao": "Área externa"}
    ]
    db.localizacoes.insert_many(localizacoes)
    print("Localizações inseridas!")

    produtos = [
        {
            "_id": 10,
            "descricao_produto": "Cabo HDMI 2m",
            "quantidade_atual": 25,
            "quantidade_minima": 5,
            "quantidade_maxima": 100,
            "preco_custo": 12.5,
            "preco_venda": 25.0,
            "codigo_categoria": 1,
            "codigo_localizacao": 1,
            "data_ultima_movimentacao": datetime.now()
        },
        {
            "_id": 11,
            "descricao_produto": "Monitor 24''",
            "quantidade_atual": 12,
            "quantidade_minima": 2,
            "quantidade_maxima": 20,
            "preco_custo": 550.0,
            "preco_venda": 900.0,
            "codigo_categoria": 1,
            "codigo_localizacao": 3,
            "data_ultima_movimentacao": datetime.now()
        }
    ]
    db.produtos.insert_many(produtos)
    print("Produtos inseridos!")

    movimentacoes = [
        {
            "_id": 1,
            "codigo_produto": 10,
            "tipo_movimentacao": "E",
            "quantidade": 10,
            "data_movimentacao": datetime.now(),
            "cnpj_fornecedor": "12345678000190",
            "motivo": "Reposição",
            "numero_nota": "NF-001"
        },
        {
            "_id": 2,
            "codigo_produto": 10,
            "tipo_movimentacao": "S",
            "quantidade": 5,
            "data_movimentacao": datetime.now(),
            "motivo": "Venda balcão",
            "numero_nota": None
        }
    ]
    db.movimentacoes.insert_many(movimentacoes)
    print("Movimentações inseridas!")

def run():
    print("Conectando ao MongoDB...")
    db = MongoDBConnection(can_write=True).connect()

    print("\nRemovendo coleções existentes...")
    drop_collections(db)

    print("\nCriando coleções...")
    create_collections(db)

    print("\nInserindo registros iniciais...")
    insert_sample_records(db)

    print("\nProcesso concluído com sucesso!")

if __name__ == "__main__":
    run()

