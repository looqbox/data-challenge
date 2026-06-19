use `looqbox-challenge`;

SELECT
	PRODUCT_NAME AS 'Nome do Produto',
    PRODUCT_VAL AS 'Valor do Produto'
FROM data_product
ORDER BY PRODUCT_VAL DESC
LIMIT 10;

SELECT DISTINCT
	DEP_NAME AS 'Nome do Departamento',
	SECTION_NAME AS 'Nome da Seção'
FROM data_product
WHERE DEP_NAME IN ('BEBIDAS', 'PADARIA')
ORDER BY DEP_NAME;

SELECT
	b.BUSINESS_NAME AS 'Área de Negócio',
    SUM(a.SALES_VALUE) AS 'Vendas Totais'
FROM data_store_sales as a
INNER JOIN data_store_cad AS b
	ON a.STORE_CODE = b.STORE_CODE
WHERE a.DATE BETWEEN '2019-01-01' AND '2019-03-31'
GROUP BY b.BUSINESS_NAME
ORDER BY 'Vendas Totais' DESC;