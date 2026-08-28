-- SQL question 3: product sales by business area in Q1 2019.
-- Validate join cardinality and totals before including the result in the report.
SELECT
    store.BUSINESS_CODE,
    store.BUSINESS_NAME,
    SUM(sales.SALES_VALUE) AS TOTAL_SALES_VALUE
FROM `looqbox-challenge`.data_product_sales AS sales
INNER JOIN `looqbox-challenge`.data_store_cad AS store
    ON store.STORE_CODE = sales.STORE_CODE
WHERE sales.DATE >= '2019-01-01'
  AND sales.DATE < '2019-04-01'
GROUP BY
    store.BUSINESS_CODE,
    store.BUSINESS_NAME
ORDER BY TOTAL_SALES_VALUE DESC;
