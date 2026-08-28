# Descrição das queries solicitadas:

# 1.	What are the 10 most expensive products in the company?
select 
product.PRODUCT_NAME,
product.PRODUCT_COD,
MAX(SALES_VALUE / SALES_QTY) AS UNIT_PRICE
FROM `looqbox-challenge`.data_product product
inner join `looqbox-challenge`.data_product_sales sales
	on product.PRODUCT_COD = sales.PRODUCT_CODE
GROUP BY 
	product.PRODUCT_COD,
	product.PRODUCT_NAME
ORDER BY UNIT_PRICE DESC
LIMIT 10;


# 2.	What sections do the 'BEBIDAS' and 'PADARIA' departments have?
SELECT DISTINCT
	DEP_NAME,
	SECTION_NAME
FROM `looqbox-challenge`.data_product
WHERE DEP_NAME = "BEBIDAS" OR DEP_NAME = "PADARIA"
order by DEP_NAME;


# 3.	What was the total sale of products (in $) of each Business Area in the first quarter of 2019?
select 
store.BUSINESS_NAME,
SUM(sales.SALES_VALUE) AS TOTAL_VALUE
FROM `looqbox-challenge`.data_store_cad store
inner join `looqbox-challenge`.data_product_sales sales
	on store.STORE_CODE = sales.STORE_CODE
where sales.DATE between '2019-01-01' AND '2019-03-31'
group by store.BUSINESS_NAME;
