-- Query 1 — Os 10 produtos mais caros da empresa
-- Decisão: desempate determinístico por PRODUCT_COD.
-- O 10º e 11º produtos empatam em preço (R$ 315,90). Mantive LIMIT 10
-- conforme o enunciado e adicionei PRODUCT_COD no ORDER BY para garantir
-- resultado reproduzível (sem o critério, o MySQL poderia retornar
-- produtos diferentes entre execuções no caso de empate).

SELECT dp.PRODUCT_COD, dp.PRODUCT_NAME, dp.PRODUCT_VAL
FROM `looqbox-challenge`.data_product dp
ORDER BY dp.PRODUCT_VAL DESC, dp.PRODUCT_COD ASC
LIMIT 10;
