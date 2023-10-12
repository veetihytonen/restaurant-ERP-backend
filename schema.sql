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
    amount DECIMAL,
    price_per_unit INT
);

CREATE TABLE ingredient_stock_updates (
    id SERIAL PRIMARY KEY,
    replenishment_id INT REFERENCES warehouse_replenishments,
    purchase_id INT,
    ingredient_id INT REFERENCES ingredients,
    amount DECIMAL
);
