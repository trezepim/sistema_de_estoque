select p.codigo_produto as "Código",
       p.descricao_produto as "Produto",
       p.quantidade_atual as "Qtd Atual", 
       p.quantidade_minima as "Qtd Mínima",
       c.nome_categoria as "Categoria",
       l.nome_localizacao as "Localização"
from produtos p
join categorias c on p.codigo_categoria = c.codigo_categoria
join localizacoes l on p.codigo_localizacao = l.codigo_localizacao
where p.quantidade_atual <= p.quantidade_minima
order by p.quantidade_atual