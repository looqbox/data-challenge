# Looqbox Data Challenge
![Looqbox](https://github.com/looqbox/data-challenge/blob/master/logo.png)

## Accessing the database
You will need to access our MySQL database for this challenge. The database credentials will be sent to you by e-mail.

## Challenge
### Tables descriptions
 <details>
  <summary><b> DATA_PRODUCT: PRODUCT INFO</b></summary>

| COLUMN NAME  | COLUMN DESCRIPTION                                 |
|--------------|----------------------------------------------------|
| PRODUCT_COD  | PRODUCT CODE                                       |
| PRODUCT_NAME | PRODUCT FULL NAME                                  |
| PRODUCT_VAL  | PRODUCT SALES VALUE                                |
| DEP_NAME     | NAME OF THE DEPARTMENT RESPONSIBLE FOR THE PRODUCT |
| DEP_COD      | CODE OF THE DEPARTMENT RESPONSIBLE FOR THE PRODUCT |
| SECTION_NAME | NAME OF THE SECTION WHERE THE PRODUCT IS           |
| SECTION_COD  | CODE OF THE SECTION WHERE THE PRODUCT IS           |

 </details>
  
 <details>
  <summary><b> DATA_PRODUCT_SALES: PRODUCT SALES</b></summary>

| COLUMN NAME  | COLUMN DESCRIPTION                                 |
|--------------|----------------------------------------------------|
| STORE_CODE   | STORE CODE                                         |
| PRODUCT_CODE | PRODUCT CODE                                       |
| DATE         | SALES DATE                                         |
| SALES_VALUE  | SALES VALUES                                       |
| SALES_QTY    | SALES QUANTITY                                     |

  
 </details>
 <details>
  <summary><b> DATA_STORE_CAD: STORE INFO</b></summary>

| COLUMN NAME  | COLUMN DESCRIPTION                                 |
|--------------|----------------------------------------------------|
| STORE_CODE   | STORE CODE                                         |
| STORE_NAME   | STORE NAME                                         |
| START_DATE   | SHOP OPENING DATE                                  |
| END_DATA     | SHOP CLOSING DATE                                  |
| BUSINESS_NAME| NAMES OF BUSINESS AREA RESPONSIBLE FOR THE SHOP    |
| BUSINESS_CODE| CODE OF BUSINESS AREA RESPONSIBLE FOR THE SHOP     |

 </details>
 <details>
  <summary><b> DATA_STORE_SALES: SALES PER STORE</b></summary>

| COLUMN NAME  | COLUMN DESCRIPTION                                 |
|--------------|----------------------------------------------------|
| STORE_CODE   | STORE CODE                                         |
| DATE         | COMMERCIAL DATE                                    |
| SALES_VALUE  | TOTAL VALUE OF SALES IN THAT DATE                  |
| SALES_QTY    | TOTAL QUANTITY OF SALES IN THAT DATE               |

 </details>

### SQL test
After accessing our database, create queries using the schema **looqbox_challenge** to answer the following questions:

1) What are the 10 most expensive products in the company?
2) What sections do the 'BEBIDAS' and 'PADARIA' departments have?
3) What was the total sale of products (in $) of each Business Area in the first quarter of 2019?

### Cases
#### 1) The Dev Team was tired of developing the same old queries just varying the filters accordingly to their boss demands.
As a new member of the crew, your mission now is to create a dynamic function, on the most flexible of ways, to produce queries and retrieve a dataframe based on three parameters:

- product_code: integer

- store_code: integer

- date: list of ISO-like strings

- Date e.g.
  - ['2019-01-01', '2019-01-31'] → Python

  - c('2019-01-01', '2019-01-31') → R

It should look like this
my_data = retrieve_data(product_code, store_code, date)

Make your team proud!

Extra instructions:
Retrieve all columns from table data_product_sales.

#### 2) A brand new client sent you two ready-to-go queries. Those are listed below:

Query 1:

```
SELECT
      STORE_CODE,
      STORE_NAME,
      START_DATE,
      END_DATE,
      BUSINESS_NAME,
      BUSINESS_CODE
FROM data_store_cad
```
Query 2:

```
SELECT
        STORE_CODE,
        DATE,
        SALES_VALUE,
        SALES_QTY
FROM data_store_sales
WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
```
In addition, he gave you this set of instructions:

- You must not modify my queries!

- Please filter the period between this given range: 
  - ['2019-10-01','2019-12-31']


<details>
 <summary><b> We are in need of this visualization (click here to see it)! Please, create it with Python or R</b></summary>
  
| Loja           | Categoria   | TM    | 
|----------------|-------------|-------| 
| Bahia          | Atacado     | 15.39 | 
| Bangkok        | Posto       | 13.67 | 
| Belem          | Proximidade | 15.37 | 
| Berlin         | Proximidade | 15.39 | 
| Buenos Aires   | Atacado     | 15.39 | 
| Chicago        | Varejo      | 15.53 | 
| Dubai          | Atacado     | 15.39 | 
| Hong Kong      | Farma       | 26.35 | 
| London         | Farma       | 28.99 | 
| Madri          | Farma       | 29.03 | 
| Miami          | Posto       | 13.67 | 
| New York       | Proximidade | 15.39 | 
| Paris          | Proximidade | 15.39 | 
| Rio de Janeiro | Farma       | 29.59 | 
| Roma           | Varejo      | 15.39 | 
| Salvador       | Atacado     | 15.39 | 
| Sao Paulo      | Varejo      | 15.39 | 
| Sidney         | Posto       | 13.67 | 
| Tokio          | Varejo      | 15.39 | 
| Vancouver      | Posto       | 13.67 | 
  
</details>

#### 3) Building your own visualization

Create at least one chart using the table **IMDB_movies**. The code must be in R or Python, and you are free to use any libraries, data in the table and graphic format. Explain why you chose the visualization (or visualizations) you are submitting.

## Stack
- MySQL database 
- R/Python

## Submitting
- Send an e-mail to the person that you are in contact within Looqbox!
- Your answer must be sent in PDF format with the code snippets used in each question, as well as the result obtained (values, tables, graphs)

## Useful links
- [MySQL documentation](https://dev.mysql.com/doc/)
- [Data Visualization Catalogue](https://datavizcatalogue.com/)
