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

-- The most products sold and its date/store name
select A.sales_value, A.date, B.business_name
from data_product_sales as A
inner join data_store_cad as B
on B.store_code = A.store_code order by sales_value desc;

-- data_store_sales analysis 
select * from data_store_sales order by SALES_VALUE desc;

select distinct A.store_code, B.business_name
from data_store_sales as A
inner join data_store_cad as B
on A.store_code = B.store_code;

-- The sale of each business area in the first quarter of 2019

-- Value of the sales
select FORMAT(sum(A.sales_value),2) "sales - R$", B.business_name 
from data_store_sales as A
left join data_store_cad as B
on B.store_code = A.store_code where date between '2018-12-31 00:00:00' and '2019-03-31 23:59:00' 
group by business_name;

-- Quantity of the sales
select sum(A.sales_qty) "qty" , B.business_name
from data_store_sales as A
left join data_store_cad as B
on B.store_code = A.store_code 
where date between '2018-12-31 00:00:00' and '2019-03-31 23:59:00' 
group by business_name;

-- github/palomara - looqbox_challenge

