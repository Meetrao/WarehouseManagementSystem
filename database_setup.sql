-- Warehouse Management System Database Schema
-- Run this script in MySQL to create the required database and tables

-- Create database
CREATE DATABASE IF NOT EXISTS warehouse_db;
USE warehouse_db;

-- Drop existing tables if they exist (in correct order due to foreign keys)
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS users;

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Suppliers table
CREATE TABLE suppliers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    contact_person VARCHAR(255),
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_company_name (company_name)
);

-- Products table
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    quantity INT NOT NULL DEFAULT 0,
    category VARCHAR(100),
    supplier VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_category (category),
    INDEX idx_supplier (supplier)
);

-- Orders table  
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    customer_phone VARCHAR(20),
    customer_address TEXT,
    total_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    status ENUM('Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled') DEFAULT 'Pending',
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_customer_name (customer_name),
    INDEX idx_status (status),
    INDEX idx_order_date (order_date)
);

-- Order items table
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT,
    INDEX idx_order_id (order_id),
    INDEX idx_product_id (product_id)
);

-- Insert default admin user (password: admin123)
INSERT INTO users (username, password, role) VALUES 
('admin', 'admin123', 'admin');

-- Sample suppliers
INSERT INTO suppliers (company_name, contact_person, phone, email, address) VALUES 
('TechSupplies Inc', 'John Smith', '+91-9876543210', 'john@techsupplies.com', '123 Tech Street, Mumbai, Maharashtra'),
('Global Electronics', 'Sarah Johnson', '+91-9876543211', 'sarah@globalelec.com', '456 Electronic Avenue, Delhi'),
('Office Solutions', 'Mike Wilson', '+91-9876543212', 'mike@officesol.com', '789 Business Park, Bangalore, Karnataka');

-- Sample products
INSERT INTO products (name, description, price, quantity, category, supplier) VALUES 
('Laptop Dell Inspiron 15', 'Dell Inspiron 15 3000 Series with Intel Core i5', 45000.00, 25, 'Electronics', 'TechSupplies Inc'),
('Office Chair Executive', 'High-back executive office chair with lumbar support', 8500.00, 50, 'Furniture', 'Office Solutions'),
('Wireless Mouse Logitech', 'Logitech M705 Marathon Wireless Mouse', 2500.00, 100, 'Electronics', 'TechSupplies Inc'),
('Printer HP LaserJet', 'HP LaserJet Pro M404dn Monochrome Printer', 18000.00, 15, 'Electronics', 'Global Electronics'),
('Desk Lamp LED', 'Adjustable LED desk lamp with USB charging port', 1200.00, 75, 'Furniture', 'Office Solutions'),
('External Hard Drive 1TB', 'Seagate Backup Plus Slim 1TB External HDD', 4500.00, 30, 'Electronics', 'TechSupplies Inc'),
('Office Desk Wooden', '4ft x 2ft wooden office desk with drawers', 12000.00, 20, 'Furniture', 'Office Solutions'),
('Webcam HD 1080p', 'Logitech C920 HD Pro Webcam', 6500.00, 40, 'Electronics', 'Global Electronics'),
('Keyboard Mechanical', 'Corsair K95 RGB Platinum Mechanical Keyboard', 15000.00, 12, 'Electronics', 'TechSupplies Inc'),
('Bookshelf 5-Tier', 'Wooden 5-tier bookshelf for office storage', 3500.00, 25, 'Furniture', 'Office Solutions');

-- Sample orders
INSERT INTO orders (customer_name, customer_phone, customer_address, total_amount, status, order_date) VALUES 
('Raj Patel', '+91-9988776655', 'A-101, Galaxy Apartments, Pune, Maharashtra', 47500.00, 'Delivered', '2024-11-15 10:30:00'),
('Priya Sharma', '+91-9988776656', 'B-205, Sunrise Complex, Mumbai, Maharashtra', 26500.00, 'Shipped', '2024-11-18 14:15:00'),
('Amit Kumar', '+91-9988776657', 'C-301, Tech Tower, Bangalore, Karnataka', 33000.00, 'Processing', '2024-11-20 09:45:00');

-- Sample order items (for the sample orders above)
-- Order 1 items
INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price) VALUES 
(1, 1, 1, 45000.00, 45000.00),  -- Laptop
(1, 3, 1, 2500.00, 2500.00);    -- Wireless Mouse

-- Order 2 items  
INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price) VALUES 
(2, 2, 2, 8500.00, 17000.00),   -- Office Chairs
(2, 4, 1, 18000.00, 18000.00),  -- Printer
(2, 5, 1, 1200.00, 1200.00);    -- Desk Lamp

-- Order 3 items
INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price) VALUES 
(3, 7, 2, 12000.00, 24000.00),  -- Office Desks
(3, 9, 1, 15000.00, 15000.00);  -- Mechanical Keyboard

-- Create indexes for better performance
CREATE INDEX idx_products_supplier ON products(supplier);
CREATE INDEX idx_orders_date_status ON orders(order_date, status);
CREATE INDEX idx_order_items_order_product ON order_items(order_id, product_id);

-- Create views
CREATE OR REPLACE VIEW order_summary AS
SELECT 
    o.id,
    o.customer_name,
    o.customer_phone,
    o.total_amount,
    o.status,
    o.order_date,
    COUNT(oi.id) as item_count,
    SUM(oi.quantity) as total_quantity
FROM orders o
LEFT JOIN order_items oi ON o.id = oi.order_id
GROUP BY o.id, o.customer_name, o.customer_phone, o.total_amount, o.status, o.order_date;

CREATE OR REPLACE VIEW inventory_status AS
SELECT 
    p.id,
    p.name,
    p.category,
    p.quantity,
    p.price,
    (p.quantity * p.price) as total_value,
    p.supplier,
    CASE 
        WHEN p.quantity = 0 THEN 'Out of Stock'
        WHEN p.quantity <= 5 THEN 'Critical'
        WHEN p.quantity <= 10 THEN 'Low Stock'
        ELSE 'In Stock'
    END as stock_status
FROM products p;

CREATE OR REPLACE VIEW supplier_performance AS
SELECT 
    s.company_name,
    s.contact_person,
    s.phone,
    s.email,
    COUNT(p.id) as product_count,
    SUM(p.quantity) as total_stock,
    SUM(p.quantity * p.price) as inventory_value
FROM suppliers s
LEFT JOIN products p ON s.company_name = p.supplier
GROUP BY s.id, s.company_name, s.contact_person, s.phone, s.email;

COMMIT;