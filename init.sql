DROP TABLE IF EXISTS purchases;
DROP TABLE IF EXISTS products;

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) UNIQUE NOT NULL,
    unit_price NUMERIC NOT NULL
);

CREATE TABLE purchases (
    id SERIAL PRIMARY KEY,
    supermarket_id VARCHAR(10),
    timestamp TIMESTAMP NOT NULL,
    user_id UUID NOT NULL,
    items_list TEXT NOT NULL,
    total_amount NUMERIC NOT NULL
);