-- TESTE SQL
# --------------------------------------------------------------------------------------------------------------

-- PERGUNTA 1:
-- QUAIS SÃO OS 10 PRODUTOS MAIS CAROS DA EMPRESA?


-- Seleciona os 10 produtos mais caros da tabela de produtos (data_product).
SELECT PRODUCT_NAME, PRODUCT_VAL
FROM data_product
ORDER BY PRODUCT_VAL DESC
LIMIT 10;
# --------------------------------------------------------------------------------------------------------------



-- PERGUNTA 2:
-- QUAIS SÃO AS SEÇÕES DOS DEPARTAMENTOS "BEBIDAS" E "PADARIA"?

-- Busca as seções de cada departamento.
SELECT DISTINCT SECTION_NAME, DEP_NAME
FROM data_product
where DEP_NAME IN ('PADARIA', 'BEBIDAS');
# --------------------------------------------------------------------------------------------------------------



-- PERGUNTA 3:
-- QUAL O TOTAL DE VENDAS DE PRODUTOS (EM DÓLARES) DE CADA ÁREA DE NEGÓCIO NO PRIMEIRO TRIMESTRE DE 2019

-- Traz a quantidade total de vendas para cada área de negócio.
SELECT A.BUSINESS_NAME    AS AREA_DE_NEGOCIO,
       SUM(D.SALES_VALUE) AS TOTAL_DE_VENDAS_DOLAR
FROM data_product_sales D
         INNER JOIN data_store_cad A
             ON D.STORE_CODE = A.STORE_CODE
WHERE D.DATE BETWEEN '2019-01-01' AND '2019-03-31' -- PRIMEIRO TRIMESTRE
GROUP BY A.BUSINESS_NAME
ORDER BY TOTAL_DE_VENDAS_DOLAR DESC
# --------------------------------------------------------------------------------------------------------------
