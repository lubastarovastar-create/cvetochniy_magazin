CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL
);


CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    phone TEXT NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    total REAL NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);


-- Тестовые данные
INSERT INTO products (name, category, price, quantity)
SELECT 'Роза красная', 'Цветы', 250.00, 100
WHERE NOT EXISTS (SELECT 1 FROM products WHERE name = 'Роза красная');


INSERT INTO products (name, category, price, quantity)
SELECT 'Тюльпан жёлтый', 'Цветы', 150.00, 80
WHERE NOT EXISTS (SELECT 1 FROM products WHERE name = 'Тюльпан жёлтый');


INSERT INTO products (name, category, price, quantity)
SELECT 'Букет «Весенний»', 'Букеты', 1500.00, 20
WHERE NOT EXISTS (SELECT 1 FROM products WHERE name = 'Букет «Весенний»');


INSERT INTO products (name, category, price, quantity)
SELECT 'Композиция «Нежность»', 'Композиции', 2200.00, 15
WHERE NOT EXISTS (SELECT 1 FROM products WHERE name = 'Композиция «Нежность»');


INSERT INTO customers (full_name, phone)
SELECT 'Иванова Анна', '+7-900-111-22-33'
WHERE NOT EXISTS (SELECT 1 FROM customers WHERE phone = '+7-900-111-22-33');


INSERT INTO customers (full_name, phone)
SELECT 'Петров Сергей', '+7-900-444-55-66'
WHERE NOT EXISTS (SELECT 1 FROM customers WHERE phone = '+7-900-444-55-66');CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL
);


CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    phone TEXT NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    total REAL NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);


-- Тестовые данные
INSERT INTO products (name, category, price, quantity)
SELECT 'Роза красная', 'Цветы', 250.00, 100
WHERE NOT EXISTS (SELECT 1 FROM products WHERE name = 'Роза красная');


INSERT INTO products (name, category, price, quantity)
SELECT 'Тюльпан жёлтый', 'Цветы', 150.00, 80
WHERE NOT EXISTS (SELECT 1 FROM products WHERE name = 'Тюльпан жёлтый');


INSERT INTO products (name, category, price, quantity)
SELECT 'Букет «Весенний»', 'Букеты', 1500.00, 20
WHERE NOT EXISTS (SELECT 1 FROM products WHERE name = 'Букет «Весенний»');


INSERT INTO products (name, category, price, quantity)
SELECT 'Композиция «Нежность»', 'Композиции', 2200.00, 15
WHERE NOT EXISTS (SELECT 1 FROM products WHERE name = 'Композиция «Нежность»');


INSERT INTO customers (full_name, phone)
SELECT 'Иванова Анна', '+7-900-111-22-33'
WHERE NOT EXISTS (SELECT 1 FROM customers WHERE phone = '+7-900-111-22-33');


INSERT INTO customers (full_name, phone)
SELECT 'Петров Сергей', '+7-900-444-55-66'
WHERE NOT EXISTS (SELECT 1 FROM customers WHERE phone = '+7-900-444-55-66');
