Assaf Sardi - An Interactive Docker-based Microservices System for operating a Supermarket.  Written in Python (FastAPI)

# Supermarket:

## Application Design:

- There are 2 microservices:
  - `purchase_service` - let customers purchase products
  - `owner_service` - let supermarket owner get the updated data about customers and products
- The database is PostgreSQL
  - Products table
    - product_name, unit_price
  - Purchases table
    - supermarket_id, timestamp, user_id, items_list, total_amount


## Instructions for how to run
- Inorder to load `products` and `purchases` data to the DB at application startup, place both `products_list.csv` and `purchases.csv` files in Supermarket/data directory

- Run with `docker-compose`
   ```shell
  docker-compose down
  docker-compose build
  docker-compose up
   ```

- Open http://localhost:8001/api/v1/customer/purchase in browser to purchase products


## HTTP Requests
### Customer
- `[GET]` http://localhost:8001/api/v1/customer/purchase
  - purchase products - interactive UI
- `[POST]` http://localhost:8001/api/v1/customer/purchase
  - purchase products - make the purchase and store in DB
- `[Get]` http://localhost:8001/api/v1/customer/supermarkets
  - get the supermarket branches
- `[Get]` http://localhost:8001/api/v1/customer/products
  - get the products
### Owner
- `[Get]` http://localhost:8002/api/v1/owner/dashboard
  - Owner dashboard - can call the following requests via interactive UI 
- `[Get]` http://localhost:8002/api/v1/owner/unique-customers
  - get the number of different customers
- `[Get]` http://localhost:8002/api/v1/owner/loyal-customers
  - get the customers who purchased at least 3 times
- `[Get]` http://localhost:8002/api/v1/owner/top-products
  - get the top 3 products. in case of a tie, return all of tied products


## Run Tests
Run in terminal:
  ```shell
    make test-all
  ```