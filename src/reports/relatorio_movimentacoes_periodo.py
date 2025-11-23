from datetime import datetime
from conexion.mongodb_connection import MongoDBConnection

def relatorio_movimentacoes_periodo(data_inicial: str, data_final: str):
    """
    data_inicial e data_final devem vir no formato 'DD/MM/YYYY'
    """

    db = MongoDBConnection().connect()

    dt_inicio = datetime.strptime(data_inicial, "%d/%m/%Y")
    dt_fim    = datetime.strptime(data_final, "%d/%m/%Y")

    pipeline = [
        {
            "$match": {
                "data_movimentacao": {
                    "$gte": dt_inicio,
                    "$lte": dt_fim
                }
            }
        },
        {
            "$lookup": {
                "from": "produtos",
                "localField": "codigo_produto",
                "foreignField": "_id",
                "as": "produto"
            }
        },
        { "$unwind": "$produto" },

        {
            "$lookup": {
                "from": "fornecedores",
                "localField": "cnpj_fornecedor",
                "foreignField": "_id",
                "as": "fornecedor"
            }
        },
        {
            "$unwind": {
                "path": "$fornecedor",
                "preserveNullAndEmptyArrays": True
            }
        },

        {
            "$addFields": {
                "tipo": {
                    "$cond": [
                        { "$eq": ["$tipo_movimentacao", "E"] },
                        "Entrada",
                        "Saída"
                    ]
                }
            }
        },

        {
            "$project": {
                "_id": 0,
                "data": "$data_movimentacao",
                "produto": "$produto.descricao_produto",
                "tipo": "$tipo",
                "quantidade": 1,
                "fornecedor": "$fornecedor.nome_fantasia",
                "motivo": 1,
                "numero_nota": 1
            }
        },

        { "$sort": { "data": -1 } }
    ]

    resultados = list(db.movimentacoes.aggregate(pipeline))

    print("\nRELATÓRIO DE MOVIMENTAÇÕES POR PERÍODO")
    print(f"Período: {data_inicial} até {data_final}")
    print("-" * 60)

    for r in resultados:
        print(
            f"Data: {r['data']} | Produto: {r['produto']} | Tipo: {r['tipo']} | "
            f"Qtd: {r['quantidade']} | Fornecedor: {r.get('fornecedor', '—')} | "
            f"Motivo: {r['motivo']} | Nota: {r.get('numero_nota', '—')}"
        )

    print("-" * 60)
    print(f"Total de movimentações: {len(resultados)}")

