select p.codigo_produto as "Código",
       p.descricao_produto as "Produto",
       c.nome_categoria as "Categoria",
       l.nome_localizacao as "Localização",
       p.quantidade_atual as "Qtd Atual",
       p.quantidade_minima as "Qtd Mínima",
       p.quantidade_maxima as "Qtd Máxima",
       case 
           when p.quantidade_atual <= p.quantidade_minima then 'CRÍTICO'
           when p.quantidade_atual <= p.quantidade_minima * 1.5 then 'ALERTA'
           else 'OK'
       end as "Status",
       p.preco_custo as "Preço Custo",
       p.preco_venda as "Preço Venda",
       p.data_ultima_movimentacao as "Última Movimentação"
from produtos p
join categorias c on p.codigo_categoria = c.codigo_categoria
join localizacoes l on p.codigo_localizacao = l.codigo_localizacao
order by 
    case 
        when p.quantidade_atual <= p.quantidade_minima then 1
        when p.quantidade_atual <= p.quantidade_minima * 1.5 then 2
        else 3
    end,
    p.descricao_produto