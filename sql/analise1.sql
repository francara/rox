/*
Escreva uma query que retorna a quantidade de linhas na
tabela Sales.SalesOrderDetail pelo campo SalesOrderID,
desde que tenham pelo menos três linhas de detalhes.
*/
select count(d.SalesOrderId)
from salesdetail d
where
  (select count(*) from salesdetail dd
   where
     dd.SalesOrderId = d.SalesOrderId
  ) >= 3