from conexion.mongodb_connection import MongoDBConnection

def relatorio_produtos():
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
            "$project": {
                "_id": 0,
                "codigo": "$_id",
                "produto": "$descricao_produto",
                "estoque_atual": "$quantidade_atual",
                "estoque_minimo": "$quantidade_minima",
                "estoque_maximo": "$quantidade_maxima",
                "preco_custo": 1,
                "preco_venda": 1,
                "categoria": "$categoria.nome_categoria",
                "localizacao": "$localizacao.nome_localizacao",
                "ultima_movimentacao": "$data_ultima_movimentacao"
            }
        },

        { "$sort": { "produto": 1 } }
    ]

    resultados = list(db.produtos.aggregate(pipeline))

    print("\nRELATÓRIO DE PRODUTOS")
    print("-" * 60)

    for r in resultados:
        print(
            f"Código: {r['codigo']} | Produto: {r['produto']} | Atual: {r['estoque_atual']} | "
            f"Mínimo: {r['estoque_minimo']} | Máximo: {r['estoque_maximo']} | "
            f"Custo: {r['preco_custo']} | Venda: {r['preco_venda']} | "
            f"Categoria: {r['categoria']} | Localização: {r['localizacao']} | "
            f"Última Movimentação: {r['ultima_movimentacao']}"
        )

    print("-" * 60)
    print(f"Total de produtos: {len(resultados)}")

