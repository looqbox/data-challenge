SELECT DISTINCT dp.section_name, dp.dep_name, dp.section_cod
FROM data_product dp 
WHERE dp.dep_name IN ('BEBIDAS', 'PADARIA')
