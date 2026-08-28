-- 1) Quais são os 10 produtos mais caros da empresa?

SELECT product_cod as codigo, product_name as nome_produto, product_val as valor_produto, dep_name as departamento 
FROM data_product
ORDER BY Product_val DESC
LIMIT 10;
