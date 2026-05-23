SELECT dsc.business_name, dsc.business_code, SUM(dps.sales_value)
FROM data_store_cad dsc 
INNER JOIN data_product_sales dps
	ON dsc.store_code = dps.store_code
WHERE dps.date BETWEEN '2019-01-01' AND '2019-03-31'
GROUP BY dsc.business_name, dsc.BUSINESS_CODE 
