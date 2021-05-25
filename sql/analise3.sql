/*
Escreva uma query ligando as tabelas
Person.Person, Sales.Customer e Sales.SalesOrderHeader de forma a
obter uma lista de nomes de clientes e uma contagem de pedidos efetuados.
*/
select p.businessEntityID, concat(p.firstname, ' ', p.middlename, ' ', p.lastname) as completename, count(*)
from customer c
join person p on p.businessEntityID = c.personID
join salesorder s on s.customerID = c.customerID
group by p.businessEntityID, concat(p.firstname, ' ', p.middlename, ' ', p.lastname)