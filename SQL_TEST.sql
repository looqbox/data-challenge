#What are the 10 most expensive products in the company?
SELECT PRODUCT_NAME, PRODUCT_VAL
FROM data_product
ORDER BY PRODUCT_VAL DESC
LIMIT 10;

#What sections do the 'BEBIDAS' and 'PADARIA' departments have?
SELECT DISTINCT SECTION_NAME
FROM data_product
WHERE DEP_NAME IN ('BEBIDAS', 'PADARIA');

#What was the total sale of products (in $) of each Business Area in the first quarter of 2019?
SELECT sc.BUSINESS_NAME, SUM(ps.SALES_VALUE * ps.SALES_QTY) AS TOTAL_SALES
FROM data_product_sales AS ps
LEFT JOIN data_store_cad AS sc
ON ps.STORE_CODE = sc.STORE_CODE
WHERE ps.DATE BETWEEN '2019-01-01' AND '2019-03-31'
GROUP BY sc.BUSINESS_NAME
ORDER BY TOTAL_SALES DESC;