from conexion.mongodb_connection import MongoDBConnection

def relatorio_posicao_estoque():
    db = MongoDBConnection().connect()

    pipeline = [
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
            "$addFields": {
                "status": {
                    "$switch": {
                        "branches": [
                            {
                                "case": { "$lte": ["$quantidade_atual", "$quantidade_minima"] },
                                "then": "CRÍTICO"
                            },
                            {
                                "case": {
                                    "$lte": [
                                        "$quantidade_atual",
                                        { "$multiply": ["$quantidade_minima", 1.5] }
                                    ]
                                },
                                "then": "ALERTA"
                            }
                        ],
                        "default": "OK"
                    }
                }
            }
        },

        {
            "$project": {
                "_id": 0,
                "codigo": "$_id",
                "produto": "$descricao_produto",
                "categoria": "$categoria.nome_categoria",
                "localizacao": "$localizacao.nome_localizacao",
                "quantidade_atual": 1,
                "quantidade_minima": 1,
                "quantidade_maxima": 1,
                "status": 1,
                "preco_custo": 1,
                "preco_venda": 1,
                "data_ultima_movimentacao": 1
            }
        },

        {
            "$sort": {
                "status": 1,
                "produto": 1
            }
        }
    ]

    resultados = list(db.produtos.aggregate(pipeline))

    print("\nRELATÓRIO DE POSIÇÃO DE ESTOQUE")
    print("-" * 60)

    for r in resultados:
        print(
            f"Código: {r['codigo']} | Produto: {r['produto']} | Categoria: {r['categoria']} | "
            f"Localização: {r['localizacao']} | Atual: {r['quantidade_atual']} | "
            f"Mínima: {r['quantidade_minima']} | Máxima: {r['quantidade_maxima']} | "
            f"Status: {r['status']} | Custo: {r['preco_custo']} | Venda: {r['preco_venda']} | "
            f"Última Movimentação: {r['data_ultima_movimentacao']}"
        )

    print("-" * 60)
    print(f"Total de produtos: {len(resultados)}")

