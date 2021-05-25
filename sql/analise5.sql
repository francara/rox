/*
Escreva uma query mostrando os campos
SalesOrderID, OrderDate e TotalDue da tabela Sales.SalesOrderHeader.
Obtenha apenas as linhas onde a ordem tenha sido feita
durante o mês de setembro/2011 e o total devido esteja acima de 1.000.
Ordene pelo total devido decrescente.
*/
with sale as (
  select salesOrderID,
  substr(orderDate, 1, 4) as orderYear,
  substr(orderDate, 6, 2) as orderMonth, orderDate, totalDue
  from salesorder o
  where totalDue > 1000
)
select salesOrderID, orderDate, totalDue from sale
where
  orderYear = '2011' and orderMonth = '07'
order by totalDue desc

