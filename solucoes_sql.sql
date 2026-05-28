-- 1. What are the 10 most expensive products in the company?
USE `looqbox-challenge`;
SELECT PRODUCT_COD, PRODUCT_NAME, PRODUCT_VAL FROM data_product
ORDER BY PRODUCT_VAL DESC
LIMIT 10;

-- 2. What sections do the 'BEBIDAS' and 'PADARIA' departments have?
USE `looqbox-challenge`;
SELECT DISTINCT SECTION_COD, SECTION_NAME, DEP_NAME 
FROM data_product
WHERE DEP_NAME = 'BEBIDAS' OR DEP_NAME = 'PADARIA'
ORDER BY DEP_NAME;

-- 3. What was the total sale of products (in $) of each Business Area in the first quarter of 2019?
USE `looqbox-challenge`;
SELECT dsc.BUSINESS_NAME, SUM(dss.SALES_VALUE) as TOTAL_SALES
FROM data_store_cad dsc
INNER JOIN data_store_sales dss
ON dsc.STORE_CODE = dss.STORE_CODE
WHERE dss.DATE BETWEEN '2019-01-01' AND '2019-03-31'
GROUP BY dsc.BUSINESS_NAME
ORDER BY TOTAL_SALES DESC;


