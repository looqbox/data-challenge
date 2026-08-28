-- SQL question 2: sections belonging to BEBIDAS and PADARIA.
SELECT DISTINCT
    DEP_NAME,
    SECTION_COD,
    SECTION_NAME
FROM `looqbox-challenge`.data_product
WHERE DEP_NAME IN ('BEBIDAS', 'PADARIA')
ORDER BY DEP_NAME, SECTION_NAME;
