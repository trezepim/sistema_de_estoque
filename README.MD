# Sistema de Controle de Estoque com Python e Oracle

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

3. Testar a conexão com o banco de dados:
```shell
python src/test.py
```

## Organização
- [diagrams](diagrams): Nesse diretório está o [diagrama relacional](diagrams/sistema_de_estoque.mmd) (lógico) do sistema de controle de estoque.
    * O sistema gerencia cinco entidades principais:
        * PRODUTOS: Cadastro e controle de produtos em estoque
        * CLIENTES: Gerenciamento de clientes que realizam pedidos
        * FORNECEDORES: Cadastro de fornecedores que abastecem o estoque
        * PEDIDOS: Registro de transações de compra/venda
        * ITENS_PEDIDO: Detalhamento dos produtos em cada pedido com quantidades

- [sql](sql): Scripts SQL para configuração e população inicial do banco de dados
    * [create_tables_pedidos.sql](sql/create_tables_pedidos.sql): Cria a estrutura de tabelas com relacionamentos para controle de estoque
    * [inserting_samples_records.sql](sql/inserting_samples_records.sql): Insere dados de exemplo de produtos, clientes e fornecedores
    * [inserting_samples_related_records.sql](sql/inserting_samples_related_records.sql): Insere dados de exemplo de pedidos e movimentações de estoque

- [src](src): Código-fonte do sistema, organizado nos seguintes módulos:
    * [conexion](src/conexion): Módulo de conexão com o banco Oracle
        * [oracle_queries.py](src/conexion/oracle_queries.py): Gerencia conexões e queries
        * [passphrase](src/conexion/passphrase): Armazena credenciais de acesso

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
## Exemplos de Código

### Registro de Novo Produto (src/controller/controller_produto.py)
```python
def inserir_produto(self) -> Produto:
    oracle = OracleQueries()
    cursor = oracle.connect()
    output_value = cursor.var(int)

    descricao_novo_produto = input("Descrição (Novo): ")

    data = dict(codigo=output_value, descricao_produto=descricao_novo_produto)
    cursor.execute("""
    begin
        :codigo := PRODUTOS_CODIGO_PRODUTO_SEQ.NEXTVAL;
        insert into produtos values(:codigo, :descricao_produto);
    end;
    """, data)
    codigo_produto = output_value.getvalue()
    oracle.conn.commit()
    df_produto = oracle.sqlToDataFrame(f"select codigo_produto, descricao_produto from produtos where codigo_produto = {codigo_produto}")
    novo_produto = Produto(df_produto.codigo_produto.values[0], df_produto.descricao_produto.values[0])
    return novo_produto

```

### Verificação de Produto (src/controller/controller_produto.py)
```python
def verifica_existencia_produto(self, oracle:OracleQueries, codigo:int=None) -> bool:
    df_produto = oracle.sqlToDataFrame(f"select codigo_produto, descricao_produto from produtos where codigo_produto = {codigo}")
    return df_produto.empty
```

### Configuração do Oracle em Container
Se estiver usando Docker ou máquina virtual, ajuste o método connect em `src/conexion/oracle_queries.py`:
```python
self.conn = cx_Oracle.connect(user=self.user,
                          password=self.passwd,
                          dsn=self.connectionString(in_container=True)
                          )

### Bibliotecas Utilizadas
- [requirements.txt](src/requirements.txt): `pip install -r requirements.txt`

#### Em caso de problemas com a execução dos software dando a seguinte mensagem `ORA-28001: the password has expired`, execute as linhas de comando a seguir no Oracle:
- `ALTER PROFILE DEFAULT LIMIT PASSWORD_LIFE_TIME UNLIMITED;`
- `ALTER USER labdatabase IDENTIFIED BY "labDatabase2022";`
- `ALTER USER labdatabase IDENTIFIED BY  "labDatabase2022";`

### Instalando Oracle InstantClient
- Baixe a versão do [InstantClient](https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html) de acordo com a versão do Banco de Dados
- Caso esteja utilizando uma distribuição Linux baseado em Debian, será necessário executar o comando a seguir para converter o arquivo .rpm para .deb.
  ```shell
  sudo alien --scripts oracle-instantclient18.5-basic-18.5.0.0.0-3.x86_64.rpm
  ```
- Descompacte o arquivo e será gerado um diretório em um diretório de fácil acesso.
- Mova os diretórios lib e share para dentro do diretório do InstantClient
  ```shell
  sudo mv lib /usr/local/oracle/instantclient_18_5/
  ```
  
  ```shell
  sudo mv share instantclient_18_5/
  ```
- Edite o arquivo `.bash_profile` incluindo as linhas a seguir ao final do arquivo:
  ```shell
  export ORACLE_HOME=/usr/local/oracle/instantclient_18_5/lib/oracle/18.5/client64
  export LD_LIBRARY_PATH=$ORACLE_HOME/lib
  export PATH=$PATH:$ORACLE_HOME/bin
  export PATH
  ```

## Passo a Passo para Executar o Projeto

### 1. Pré-requisitos
- Oracle Database instalado (ou container Docker com Oracle)
- Python instalado
- Git (para clonar o repositório)

### 2. Configuração do Ambiente
1. Clone o repositório:
   ```shell
   git clone https://github.com/mrkn03/sistema_de_estoque.git
   cd sistema_de_estoque
   ```

2. Crie e ative um ambiente virtual Python:
   ```shell
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # ou
   .venv\Scripts\activate  # Windows
   ```

3. Instale as dependências:
   ```shell
   pip install -r src/requirements.txt
   ```

### 3. Configuração do Oracle InstantClient
1. Baixe o Oracle InstantClient compatível com sua versão do Oracle
2. Para distribuições Linux baseadas em Debian, converta o pacote RPM:
   ```shell
   sudo alien --scripts oracle-instantclient18.5-basic-18.5.0.0.0-3.x86_64.rpm
   ```
3. Configure os diretórios:
   ```shell
   sudo mkdir -p /usr/local/oracle/instantclient_18_5
   sudo cp -r /usr/lib/oracle/21 /usr/local/oracle/instantclient_18_5/lib
   sudo cp -r /usr/share/oracle/21 /usr/local/oracle/instantclient_18_5/share
   ```
4. Configure as variáveis de ambiente no ~/.bash_profile:
   ```shell
   export ORACLE_HOME=/usr/local/oracle/instantclient_18_5/lib/oracle/21/client64
   export LD_LIBRARY_PATH=$ORACLE_HOME/lib
   export PATH=$PATH:$ORACLE_HOME/bin
   export PATH
   ```
5. Aplique as alterações:
   ```shell
   source ~/.bash_profile
   ```

### 4. Configuração do Banco de Dados Oracle
1. Inicie o servidor Oracle (ou container Docker)
2. Acesse o SQL*Plus como administrador:
   ```shell
   sqlplus / as sysdba
   ```
3. Configure o usuário e privilégios:
   ```sql
   ALTER SESSION SET CONTAINER = XEPDB1;
   ALTER PROFILE DEFAULT LIMIT PASSWORD_LIFE_TIME UNLIMITED;
   GRANT ALL PRIVILEGES TO labdatabase;
   ALTER USER labdatabase IDENTIFIED BY "labDatabase2022";
   ```

### 5. Configuração do Projeto
1. Se estiver usando Docker ou máquina virtual, ajuste o arquivo `src/conexion/oracle_queries.py` para usar `in_container=True`
2. Verifique se o arquivo de autenticação está correto em `src/conexion/passphrase/authentication.oracle`
   - Deve conter: `labdatabase,labDatabase2022`

### 6. Execução do Sistema
1. Crie as tabelas e dados de exemplo:
   ```shell
   cd src
   python create_tables_and_records.py
   ```
2. Execute o programa principal:
   ```shell
   python principal.py
   ```
