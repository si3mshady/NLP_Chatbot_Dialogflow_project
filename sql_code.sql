-- Table to store food items
CREATE TABLE food_items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

-- Sample food items data
INSERT INTO food_items (name, price) VALUES
    ('Donut', 2.50),
    ('Pigs in a Blanket', 4.00),
    ('Burrito', 5.50),
    ('Shake', 3.00),
    ('Sandwich', 4.50),
    ('Pancake', 3.25);

-- Table to store orders
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,  -- Unique session ID for each order
    item_id INT REFERENCES food_items(id),
    quantity INT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample order data (for reference, you can insert orders when they are placed)
-- INSERT INTO orders (session_id, item_id, quantity) VALUES
--     ('session_1', 1, 2),
--     ('session_1', 3, 1),
--     ('session_2', 2, 3);

-- Index to improve query performance
CREATE INDEX idx_session_id ON orders (session_id);

-- Function to calculate total cost for an order
CREATE OR REPLACE FUNCTION calculate_total_cost(order_id INT)
RETURNS DECIMAL(10, 2) AS $$
DECLARE
    total DECIMAL(10, 2) := 0;
BEGIN
    SELECT SUM(oi.quantity * fi.price)
    INTO total
    FROM orders oi
    JOIN food_items fi ON oi.item_id = fi.id
    WHERE oi.id = order_id;

    RETURN total;
END;
$$ LANGUAGE plpgsql;

-- Function to get the current order for a session
CREATE OR REPLACE FUNCTION get_current_order(session_id VARCHAR(255))
RETURNS TABLE (
    item_name VARCHAR(255),
    quantity INT,
    total_cost DECIMAL(10, 2)
) AS $$
BEGIN
    RETURN QUERY SELECT fi.name, oi.quantity, (oi.quantity * fi.price) AS total_cost
    FROM orders oi
    JOIN food_items fi ON oi.item_id = fi.id
    WHERE oi.session_id = session_id;
END;
$$ LANGUAGE plpgsql;

-- Function to get order details by order ID
CREATE OR REPLACE FUNCTION get_order_details(order_id INT)
RETURNS TABLE (
    item_name VARCHAR(255),
    quantity INT,
    total_cost DECIMAL(10, 2)
) AS $$
BEGIN
    RETURN QUERY SELECT fi.name, oi.quantity, (oi.quantity * fi.price) AS total_cost
    FROM orders oi
    JOIN food_items fi ON oi.item_id = fi.id
    WHERE oi.id = order_id;
END;
$$ LANGUAGE plpgsql;
