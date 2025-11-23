from conexion.mongodb_connection import MongoDBConnection

def relatorio_produtos_abaixo_minimo():
    db = MongoDBConnection().connect()

    pipeline = [
        {
            "$match": {
                "$expr": {
                    "$lte": ["$quantidade_atual", "$quantidade_minima"]
                }
            }
        },

        {
            "$lookup": {
                "from": "categorias",
                "localField": "codigo_categoria",
                "foreignField": "_id",
                "as": "categoria"
            }
        },
        {"$unwind": "$categoria"},

        {
            "$lookup": {
                "from": "localizacoes",
                "localField": "codigo_localizacao",
                "foreignField": "_id",
                "as": "localizacao"
            }
        },
        {"$unwind": "$localizacao"},

        {
            "$project": {
                "_id": 0,
                "codigo": "$_id",
                "produto": "$descricao_produto",
                "quantidade_atual": 1,
                "quantidade_minima": 1,
                "categoria": "$categoria.nome_categoria",
                "localizacao": "$localizacao.nome_localizacao"
            }
        },

        { "$sort": { "quantidade_atual": 1 } }
    ]

    resultados = list(db.produtos.aggregate(pipeline))

    print("\nRELATÓRIO: PRODUTOS ABAIXO DO ESTOQUE MÍNIMO")
    print("-" * 60)

    for r in resultados:
        print(
            f"Código: {r['codigo']} | Produto: {r['produto']} | "
            f"Qtd Atual: {r['quantidade_atual']} | Qtd Mínima: {r['quantidade_minima']} | "
            f"Categoria: {r['categoria']} | Localização: {r['localizacao']}"
        )

    print("-" * 60)
    print(f"Total de produtos abaixo do mínimo: {len(resultados)}")

