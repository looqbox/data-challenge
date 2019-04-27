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
select distinct sales_value, date from data_product_sales order by sales_value;
