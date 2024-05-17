-- Table to store product details
create table IF NOT EXISTS products
(
    product_id   INTEGER not null
        primary key autoincrement,
    product_name TEXT,
    product_url  TEXT,
    created_at   TIMESTAMP    not null,
    category     TEXT,
    updated_at   DATE    not null
);

-- Table to store price history
create table IF NOT EXISTS price_history
(
    id                INTEGER
        primary key autoincrement,
    product_id        INTEGER
        constraint price_history_products_id_fk
            references products,
    lowest_price      REAL,
    current_price     REAL      not null,
    expected_discount REAL,
    updated_at        TIMESTAMP default CURRENT_TIMESTAMP,
    currency          TEXT      not null,
    created_at        TIMESTAMP not null
);
