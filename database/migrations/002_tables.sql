CREATE SCHEMA IF NOT EXISTS artefact;
CREATE SCHEMA IF NOT EXISTS extensions;
CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA extensions;

CREATE TABLE IF NOT EXISTS artefact.categories (
    category_id integer PRIMARY KEY, name text NOT NULL, description text NOT NULL
);
CREATE TABLE IF NOT EXISTS artefact.products (
    product_id integer PRIMARY KEY, price_brl numeric(12,2) NOT NULL CHECK (price_brl >= 0),
    name text NOT NULL, category_id integer NOT NULL REFERENCES artefact.categories,
    description text NOT NULL, stock_quantity integer NOT NULL CHECK (stock_quantity >= 0),
    status text NOT NULL CHECK (status IN ('active', 'discontinued', 'coming_soon')),
    specs jsonb NOT NULL, created_at date NOT NULL
);
CREATE TABLE IF NOT EXISTS artefact.promotions (
    promotion_id integer PRIMARY KEY, product_id integer NOT NULL REFERENCES artefact.products,
    discount_percent numeric(5,2) NOT NULL CHECK (discount_percent BETWEEN 0 AND 100),
    description text NOT NULL, is_active boolean NOT NULL
);
CREATE TABLE IF NOT EXISTS artefact.customers (
    customer_id integer PRIMARY KEY, name text NOT NULL, phone text NOT NULL,
    email text NOT NULL, city text NOT NULL
);
CREATE TABLE IF NOT EXISTS artefact.orders (
    order_id integer PRIMARY KEY, customer_id integer NOT NULL REFERENCES artefact.customers,
    order_date date NOT NULL, status text NOT NULL, total_brl numeric(12,2) NOT NULL,
    payment_method text NOT NULL, tracking_code text, estimated_delivery date, notes text
);
CREATE TABLE IF NOT EXISTS artefact.order_items (
    order_id integer NOT NULL REFERENCES artefact.orders,
    product_id integer NOT NULL REFERENCES artefact.products,
    quantity integer NOT NULL CHECK (quantity > 0), PRIMARY KEY (order_id, product_id)
);
CREATE TABLE IF NOT EXISTS artefact.policy_chunks (
    chunk_id text PRIMARY KEY, page integer NOT NULL, section text NOT NULL,
    content text NOT NULL, source_hash text NOT NULL, model text NOT NULL,
    embedding extensions.vector(1536) NOT NULL
);
REVOKE ALL ON ALL TABLES IN SCHEMA artefact FROM PUBLIC, anon, authenticated;
