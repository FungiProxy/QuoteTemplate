-- Customer Database Schema
-- Simple customer database with just company, contact, email, and phone
-- Created for QuoteTemplate application
-- 
-- NOTE: Phone numbers are stored as digits only (e.g., '1234567890')
-- The application automatically formats them for display as (123) 456-7890
-- Do not store formatted phone numbers in the database

-- Temporarily disable foreign keys for table recreation
PRAGMA foreign_keys = OFF;

-- Drop existing tables if they exist
DROP TABLE IF EXISTS customers;

-- CUSTOMERS - Simple customer information
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    contact_name TEXT,
    email TEXT,
    phone TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- INDEXES for performance
CREATE INDEX idx_customers_name ON customers(customer_name);
CREATE INDEX idx_customers_contact ON customers(contact_name);

-- TRIGGER for updated_at timestamp
CREATE TRIGGER update_customers_timestamp 
    AFTER UPDATE ON customers
    FOR EACH ROW
    BEGIN
        UPDATE customers SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

-- Re-enable foreign keys
PRAGMA foreign_keys = ON; 