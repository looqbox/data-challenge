-- SQL question 1: ten most expensive products.
-- Run this query against the looqbox_challenge schema and validate the result.
SELECT
    PRODUCT_COD,
    PRODUCT_NAME,
    PRODUCT_VAL
FROM `looqbox-challenge`.data_product
ORDER BY PRODUCT_VAL DESC
LIMIT 10;
