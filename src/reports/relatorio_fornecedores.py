from conexion.mongodb_connection import MongoDBConnection

def relatorio_fornecedores():
    db = MongoDBConnection().connect()

    fornecedores = db.fornecedores.find(
        {},
        {
            "_id": 1,
            "razao_social": 1,
            "nome_fantasia": 1
        }
    ).sort("nome_fantasia", 1)

    print("\nRELATÓRIO DE FORNECEDORES")
    print("-" * 50)

    for f in fornecedores:
        print(f"CNPJ: {f['_id']} | Razão Social: {f['razao_social']} | Nome Fantasia: {f['nome_fantasia']}")
