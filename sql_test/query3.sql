-- Query 3 — Venda total (em $) por Business Area no 1º trimestre de 2019
-- JOIN entre as vendas de produto (data_product_sales) e o cadastro de loja
-- (data_store_cad), que contém a Business Area.
-- Decisão técnica: STORE_CODE é varchar em data_product_sales e int em
-- data_store_cad. Apliquei CAST(... AS UNSIGNED) para alinhar os tipos no JOIN.
-- DATE é tipo DATE (sem hora), então BETWEEN inclui o dia 31/03 integralmente.
-- INNER JOIN é adequado: uma venda sem loja cadastrada não tem Business Area
-- atribuível, logo deve ficar de fora da agregação por área.

SELECT   dsc.BUSINESS_NAME,
         SUM(dps.SALES_VALUE) AS TOTAL_VENDA
FROM     `looqbox-challenge`.data_product_sales dps
JOIN     `looqbox-challenge`.data_store_cad dsc
         ON CAST(dps.STORE_CODE AS UNSIGNED) = dsc.STORE_CODE
WHERE    dps.`DATE` BETWEEN '2019-01-01' AND '2019-03-31'
GROUP BY dsc.BUSINESS_NAME
ORDER BY TOTAL_VENDA DESC;
