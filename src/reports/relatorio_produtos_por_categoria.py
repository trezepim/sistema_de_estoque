from conexion.mongodb_connection import MongoDBConnection
from bson import ObjectId

def relatorio_produtos_por_categoria():
    # Cria conexão com o banco
    db = MongoDBConnection().connect()

    # Pipeline de agregação
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
                "categoria": "$categoria.nome_categoria",
                "codigo": "$_id",
                "produto": "$descricao_produto",
                "quantidade_atual": 1,
                "quantidade_minima": 1,
                "localizacao": "$localizacao.nome_localizacao",
                "preco_venda": 1
            }
        },

        {
            "$sort": {
                "categoria": 1,
                "produto": 1
            }
        }
    ]

    # Executa agregação
    resultados = list(db.produtos.aggregate(pipeline))

    # Exibe relatório
    print("\nRELATÓRIO DE PRODUTOS POR CATEGORIA")
    print("-" * 80)

    for r in resultados:
        print(
            f"Categoria: {r['categoria']} | Código: {r['codigo']} | Produto: {r['produto']} | "
            f"Qtd Atual: {r['quantidade_atual']} | Qtd Mínima: {r['quantidade_minima']} | "
            f"Localização: {r['localizacao']} | Preço: {r['preco_venda']}"
        )

    print("-" * 80)
    print(f"Total de registros: {len(resultados)}")
    print()

# Se quiser testar rapidamente
if __name__ == "__main__":
    relatorio_produtos_por_categoria()
