# Sistema de Controle de Estoque com Python e MongoDB

Sistema para gerenciamento de estoque.  
O sistema permite o controle eficiente de produtos, gestão de pedidos de compra e venda, e geração de relatórios gerenciais para tomada de decisão.

## Funcionalidades Principais

- **Gestão de Produtos**
  * Cadastro e atualização de produtos
  * Controle de estoque
  * Preços e informações detalhadas

- **Gestão de Clientes e Fornecedores**
  * Cadastro completo de clientes
  * Gestão de fornecedores
  * Histórico de transações

- **Controle de Pedidos**
  * Registro de pedidos de compra e venda
  * Múltiplos itens por pedido
  * Acompanhamento de status

- **Relatórios Gerenciais**
  * Relatórios de estoque
  * Análise de pedidos por fornecedor
  * Histórico de movimentações
  * Relatórios de clientes e fornecedores

## Início Rápido

1. Criar as tabelas e dados iniciais:
```shell
python src/create_tables_and_records.py
```

2. Executar o sistema:
```shell
python src/principal.py
```

## Organização
- [diagrams](diagrams): Nesse diretório está o [diagrama relacional](diagrams/sistema_de_estoque.mmd) (lógico) do sistema de controle de estoque.
    * O sistema gerencia cinco entidades principais:
        * PRODUTOS: Cadastro e controle de produtos em estoque
        * CLIENTES: Gerenciamento de clientes que realizam pedidos
        * FORNECEDORES: Cadastro de fornecedores que abastecem o estoque
        * PEDIDOS: Registro de transações de compra/venda
        * ITENS_PEDIDO: Detalhamento dos produtos em cada pedido com quantidades

- [src](src): Código-fonte do sistema, organizado nos seguintes módulos:
    * [conexion](src/conexion): Módulo de conexão com o banco

    * [controller](src/controller): Classes controladoras para gerenciamento de entidades
        * [controller_produto.py](src/controller/controller_produto.py): Gerencia produtos (CRUD)
        * [controller_cliente.py](src/controller/controller_cliente.py): Gerencia clientes (CRUD)
        * [controller_fornecedor.py](src/controller/controller_fornecedor.py): Gerencia fornecedores (CRUD)
        * [controller_pedido.py](src/controller/controller_pedido.py): Gerencia pedidos (CRUD)
        * [controller_item_pedido.py](src/controller/controller_item_pedido.py): Gerencia itens de pedido (CRUD)

    * [model](src/model): Classes que representam as entidades do sistema
        * [produtos.py](src/model/produtos.py): Modelo de produtos com atributos e métodos
        * [clientes.py](src/model/clientes.py): Modelo de clientes
        * [fornecedores.py](src/model/fornecedores.py): Modelo de fornecedores
        * [pedidos.py](src/model/pedidos.py): Modelo de pedidos
        * [itens_pedido.py](src/model/itens_pedido.py): Modelo de itens de pedido

    * [reports](src/reports): Módulo de relatórios
        * [relatorios.py](src/reports/relatorios.py): Gera relatórios gerenciais:
            * Relatório de Pedidos por Fornecedor
            * Relatório de Pedidos
            * Relatório de Produtos em Estoque
            * Relatório de Clientes
            * Relatório de Fornecedores
            * Relatório de Itens de Pedidos

    * [utils](src/utils): Módulos utilitários
        * [config.py](src/utils/config.py): Configurações e menus do sistema
        * [splash_screen.py](src/utils/splash_screen.py): Interface inicial

    * Arquivos principais:
        * [create_tables_and_records.py](src/create_tables_and_records.py): Script de inicialização do banco
        * [principal.py](src/principal.py): Ponto de entrada do sistema, integra todos os módulos
