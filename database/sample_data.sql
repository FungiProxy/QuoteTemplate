
-- Sample Data for Babbitt Quote Generator Testing
-- This file contains sample quotes and customer data for testing

-- Sample customers (not in main schema but useful for testing)
-- You can add this as a separate table if needed:
-- CREATE TABLE IF NOT EXISTS customers (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     name TEXT NOT NULL,
--     email TEXT,
--     phone TEXT,
--     address TEXT,
--     created_at DATETIME DEFAULT CURRENT_TIMESTAMP
-- );

-- Sample quotes for testing
INSERT OR IGNORE INTO quotes (quote_number, customer_name, customer_email, status, total_price, created_at, updated_at) VALUES
('BBT-2024-001', 'Acme Manufacturing', 'orders@acme.com', 'draft', 425.00, '2024-01-15 10:30:00', '2024-01-15 10:30:00'),
('BBT-2024-002', 'Industrial Solutions Inc', 'purchasing@industrial.com', 'sent', 570.00, '2024-01-16 14:20:00', '2024-01-16 14:20:00'),
('BBT-2024-003', 'Chemical Processing LLC', 'orders@chemproc.com', 'approved', 1285.00, '2024-01-17 09:15:00', '2024-01-18 16:45:00');

-- Sample quote items
INSERT OR IGNORE INTO quote_items (quote_id, part_number, description, quantity, unit_price, total_price, created_at) VALUES
(1, 'LS2000-115VAC-S-10"', 'LS2000 Level Switch, 115VAC, Stainless Steel, 10" probe', 1, 425.00, 425.00, '2024-01-15 10:30:00'),
(2, 'LS2000-115VAC-S-10"-XSP-VR-8"TEFINS', 'LS2000 Level Switch with Extra Static Protection, Vibration Resistant, 8" Teflon Insulator', 1, 570.00, 570.00, '2024-01-16 14:20:00'),
(3, 'LS7000-115VAC-H-18"-CP-SST', 'LS7000 Level Switch, 115VAC, Halar Coated, 18" probe, Cable Probe, Stainless Steel Tag', 2, 642.50, 1285.00, '2024-01-17 09:15:00');

-- Test part numbers that should work
-- LS2000-115VAC-S-10"               -- Basic LS2000
-- LS2000-115VAC-S-10"-XSP           -- With extra static protection  
-- LS2100-24VDC-H-12"                -- LS2100 with Halar
-- LS6000-115VAC-S-14"-1"NPT         -- LS6000 with NPT connection
-- LS7000-115VAC-H-18"-TEF           -- LS7000 with Teflon insulator
-- LS8000-115VAC-S-24"-CP-SST        -- LS8000 with cable probe and SS tag

-- Test part numbers that should fail validation
-- LS2000-12VDC-S-10"                -- 12VDC not available for LS2000
-- LS2100-115VAC-S-10"               -- 115VAC not available for LS2100  
-- LS2000-115VAC-H-80"               -- Halar over 72" limit
-- LS2000-115VAC-S-10"-CP-BP         -- Cable probe and bent probe incompatible
