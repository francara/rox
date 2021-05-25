/*
Escreva uma query que ligue as tabelas
Sales.SalesOrderDetail, Sales.SpecialOfferProduct e Production.Product e
retorne os 3 produtos (Name) mais vendidos (pela soma de OrderQty),
agrupados pelo número de dias para manufatura (DaysToManufacture).
*/
with rank as (
  select p.daystomanufacture, p.Name, sum(d.orderqty) total
  from salesdetail d
  join specialoffer o on o.specialOfferID = d.specialOfferID
  join product p on p.productID = d.productID
  group by p.daystomanufacture, p.Name
  order by p.daystomanufacture, total desc
)
select * from (
  select row_number() over (partition by daystomanufacture) as rowid, *
  from rank)
where
  rowid <= 3
