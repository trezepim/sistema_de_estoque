select f.cnpj as "CNPJ",
       f.razao_social as "Razão Social",
       f.nome_fantasia as "Nome Fantasia"
from fornecedores f
order by f.nome_fantasia