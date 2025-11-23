select p.codigo_produto as "Código",
       p.descricao_produto as "Produto",
       p.quantidade_atual as "Estoque Atual",
       p.quantidade_minima as "Estoque Mínimo",
       p.quantidade_maxima as "Estoque Máximo", 
       p.preco_custo as "Preço Custo",
       p.preco_venda as "Preço Venda",
       c.nome_categoria as "Categoria",
       l.nome_localizacao as "Localização",
       p.data_ultima_movimentacao as "Última Movimentação"
from produtos p
join categorias c on p.codigo_categoria = c.codigo_categoria
join localizacoes l on p.codigo_localizacao = l.codigo_localizacao
order by p.descricao_produto