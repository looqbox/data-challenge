-- 3) Qual foi o total de vendas de produtos (em dólares) de cada área de negócios no primeiro trimestre de 2019?

SELECT store.business_name AS area_de_negocios, SUM(sales.sales_value) AS total_vendas
FROM data_store_cad as store 
JOIN data_store_sales as sales
WHERE store.store_code = sales.store_code AND sales.date BETWEEN '2019-01-01' AND '2019-03-31'
GROUP BY store.business_name
ORDER BY total_vendas DESC;
