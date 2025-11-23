from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorio
from controller.controller_produto import Controller_Produto
from controller.controller_fornecedor import Controller_Fornecedor
from controller.controller_categoria import Controller_Categoria
from controller.controller_localizacao import Controller_Localizacao
from controller.controller_movimentacao import Controller_Movimentacao

tela_inicial = SplashScreen()
relatorio = Relatorio()
ctrl_produto = Controller_Produto()
ctrl_fornecedor = Controller_Fornecedor()
ctrl_categoria = Controller_Categoria()
ctrl_localizacao = Controller_Localizacao()
ctrl_movimentacao = Controller_Movimentacao()

def reports(opcao_relatorio:int=0):
    """Função para chamar os relatórios do MongoDB"""
    if opcao_relatorio == 1:
        relatorio.get_relatorio_produtos_abaixo_minimo()            
    elif opcao_relatorio == 2:
        relatorio.get_relatorio_produtos_por_categoria()
    elif opcao_relatorio == 3:
        relatorio.get_relatorio_movimentacoes_periodo()
    elif opcao_relatorio == 4:
        relatorio.get_relatorio_posicao_estoque()
    elif opcao_relatorio == 5:
        relatorio.get_relatorio_produtos()
    elif opcao_relatorio == 6:
        relatorio.get_relatorio_fornecedores()

def inserir(opcao_inserir:int=0):
    """Função para inserir novos registros no MongoDB"""
    if opcao_inserir == 1:                               
        novo_produto = ctrl_produto.inserir_produto()
    elif opcao_inserir == 2:
        nova_categoria = ctrl_categoria.inserir_categoria()
    elif opcao_inserir == 3:
        novo_fornecedor = ctrl_fornecedor.inserir_fornecedor()
    elif opcao_inserir == 4:
        nova_localizacao = ctrl_localizacao.inserir_localizacao()
    elif opcao_inserir == 5:
        nova_movimentacao = ctrl_movimentacao.inserir_movimentacao()

def atualizar(opcao_atualizar:int=0):
    """Função para atualizar registros existentes no MongoDB"""
    if opcao_atualizar == 1:
        relatorio.get_relatorio_produtos()
        produto_atualizado = ctrl_produto.atualizar_produto()
    elif opcao_atualizar == 2:
        print("\nCategorias disponíveis:")
        relatorio.get_relatorio_produtos_por_categoria()
        categoria_atualizada = ctrl_categoria.atualizar_categoria()
    elif opcao_atualizar == 3:
        relatorio.get_relatorio_fornecedores()
        fornecedor_atualizado = ctrl_fornecedor.atualizar_fornecedor()
    elif opcao_atualizar == 4:
        print("\nLocalizações no relatório de produtos:")
        relatorio.get_relatorio_produtos()
        localizacao_atualizada = ctrl_localizacao.atualizar_localizacao()
    elif opcao_atualizar == 5:
        print("\nMovimentações por período:")
        relatorio.get_relatorio_movimentacoes_periodo()
        movimentacao_atualizada = ctrl_movimentacao.atualizar_movimentacao()

def excluir(opcao_excluir:int=0):
    """Função para excluir registros do MongoDB"""
    if opcao_excluir == 1:
        relatorio.get_relatorio_produtos()
        ctrl_produto.excluir_produto()
    elif opcao_excluir == 2:                
        print("\nCategorias disponíveis:")
        relatorio.get_relatorio_produtos_por_categoria()
        ctrl_categoria.excluir_categoria()
    elif opcao_excluir == 3:                
        relatorio.get_relatorio_fornecedores()
        ctrl_fornecedor.excluir_fornecedor()
    elif opcao_excluir == 4:                
        print("\nLocalizações no relatório de produtos:")
        relatorio.get_relatorio_produtos()
        ctrl_localizacao.excluir_localizacao()
    elif opcao_excluir == 5:
        print("\nMovimentações por período:")
        relatorio.get_relatorio_movimentacoes_periodo()
        ctrl_movimentacao.excluir_movimentacao()

def movimentar_estoque():
    """Função para movimentar o estoque"""
    while True:
        print(config.MENU_MOVIMENTACAO)
        opcao = int(input("Escolha uma opção [0-2]: "))
        config.clear_console(1)
        
        if opcao == 1:
            ctrl_movimentacao.registrar_entrada()
        elif opcao == 2:
            ctrl_movimentacao.registrar_saida()
        elif opcao == 0:
            break
        
        config.clear_console()

def run():
    """Função principal para execução do menu"""
    print(tela_inicial.get_updated_screen())
    config.clear_console()

    while True:
        print(config.MENU_PRINCIPAL)
        opcao = int(input("Escolha uma opção [1-6]: "))
        config.clear_console(1)
        
        if opcao == 1:
            print(config.MENU_RELATORIOS)
            opcao_relatorio = int(input("Escolha uma opção [0-6]: "))
            config.clear_console(1)

            if opcao_relatorio == 0:
                continue
                
            reports(opcao_relatorio)
            config.clear_console(1)

        elif opcao == 2:
            print(config.MENU_ENTIDADES)
            opcao_inserir = int(input("Escolha uma opção [0-5]: "))
            config.clear_console(1)

            if opcao_inserir == 0:
                continue
                
            inserir(opcao_inserir=opcao_inserir)
            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 3:
            print(config.MENU_ENTIDADES)
            opcao_atualizar = int(input("Escolha uma opção [0-5]: "))
            config.clear_console(1)

            if opcao_atualizar == 0:
                continue
                
            atualizar(opcao_atualizar=opcao_atualizar)
            config.clear_console()

        elif opcao == 4:
            print(config.MENU_ENTIDADES)
            opcao_excluir = int(input("Escolha uma opção [0-5]: "))
            config.clear_console(1)

            if opcao_excluir == 0:
                continue
                
            excluir(opcao_excluir=opcao_excluir)
            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 5:
            movimentar_estoque()
            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 6:
            print(tela_inicial.get_updated_screen())
            config.clear_console()
            print("Obrigado por utilizar o nosso sistema.")
            exit(0)

        else:
            print("Opção incorreta. Tente novamente.")
            exit(0)

if __name__ == "__main__":
    run()

