-- Pergunta 1 Quais são os 10 produtos mais caros na empresa?
-- Resposta:
SELECT 
    PRODUCT_COD, 
    PRODUCT_NAME, 
    PRODUCT_VAL
FROM 
    data_product
ORDER BY 
    PRODUCT_VAL DESC
LIMIT 10;

-- Pergunta 2 Quais seções os departamentos 'BEBIDAS' e 'PADARIA' possuem? 
-- Resposta:
SELECT DISTINCT
    DEP_NAME,
    SECTION_NAME
FROM 
    data_product
WHERE 
    DEP_NAME IN ('BEBIDAS', 'PADARIA')
ORDER BY 
    DEP_NAME, 
    SECTION_NAME;

-- Pergunta 3 Qual foi a venda total de produtos (em $) de cada Área de Negócio no primeiro trimestre de 2019?
-- Resposta:
SELECT 
    cadastro.BUSINESS_NAME,
    ROUND(SUM(vendas.SALES_VALUE), 2) AS TOTAL_VENDAS_Q1
FROM 
    data_store_sales AS vendas

JOIN 
    data_store_cad AS cadastro 
    ON vendas.STORE_CODE = cadastro.STORE_CODE

WHERE 
    vendas.DATE BETWEEN '2019-01-01' AND '2019-03-31'
GROUP BY 
    cadastro.BUSINESS_NAME
ORDER BY 
    TOTAL_VENDAS_Q1 DESC;