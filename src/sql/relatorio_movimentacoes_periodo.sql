select m.data_movimentacao as "Data",
       p.descricao_produto as "Produto",
       case m.tipo_movimentacao 
           when 'E' then 'Entrada'
           when 'S' then 'Saída'
       end as "Tipo",
       m.quantidade as "Quantidade",
       f.nome_fantasia as "Fornecedor",
       m.motivo as "Motivo",
       m.numero_nota as "Nota Fiscal"
from movimentacoes m
join produtos p on m.codigo_produto = p.codigo_produto
left join fornecedores f on m.cnpj_fornecedor = f.cnpj
where m.data_movimentacao between to_date('&data_inicial', 'DD/MM/YYYY')
                             and to_date('&data_final', 'DD/MM/YYYY')
order by m.data_movimentacao desc