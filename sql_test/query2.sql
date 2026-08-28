-- Query 2 — Seções dos departamentos BEBIDAS e PADARIA
-- DISTINCT elimina a duplicação (cada seção se repete por produto).
-- Verificação prévia: confirmei a lista completa de departamentos para
-- garantir que não havia variações de nome (ex.: "BEBES" é um departamento
-- distinto de "BEBIDAS"). Apenas "BEBIDAS" e "PADARIA" correspondem ao pedido.

SELECT DISTINCT dp.DEP_NAME, dp.SECTION_NAME
FROM `looqbox-challenge`.data_product dp
WHERE dp.DEP_NAME IN ('BEBIDAS', 'PADARIA')
ORDER BY dp.DEP_NAME;
