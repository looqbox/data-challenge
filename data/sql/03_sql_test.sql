SELECT  sc.BUSINESS_NAME AS Business_Area,
        ROUND(SUM(ps.SALES_VALUE), 2) AS Total_Vendas
FROM data_product_sales ps
JOIN data_store_cad sc ON ps.STORE_CODE = sc.STORE_CODE
WHERE ps.DATE BETWEEN '2019-01-01' AND '2019-03-31'
GROUP BY sc.BUSINESS_NAME
ORDER BY Total_Vendas DESC;