/*
Escreva uma query usando as tabelas
Sales.SalesOrderHeader, Sales.SalesOrderDetail e Production.Product, de forma a
obter a soma total de produtos (OrderQty) por ProductID e OrderDate.
*/
select p.productID, o.orderDate, sum(d.orderqty) total
from salesorder o
join salesdetail d on d.salesOrderID = o.salesOrderID
join product p on p.productID = d.productID
group by p.productID, o.orderDate
