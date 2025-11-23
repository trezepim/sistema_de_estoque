select c.nome_categoria as "Categoria",
       p.codigo_produto as "Código",
       p.descricao_produto as "Produto",
       p.quantidade_atual as "Qtd Atual",
       p.quantidade_minima as "Qtd Mínima",
       l.nome_localizacao as "Localização",
       p.preco_venda as "Preço"
from produtos p
join categorias c on p.codigo_categoria = c.codigo_categoria
join localizacoes l on p.codigo_localizacao = l.codigo_localizacao
order by c.nome_categoria, p.descricao_produto