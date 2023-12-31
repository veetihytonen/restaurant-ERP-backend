CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role INT
);

CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    storage_category TEXT
);

CREATE TABLE warehouse_replenishments (
    id SERIAL PRIMARY KEY,
    vendor_name TEXT
);

CREATE TABLE ingredient_replenishments (
    id SERIAL PRIMARY KEY,
    replenishment_id INT REFERENCES warehouse_replenishments,
    ingredient_id INT REFERENCES ingredients,
    amount FLOAT,
    price_per_unit INT
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE product_versions (
    id SERIAL PRIMARY KEY,
    version_number INT,
    sale_price INT,
    product_id INT REFERENCES products
);

CREATE TABLE product_ingredient_mapping (
    id SERIAL PRIMARY KEY,
    product_version_id INT REFERENCES product_versions,
    ingredient_id INT REFERENCES ingredients,
    amount FLOAT
);

CREATE TABLE purchases (
    id SERIAL PRIMARY KEY
);

CREATE TABLE product_sales (
    id SERIAL PRIMARY KEY,
    purchase_id INT REFERENCES purchases,
    product_version_id INT REFERENCES product_versions,
    amount INT
);

CREATE TABLE ingredient_stock_updates (
    id SERIAL PRIMARY KEY,
    replenishment_id INT REFERENCES warehouse_replenishments,
    product_sale_id INT REFERENCES product_sales,
    ingredient_id INT REFERENCES ingredients,
    amount FLOAT
);
