show databases;
use looqbox_challenge;

select * from data_product;
-- How many products the company has
select count(product_cod) as Products_Quantity from data_product;
-- The 10 most expensive products of the company 
select product_name, product_val from data_product order by product_val desc limit 10; 
-- Sections of PADARIA department
select distinct section_name, dep_name from data_product where dep_name = 'PADARIA';
-- Sections of BEBIDAS department
select distinct section_name, dep_name from data_product where dep_name = 'BEBIDAS';

select * from data_product_sales;
select * from data_store_cad;
-- The most products sold and its store
select A.sales_value, A.date, B.business_name
from data_product_sales as A
inner join data_store_cad as B
on B.store_code = A.store_code order by sales_value desc;

-- The sale of each business area in the first quarter of 2019