-- Table to store product details
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    product_url TEXT,
    created_date DATE,
    category TEXT
);

-- Table to store price history
CREATE TABLE IF NOT EXISTS price_history (
    price_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    initial_price REAL,
    current_price REAL,
    expected_discount REAL,
    updated_date DATE,
    currency TEXT,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
