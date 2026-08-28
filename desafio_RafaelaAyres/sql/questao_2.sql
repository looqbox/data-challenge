-- 2) Quais são as seções dos departamentos 'BEBIDAS' e 'PADARIA'?

SELECT DISTINCT section_cod AS cod_secao, section_name AS secao, DEP_cod AS cod_dep, dep_name AS departamento
FROM data_product
WHERE dep_name IN ('BEBIDAS', 'PADARIA')
ORDER BY dep_name, section_name;
