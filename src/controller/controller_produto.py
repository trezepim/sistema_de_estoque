from model.produtos import Produto
from conexion.oracle_queries import OracleQueries

class Controller_Produto:
    def __init__(self):
        pass
        
    def inserir_produto(self) -> Produto:
        '''Insere um novo produto no banco de dados'''
        
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita os dados do novo produto
        codigo = oracle.sqlToDataFrame("select nvl(max(codigo), 0) + 1 as codigo from produtos")["codigo"].values[0]
        descricao = input("Descrição do Produto: ")
        quantidade_minima = float(input("Quantidade Mínima: "))
        quantidade_maxima = float(input("Quantidade Máxima: "))
        preco_custo = float(input("Preço de Custo: "))
        preco_venda = float(input("Preço de Venda: "))
        
        # Lista categorias disponíveis
        print("\nCategorias disponíveis:")
        df_categorias = oracle.sqlToDataFrame("select codigo, nome from categorias order by codigo")
        print(df_categorias)
        codigo_categoria = int(input("\nCódigo da Categoria: "))
        
        # Lista localizações disponíveis
        print("\nLocalizações disponíveis:")
        df_localizacoes = oracle.sqlToDataFrame("select codigo, nome from localizacoes order by codigo")
        print(df_localizacoes)
        codigo_localizacao = int(input("\nCódigo da Localização: "))

        # Insere o novo produto
        oracle.write(f"""insert into produtos 
                    (codigo, descricao_produto, quantidade_atual, quantidade_minima, 
                    quantidade_maxima, preco_custo, preco_venda, codigo_categoria, 
                    codigo_localizacao, data_ultima_movimentacao)
                    values
                    ({codigo}, '{descricao}', 0, {quantidade_minima}, {quantidade_maxima},
                    {preco_custo}, {preco_venda}, {codigo_categoria}, {codigo_localizacao}, NULL)""")

        # Recupera os dados do novo produto
        df_produto = oracle.sqlToDataFrame(f"select * from produtos where codigo = {codigo}")
        
        # Cria e retorna o objeto Produto
        novo_produto = Produto(
            df_produto.codigo.values[0],
            df_produto.descricao_produto.values[0],
            df_produto.quantidade_atual.values[0],
            df_produto.quantidade_minima.values[0],
            df_produto.quantidade_maxima.values[0],
            df_produto.preco_custo.values[0],
            df_produto.preco_venda.values[0],
            df_produto.codigo_categoria.values[0],
            df_produto.codigo_localizacao.values[0],
            df_produto.data_ultima_movimentacao.values[0]
        )
        print("\nProduto cadastrado com sucesso!")
        print(novo_produto.to_string())
        return novo_produto

    def atualizar_produto(self) -> Produto:
        '''Atualiza um produto existente no banco de dados'''
        
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        codigo = int(input("Código do Produto que deseja alterar: "))

        # Verifica se o produto existe
        if not self.verifica_existencia_produto(oracle, codigo):
            # Mostra dados atuais
            df_produto = oracle.sqlToDataFrame(f"select * from produtos where codigo = {codigo}")
            print("\nDados atuais:")
            print(df_produto)

            # Solicita novos dados
            descricao = input("\nDescrição do Produto (novo): ")
            quantidade_minima = float(input("Quantidade Mínima (nova): "))
            quantidade_maxima = float(input("Quantidade Máxima (nova): "))
            preco_custo = float(input("Preço de Custo (novo): "))
            preco_venda = float(input("Preço de Venda (novo): "))
            
            # Lista categorias disponíveis
            print("\nCategorias disponíveis:")
            df_categorias = oracle.sqlToDataFrame("select codigo, nome from categorias order by codigo")
            print(df_categorias)
            codigo_categoria = int(input("\nCódigo da Categoria (novo): "))
            
            # Lista localizações disponíveis
            print("\nLocalizações disponíveis:")
            df_localizacoes = oracle.sqlToDataFrame("select codigo, nome from localizacoes order by codigo")
            print(df_localizacoes)
            codigo_localizacao = int(input("\nCódigo da Localização (novo): "))

            # Atualiza o produto
            oracle.write(f"""update produtos set 
                        descricao_produto = '{descricao}',
                        quantidade_minima = {quantidade_minima},
                        quantidade_maxima = {quantidade_maxima},
                        preco_custo = {preco_custo},
                        preco_venda = {preco_venda},
                        codigo_categoria = {codigo_categoria},
                        codigo_localizacao = {codigo_localizacao}
                        where codigo = {codigo}""")

            # Recupera os dados atualizados
            df_produto = oracle.sqlToDataFrame(f"select * from produtos where codigo = {codigo}")
            
            # Cria e retorna o objeto Produto
            produto_atualizado = Produto(
                df_produto.codigo.values[0],
                df_produto.descricao_produto.values[0],
                df_produto.quantidade_atual.values[0],
                df_produto.quantidade_minima.values[0],
                df_produto.quantidade_maxima.values[0],
                df_produto.preco_custo.values[0],
                df_produto.preco_venda.values[0],
                df_produto.codigo_categoria.values[0],
                df_produto.codigo_localizacao.values[0],
                df_produto.data_ultima_movimentacao.values[0]
            )
            print("\nProduto atualizado com sucesso!")
            print(produto_atualizado.to_string())
            return produto_atualizado
        else:
            print(f"O código {codigo} não existe.")
            return None

    def excluir_produto(self):
        '''Exclui um produto do banco de dados'''
        
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        codigo = int(input("Código do Produto que deseja excluir: "))

        # Verifica se o produto existe
        if not self.verifica_existencia_produto(oracle, codigo):
            # Verifica se existem movimentações
            df_movimentacoes = oracle.sqlToDataFrame(f"select count(*) as total from movimentacoes where codigo_produto = {codigo}")
            if df_movimentacoes["total"].values[0] > 0:
                print("\nNão é possível excluir o produto pois existem movimentações relacionadas.")
                return
            
            # Recupera os dados do produto para exibição
            df_produto = oracle.sqlToDataFrame(f"select * from produtos where codigo = {codigo}")
            
            # Remove o produto
            oracle.write(f"delete from produtos where codigo = {codigo}")
            
            # Cria objeto do produto excluído para exibição
            produto_excluido = Produto(
                df_produto.codigo.values[0],
                df_produto.descricao_produto.values[0],
                df_produto.quantidade_atual.values[0],
                df_produto.quantidade_minima.values[0],
                df_produto.quantidade_maxima.values[0],
                df_produto.preco_custo.values[0],
                df_produto.preco_venda.values[0],
                df_produto.codigo_categoria.values[0],
                df_produto.codigo_localizacao.values[0],
                df_produto.data_ultima_movimentacao.values[0]
            )
            print("\nProduto excluído com sucesso!")
            print(produto_excluido.to_string())
        else:
            print(f"O código {codigo} não existe.")

    def verifica_existencia_produto(self, oracle:OracleQueries, codigo:int=None) -> bool:
        '''Verifica se um produto existe no banco de dados'''
        df_produto = oracle.sqlToDataFrame(f"select codigo from produtos where codigo = {codigo}")
        return df_produto.empty