
\c orders_db;

CREATE TABLE IF NOT EXISTS orders (
    order_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    product_id INT NOT NULL,  -- Missing comma here
    product TEXT NOT NULL,
    price FLOAT NOT NULL,
    store_id INT NOT NULL
);
