from model.movimentacoes import Movimentacao
from conexion.oracle_queries import OracleQueries
from datetime import datetime

class Controller_Movimentacao:
    def __init__(self):
        pass
        
    def verifica_existencia_movimentacao(self, oracle: OracleQueries, codigo: int) -> bool:
        """Verifica se uma movimentação existe no banco de dados"""
        return not oracle.sqlToDataFrame(f"select 1 from movimentacoes where codigo_movimentacao = {codigo}").empty

    def registrar_entrada(self) -> Movimentacao:
        '''Registra uma entrada de produto no estoque'''
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Gera novo código de movimentação
        codigo = oracle.sqlToDataFrame("select nvl(max(codigo_movimentacao), 0) + 1 as codigo from movimentacoes")["codigo"].values[0]
        
        # Lista produtos disponíveis
        print("\nProdutos disponíveis:")
        df_produtos = oracle.sqlToDataFrame("""
            select p.codigo_produto, p.descricao_produto, p.quantidade_atual, 
                   c.nome_categoria, l.nome_localizacao
            from produtos p
            join categorias c on p.codigo_categoria = c.codigo_categoria
            join localizacoes l on p.codigo_localizacao = l.codigo_localizacao
            order by p.codigo_produto""")
        print(df_produtos)
        
        codigo_produto = int(input("\nCódigo do Produto: "))
        
        # Verifica se o produto existe
        if oracle.sqlToDataFrame(f"select 1 from produtos where codigo_produto = {codigo_produto}").empty:
            print("Produto não encontrado!")
            return None
            
        quantidade = float(input("Quantidade: "))
        
        # Lista fornecedores disponíveis
        print("\nFornecedores disponíveis:")
        df_fornecedores = oracle.sqlToDataFrame("select cnpj_fornecedor, razao_social from fornecedores order by razao_social")
        print(df_fornecedores)
        
        cnpj_fornecedor = input("\nCNPJ do Fornecedor: ")
        
        # Verifica se o fornecedor existe
        if oracle.sqlToDataFrame(f"select 1 from fornecedores where cnpj_fornecedor = '{cnpj_fornecedor}'").empty:
            print("Fornecedor não encontrado!")
            return None
            
        numero_nota = input("Número da Nota: ")
        motivo = input("Motivo: ")
        
        # Registra a movimentação
        oracle.write(f"insert into movimentacoes values ({codigo}, {codigo_produto}, 'E', {quantidade}, TO_DATE('{datetime.now().strftime('%d/%m/%Y')}', 'DD/MM/YYYY'), '{cnpj_fornecedor}', '{motivo}', '{numero_nota}')")
        
        # Atualiza o estoque
        oracle.write(f"update produtos set quantidade_atual = quantidade_atual + {quantidade}, data_ultima_movimentacao = TO_DATE('{datetime.now().strftime('%d/%m/%Y')}', 'DD/MM/YYYY') where codigo_produto = {codigo_produto}")
                    
        # Recupera os dados da movimentação
        df_movimentacao = oracle.sqlToDataFrame(f"select * from movimentacoes where codigo_movimentacao = {codigo}")
        
        # Cria e retorna o objeto Movimentacao
        nova_movimentacao = Movimentacao(
            df_movimentacao.codigo_movimentacao.values[0],
            df_movimentacao.codigo_produto.values[0],
            df_movimentacao.tipo_movimentacao.values[0],
            df_movimentacao.quantidade.values[0],
            df_movimentacao.data_movimentacao.values[0],
            df_movimentacao.cnpj_fornecedor.values[0],
            df_movimentacao.motivo.values[0],
            df_movimentacao.numero_nota.values[0]
        )
        print("\nMovimentação registrada com sucesso!")
        print(nova_movimentacao.to_string())
        return nova_movimentacao
        
    def atualizar_movimentacao(self) -> Movimentacao:
        '''Atualiza uma movimentação existente'''
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        codigo_movimentacao = int(input("Código da Movimentação: "))
        
        # Verifica se a movimentação existe
        if not self.verifica_existencia_movimentacao(oracle, codigo_movimentacao):
            raise Exception("Movimentação não encontrada!")
            
        # Recupera os dados atuais da movimentação    
        df_movimentacao = oracle.sqlToDataFrame(f"select * from movimentacoes where codigo_movimentacao = {codigo_movimentacao}")
        tipo_movimentacao = df_movimentacao.tipo_movimentacao.values[0]
        quantidade_antiga = df_movimentacao.quantidade.values[0]
        codigo_produto = df_movimentacao.codigo_produto.values[0]
        
        quantidade = float(input("Nova Quantidade: "))
        motivo = input("Novo Motivo: ")
        numero_nota = input("Novo Número da Nota: ")
        
        # Atualiza a movimentação
        oracle.write(f"""update movimentacoes
                    set quantidade = {quantidade},
                        motivo = '{motivo}',
                        numero_nota = '{numero_nota}'
                    where codigo_movimentacao = {codigo_movimentacao}""")
                    
        # Ajusta o estoque conforme o tipo de movimentação
        if tipo_movimentacao == 'E':
            # Entrada - subtrai quantidade antiga e soma nova quantidade
            oracle.write(f"""update produtos set 
                        quantidade_atual = quantidade_atual - {quantidade_antiga} + {quantidade}
                        where codigo_produto = {codigo_produto}""")
        else:
            # Saída - soma quantidade antiga e subtrai nova quantidade  
            oracle.write(f"""update produtos set
                        quantidade_atual = quantidade_atual + {quantidade_antiga} - {quantidade}
                        where codigo_produto = {codigo_produto}""")
                        
        # Recupera os dados atualizados
        df_movimentacao = oracle.sqlToDataFrame(f"select * from movimentacoes where codigo_movimentacao = {codigo_movimentacao}")
        
        # Cria e retorna o objeto Movimentacao atualizado
        movimentacao_atualizada = Movimentacao(
            df_movimentacao.codigo_movimentacao.values[0],
            df_movimentacao.codigo_produto.values[0],
            df_movimentacao.tipo_movimentacao.values[0],
            df_movimentacao.quantidade.values[0],
            df_movimentacao.data_movimentacao.values[0],
            df_movimentacao.cnpj_fornecedor.values[0],
            df_movimentacao.motivo.values[0],
            df_movimentacao.numero_nota.values[0]
        )
        print("\nMovimentação atualizada com sucesso!")
        print(movimentacao_atualizada.to_string())
        return movimentacao_atualizada

    def registrar_saida(self) -> Movimentacao:
        '''Registra uma saída de produto do estoque'''
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Gera novo código de movimentação
        codigo = oracle.sqlToDataFrame("select nvl(max(codigo_movimentacao), 0) + 1 as codigo from movimentacoes")["codigo"].values[0]
        
        # Lista produtos disponíveis
        print("\nProdutos disponíveis:")
        df_produtos = oracle.sqlToDataFrame("""
            select p.codigo_produto, p.descricao_produto, p.quantidade_atual, 
                   c.nome_categoria, l.nome_localizacao
            from produtos p
            join categorias c on p.codigo_categoria = c.codigo_categoria  
            join localizacoes l on p.codigo_localizacao = l.codigo_localizacao
            where p.quantidade_atual > 0
            order by p.codigo_produto""")
        print(df_produtos)
        
        codigo_produto = int(input("\nCódigo do Produto: "))
        
        # Verifica se o produto existe
        df_produto = oracle.sqlToDataFrame(f"""
            select codigo_produto, descricao_produto, quantidade_atual, quantidade_minima 
            from produtos where codigo_produto = {codigo_produto}""")
            
        if df_produto.empty:
            print("Produto não encontrado!")
            return None
            
        quantidade = float(input("Quantidade: "))
        
        # Verificar se há quantidade suficiente
        qtd_atual = df_produto["quantidade_atual"].values[0]
        if qtd_atual < quantidade:
            print(f"Quantidade insuficiente. Disponível: {qtd_atual}")
            return None
            
        # Verifica se ficará abaixo do mínimo
        qtd_minima = df_produto["quantidade_minima"].values[0]
        if (qtd_atual - quantidade) < qtd_minima:
            print(f"\nATENÇÃO: Esta saída deixará o produto abaixo da quantidade mínima ({qtd_minima})!")
            if input("Deseja continuar? (S/N) ").upper() != 'S':
                return None
                
        # Lista fornecedores disponíveis para devolução
        print("\nFornecedores disponíveis:")
        df_fornecedores = oracle.sqlToDataFrame("select cnpj_fornecedor, razao_social from fornecedores order by razao_social")
        print(df_fornecedores)
        
        cnpj_fornecedor = input("\nCNPJ do Fornecedor: ")
        
        # Verifica se o fornecedor existe
        if oracle.sqlToDataFrame(f"select 1 from fornecedores where cnpj_fornecedor = '{cnpj_fornecedor}'").empty:
            print("Fornecedor não encontrado!")
            return None
                
        numero_nota = input("Número da Nota: ")
        motivo = input("Motivo: ")
        
        # Registra a movimentação de saída
        oracle.write(f"""insert into movimentacoes values 
                    ({codigo}, {codigo_produto}, 'S', {quantidade}, 
                    TO_DATE('{datetime.now().strftime("%d/%m/%Y")}', 'DD/MM/YYYY'),
                    '{cnpj_fornecedor}', '{motivo}', '{numero_nota}')""")
                    
        # Atualiza o estoque
        oracle.write(f"""update produtos set 
                    quantidade_atual = quantidade_atual - {quantidade},
                    data_ultima_movimentacao = TO_DATE('{datetime.now().strftime("%d/%m/%Y")}', 'DD/MM/YYYY')
                    where codigo_produto = {codigo_produto}""")
                    
        # Recupera os dados da movimentação
        df_movimentacao = oracle.sqlToDataFrame(f"select * from movimentacoes where codigo_movimentacao = {codigo}")
        
        # Cria e retorna o objeto Movimentacao 
        nova_movimentacao = Movimentacao(
            df_movimentacao.codigo_movimentacao.values[0],
            df_movimentacao.codigo_produto.values[0],
            df_movimentacao.tipo_movimentacao.values[0],
            df_movimentacao.quantidade.values[0],
            df_movimentacao.data_movimentacao.values[0],
            df_movimentacao.cnpj_fornecedor.values[0],
            df_movimentacao.motivo.values[0],
            df_movimentacao.numero_nota.values[0]
        )
        print("\nMovimentação registrada com sucesso!")
        print(nova_movimentacao.to_string())
        return nova_movimentacao