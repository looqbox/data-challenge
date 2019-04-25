# Looqbox Data Challenge
![Looqbox](https://github.com/looqbox/data-challenge/blob/master/logo.png)

## Accessing the database
You will need to use MySQL to access our database. The database informations will be sent to you with the challenge e-mail.

## Tables descriptions
- **DATA_PRODUCT: PRODUCT INFO**

| COLUMN NAME  | COLUMN DESCRIPTION                                 |
|--------------|----------------------------------------------------|
| PRODUCT_COD  | PRODUCT CODE                                       |
| PRODUCT_NAME | PRODUCT FULL NAME                                  |
| PRODUCT_VAL  | PRODUCT SALES VALUE                                |
| DEP_NAME     | NAME OF THE DEPARTMENT RESPONSIBLE FOR THE PRODUCT |
| DEP_COD      | CODE OF THE DEPARTMENT RESPONSIBLE FOR THE PRODUCT |
| SECTION_NAME | NAME OF THE SECTION WHERE THE PRODUCT IS           |
| SECTION_COD  | CODE OF THE SECTION WHERE THE PRODUCT IS           |

- **DATA_PRODUCT_SALES: PRODUCT SALES**

| COLUMN NAME  | COLUMN DESCRIPTION                                 |
|--------------|----------------------------------------------------|
| STORE_CODE   | STORE CODE                                         |
| PRODUCT_CODE | PRODUCT CODE                                       |
| DATE         | SALES DATE                                         |
| SALES_VALUE  | SALES VALUES                                       |
| SALES_QTY    | SALES QUANTITY                                     |

- **DATA_STORE_CAD: STORE INFO**

| COLUMN NAME  | COLUMN DESCRIPTION                                 |
|--------------|----------------------------------------------------|
| STORE_CODE   | STORE CODE                                         |
| STORE_NAME   | STORE NAME                                         |
| START_DATE   | SHOP OPENING DATE                                  |
| END_DATA     | SHOP CLOSING DATE                                  |
| BUSINESS_NAME| NAMES OF BUSINESS AREA RESPONSIBLE FOR THE SHOP    |
| BUSINESS_CODE| CODE OF BUSINESS AREA RESPONSIBLE FOR THE SHOP     |

- **DATA_STORE_SALES: SALES PER STORE**

| COLUMN NAME  | COLUMN DESCRIPTION                                 |
|--------------|----------------------------------------------------|
| STORE_CODE   | STORE CODE                                         |
| DATE         | COMMERCIAL DATE                                    |
| SALES_VALUE  | TOTAL VALUE OF SALES IN THAT DATE                  |
| SALES_QTY    | TOTAL QUANTITY OF SALES IN THAT DATE               |

## Challenge

### SQL test
1) How many products does the company have?
2) What are the 10 most expensive products in the company?
3) What sections do the 'BEBIDAS' and 'PADARIA' departments have?
4) When were the most products sold? In which store?
5) **Bonus!!** What was the sale of each business area in the first quarter of 2019? 

### Building your own visualization
1) Create at least one chart using the table IMDB_movies. The code must be in R or Python, and you are free to use any libraries, data and graphic format.

## Stack
- MySQL database 
- R/Python

## Submitting
- Send an e-mail to the person that you are in contact with in Looqbox!
- Your answer must have the queries and the visualization (you can use notebooks or regular code)

## Bonus points!
- Question 5 is a bonus question!
- Explain why you chose the visualization.

## Useful links
- [MySQL documentation](https://dev.mysql.com/doc/)
- [Data Visualization Catalogue](https://datavizcatalogue.com/)
