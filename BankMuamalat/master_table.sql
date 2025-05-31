WITH cte AS(SELECT orders.OrderID,orders.order_date, orders.CustomerID, orders.ProdNumber,orders.Quantity,
products.ProdNumber,products.ProdName,products.Category,products.Price,
prod_category.CategoryID,prod_category.CategoryName,prod_category.CategoryAbbreviation,
customers.CustomerID AS Cust_ID, customers.CustomerAddress AS Address, customers.CustomerCity AS City,customers.CustomerState AS state
FROM orders
LEFT JOIN products
ON orders.ProdNumber = products.ProdNumber
LEFT JOIN prod_category
ON products.Category = prod_category.CategoryID
LEFT JOIN customers
ON orders.CustomerID = customers.CustomerID)
SELECT 
order_date,Cust_ID,City,State,ProdName,CategoryName,Price,Quantity,Price*Quantity AS Total
INTO master_table 
FROM cte

