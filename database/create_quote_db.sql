-- Quote Generator Database Schema
-- Simplified design focused on quote generation needs
-- Created from internal_data.txt and db7.2-1107.sql

-- Temporarily disable foreign keys for table recreation
PRAGMA foreign_keys = OFF;

-- Drop existing tables if they exist (in reverse dependency order)
DROP TABLE IF EXISTS quote_items;
DROP TABLE IF EXISTS quotes;
DROP TABLE IF EXISTS length_pricing;
DROP TABLE IF EXISTS voltages;
DROP TABLE IF EXISTS insulators;
DROP TABLE IF EXISTS options;
DROP TABLE IF EXISTS materials;
DROP TABLE IF EXISTS product_models;

-- 1. PRODUCT MODELS - Base models (LS2000, LS2100, etc.)
CREATE TABLE product_models (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_number TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    base_price REAL NOT NULL,
    base_length REAL NOT NULL DEFAULT 10.0,
    default_voltage TEXT NOT NULL,
    default_material TEXT NOT NULL,
    default_insulator TEXT NOT NULL,
    default_process_connection_type TEXT NOT NULL,
    default_process_connection_material TEXT NOT NULL,
    default_process_connection_size TEXT NOT NULL,
    max_temp_rating TEXT,
    max_pressure TEXT,
    housing_type TEXT,
    output_type TEXT,
    application_notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. MATERIALS - Material codes with pricing
CREATE TABLE materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    base_price_adder REAL DEFAULT 0.0,
    length_adder_per_foot REAL DEFAULT 0.0,
    length_adder_per_inch REAL DEFAULT 0.0,
    nonstandard_length_surcharge REAL DEFAULT 0.0,
    max_length_with_coating REAL,
    compatible_models TEXT, -- JSON array of compatible models
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. OPTIONS - Option codes with pricing
CREATE TABLE options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    price_type TEXT DEFAULT 'fixed', -- 'fixed', 'per_inch', 'per_foot'
    category TEXT, -- 'insulator', 'connection', 'protection', 'probe', 'other'
    compatible_models TEXT, -- JSON array of compatible models
    exclusions TEXT, -- JSON array of incompatible options
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 4. INSULATORS - Insulator materials with pricing and specs
CREATE TABLE insulators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    price_adder REAL DEFAULT 0.0,
    max_temp_rating TEXT,
    compatible_models TEXT, -- JSON array of compatible models
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 5. VOLTAGES - Available voltages for each model
CREATE TABLE voltages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_family TEXT NOT NULL,
    voltage TEXT NOT NULL,
    price_adder REAL DEFAULT 0.0,
    is_default BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 6. LENGTH PRICING - Length-based pricing rules
CREATE TABLE length_pricing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    material_code TEXT NOT NULL,
    model_family TEXT NOT NULL,
    base_length REAL NOT NULL,
    adder_per_foot REAL DEFAULT 0.0,
    adder_per_inch REAL DEFAULT 0.0,
    nonstandard_surcharge REAL DEFAULT 0.0,
    nonstandard_threshold REAL DEFAULT 0.0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (material_code) REFERENCES materials(code)
);

-- 7. QUOTES - Quote tracking (for future expansion)
CREATE TABLE quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote_number TEXT NOT NULL UNIQUE,
    customer_name TEXT,
    customer_email TEXT,
    status TEXT DEFAULT 'draft',
    total_price REAL DEFAULT 0.0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 8. QUOTE ITEMS - Individual items in quotes
CREATE TABLE quote_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote_id INTEGER NOT NULL,
    part_number TEXT NOT NULL,
    description TEXT,
    quantity INTEGER DEFAULT 1,
    unit_price REAL NOT NULL,
    total_price REAL NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (quote_id) REFERENCES quotes(id)
);

-- INDEXES for performance
CREATE INDEX idx_product_models_model ON product_models(model_number);
CREATE INDEX idx_materials_code ON materials(code);
CREATE INDEX idx_options_code ON options(code);
CREATE INDEX idx_options_category ON options(category);
CREATE INDEX idx_insulators_code ON insulators(code);
CREATE INDEX idx_voltages_model_voltage ON voltages(model_family, voltage);
CREATE INDEX idx_length_pricing_material_model ON length_pricing(material_code, model_family);
CREATE INDEX idx_quotes_number ON quotes(quote_number);
CREATE INDEX idx_quote_items_quote ON quote_items(quote_id);

-- POPULATE BASE MODELS
INSERT INTO product_models (model_number, description, base_price, base_length, default_voltage, default_material, default_insulator, default_process_connection_type, default_process_connection_material, default_process_connection_size, max_temp_rating, max_pressure, housing_type, output_type, application_notes) VALUES
('LS2000', 'LS2000 Level Switch', 455.00, 10.0, '115VAC', 'S', 'U', 'NPT', 'SS', '3/4"', '180F', '300 PSI', 'NEMA 7, C, D; NEMA 9, E, F, G', '10 Amp SPDT Relay', 'Limited static protection. 24VDC option at no extra charge. 12VDC and 240VAC not available.'),
('LS2100', 'LS2100 Loop Powered Level Switch', 480.00, 10.0, '24VDC', 'S', 'TEF', 'NPT', 'SS', '3/4"', '450F', '300 PSI', 'NEMA 7, C, D; NEMA 9, E, F, G', '8mA-16mA Loop Powered', 'Loop powered switch operates between 8mA and 16mA. 16-32 VDC operating range.'),
('LS6000', 'LS6000 Level Switch', 580.00, 10.0, '115VAC', 'S', 'DEL', 'NPT', 'SS', '1"', '250F', '1500 PSI', 'Explosion Proof Class I, Groups C & D', '5 Amp DPDT Relay', 'Delrin insulators standard for SS probes. 3/4" NPT optional at no charge.'),
('LS7000', 'LS7000 Level Switch', 715.00, 10.0, '115VAC', 'S', 'TEF', 'NPT', 'SS', '1"', '450F', '1500 PSI', 'NEMA 7, D; NEMA 9, E, F, G', '2 Form C contacts 5 Amp DPDT', 'On board timer available. 3/4" NPT optional at no charge.'),
('LS7000/2', 'LS7000/2 Dual Point Level Switch', 800.00, 10.0, '115VAC', 'H', 'TEF', 'NPT', 'SS', '1"', '450F', '1500 PSI', 'NEMA 7, D; NEMA 9, E, F, G', '2 Form C contacts 5 Amp DPDT', 'Auto fill/empty only. Must use Halar probe in conductive liquids.'),
('LS8000', 'LS8000 Remote Mounted Level Switch', 750.00, 10.0, '115VAC', 'S', 'TEF', 'NPT', 'SS', '3/4"', '450F', '300 PSI', 'NEMA 7, C, D; NEMA 9, E, F, G', '5 Amp DPDT Relay', 'Remote mounted system with transmitter/receiver. Multiple sensitivities available.'),
('LS8000/2', 'LS8000/2 Remote Mounted Dual Point Switch', 900.00, 10.0, '115VAC', 'H', 'TEF', 'NPT', 'SS', '3/4"', '450F', '300 PSI', 'NEMA 7, C, D; NEMA 9, E, F, G', '10 Amp SPDT Relay', 'Remote dual point system. Extra transmitter available.'),
('LT9000', 'LT9000 Level Transmitter', 950.00, 10.0, '115VAC', 'H', 'TEF', 'NPT', 'SS', '1"', '350F', '1500 PSI', 'NEMA 7, D; NEMA 9, E, F, G', '4-20mA', 'For electrically conductive liquids. Must be grounded to fluid.'),
('FS10000', 'FS10000 Flow Switch', 1920.00, 6.0, '115VAC', 'S', 'TEF', 'NPT', 'SS', '3/4"', '450F', '300 PSI', 'NEMA 7, C, D; NEMA 9, E, F, G', '5 Amp DPDT Relay', 'Flow/No-flow detection. Max 24" probe length recommended.'),
('LS7500', 'LS7500 Presence/Absence Switch', 0.00, 10.0, '115VAC', 'S', 'DEL', 'Flange', 'SS', '1-1/2"', '450F', '150 PSI', 'NEMA 7, C, D; NEMA 9, E, F, G', '2 Form C Contacts 5 Amp DPDT', 'Replacement for Princo L3515. Flange mounted.'),
('LS8500', 'LS8500 Presence/Absence Switch', 0.00, 10.0, '115VAC', 'S', 'DEL', 'Flange', 'SS', '1-1/2"', '450F', '150 PSI', 'NEMA 7, C, D; NEMA 9, E, F, G', '2 Form C Contacts 5 Amp DPDT', 'Replacement for Princo L3545. Flange mounted.');

-- POPULATE MATERIALS
INSERT INTO materials (code, name, description, base_price_adder, length_adder_per_foot, length_adder_per_inch, nonstandard_length_surcharge, max_length_with_coating, compatible_models) VALUES
('S', '316 Stainless Steel', '316 Stainless Steel Probe', 0.00, 45.00, 0.00, 0.00, 999.0, 'ALL'),
('H', 'Halar Coated', 'Halar Coated Probe', 110.00, 110.00, 0.00, 300.00, 999.0, 'ALL'),
('U', 'UHMWPE Blind End', 'UHMWPE Blind End Probe', 20.00, 0.00, 40.00, 0.00, 999.0, 'ALL'),
('T', 'Teflon Blind End', 'Teflon Blind End Probe', 60.00, 0.00, 50.00, 0.00, 999.0, 'ALL'),
('TS', 'Teflon Sleeve', 'Teflon Sleeve Probe', 80.00, 60.00, 0.00, 0.00, 999.0, 'ALL'),
('CPVC', 'CPVC Blind End', 'CPVC Blind End Probe with Integrated NPT Nipple', 400.00, 0.00, 50.00, 0.00, 999.0, 'ALL'),
('C', 'Cable', 'Cable Probe', 80.00, 45.00, 0.00, 0.00, 999.0, 'ALL'),
('A', 'Alloy 20', 'Alloy 20 Probe (Manual Pricing)', 0.00, 0.00, 0.00, 0.00, 999.0, 'ALL'),
('HC', 'Hastelloy-C-276', 'Hastelloy-C-276 Probe (Manual Pricing)', 0.00, 0.00, 0.00, 0.00, 999.0, 'ALL'),
('HB', 'Hastelloy-B', 'Hastelloy-B Probe (Manual Pricing)', 0.00, 0.00, 0.00, 0.00, 999.0, 'ALL'),
('TT', 'Titanium', 'Titanium Probe (Manual Pricing)', 0.00, 0.00, 0.00, 0.00, 999.0, 'ALL');

-- POPULATE OPTIONS
INSERT INTO options (code, name, description, price, price_type, category, compatible_models, exclusions) VALUES
('XSP', 'Extra Static Protection', 'Extra Static Protection for plastic pellets/resins', 30.00, 'fixed', 'protection', 'ALL', NULL),
('VR', 'Vibration Resistant', 'Vibration Resistant Construction', 50.00, 'fixed', 'protection', 'ALL', NULL),
('BP', 'Bent Probe', 'Bent Probe Configuration', 50.00, 'fixed', 'probe', 'ALL', NULL),
('SST', 'Stainless Steel Tag', 'Stainless Steel Identification Tag', 30.00, 'fixed', 'other', 'ALL', NULL),
('TEF', 'Teflon Insulator', 'Teflon Insulator (instead of standard)', 40.00, 'fixed', 'insulator', 'ALL', NULL),
('PEEK', 'PEEK Insulator', 'PEEK Insulator (550F rating)', 120.00, 'fixed', 'insulator', 'ALL', NULL),
('SSH', 'Stainless Steel Housing', 'Stainless Steel Housing (NEMA 4X)', 285.00, 'fixed', 'housing', 'ALL', NULL),
('3QD', '3/4" Diameter Probe', '3/4" Diameter Probe (175 base + 175/foot)', 175.00, 'base_plus_per_foot', 'probe', 'ALL', '{"per_foot_price": 175.0}');

-- POPULATE INSULATORS
INSERT INTO insulators (code, name, description, price_adder, max_temp_rating, compatible_models) VALUES
('U', 'UHMWPE', 'Ultra High Molecular Weight Polyethylene', 0.00, '180F', 'ALL'),
('TEF', 'Teflon', 'Teflon Insulator', 40.00, '450F', 'ALL'),
('DEL', 'Delrin', 'Delrin Insulator', 0.00, '250F', 'ALL'),
('PEEK', 'PEEK', 'PEEK Insulator', 120.00, '550F', 'ALL'),
('CER', 'Ceramic', 'Ceramic Insulator', 200.00, '800F', 'ALL');

-- POPULATE VOLTAGES - Simplified to 4 core voltages
INSERT INTO voltages (model_family, voltage, price_adder, is_default) VALUES
('ALL', '115VAC', 0.00, 1),
('ALL', '24VDC', 0.00, 0),
('ALL', '230VAC', 0.00, 0),
('ALL', '12VDC', 0.00, 0);

-- POPULATE LENGTH PRICING
INSERT INTO length_pricing (material_code, model_family, base_length, adder_per_foot, adder_per_inch, nonstandard_surcharge, nonstandard_threshold) VALUES
('S', 'LS2000', 10.0, 45.00, 0.00, 0.00, 0.0),
('H', 'LS2000', 10.0, 110.00, 0.00, 300.00, 96.0),
('U', 'LS2000', 4.0, 0.00, 40.00, 0.00, 0.0),
('T', 'LS2000', 4.0, 0.00, 50.00, 0.00, 0.0),
('S', 'LS2100', 10.0, 45.00, 0.00, 0.00, 0.0),
('H', 'LS2100', 10.0, 110.00, 0.00, 300.00, 96.0),
('S', 'LS6000', 10.0, 45.00, 0.00, 0.00, 0.0),
('H', 'LS6000', 10.0, 110.00, 0.00, 300.00, 96.0),
('TS', 'LS6000', 10.0, 60.00, 0.00, 0.00, 0.0),
('CPVC', 'LS6000', 4.0, 0.00, 50.00, 0.00, 0.0),
('S', 'LS7000', 10.0, 45.00, 0.00, 0.00, 0.0),
('H', 'LS7000', 10.0, 110.00, 0.00, 300.00, 96.0),
('TS', 'LS7000', 10.0, 60.00, 0.00, 0.00, 0.0),
('CPVC', 'LS7000', 4.0, 0.00, 50.00, 0.00, 0.0),
('H', 'LS7000/2', 10.0, 110.00, 0.00, 300.00, 96.0),
('TS', 'LS7000/2', 10.0, 60.00, 0.00, 0.00, 0.0),
('S', 'LS8000', 10.0, 45.00, 0.00, 0.00, 0.0),
('H', 'LS8000', 10.0, 110.00, 0.00, 300.00, 96.0),
('TS', 'LS8000', 10.0, 60.00, 0.00, 0.00, 0.0),
('H', 'LS8000/2', 10.0, 110.00, 0.00, 300.00, 96.0),
('S', 'LS8000/2', 10.0, 45.00, 0.00, 0.00, 0.0),
('TS', 'LS8000/2', 10.0, 60.00, 0.00, 0.00, 0.0),
('H', 'LT9000', 10.0, 110.00, 0.00, 300.00, 96.0),
('TS', 'LT9000', 10.0, 60.00, 0.00, 0.00, 0.0),
('S', 'FS10000', 6.0, 45.00, 0.00, 0.00, 0.0),
-- Cable Material
('C', 'LS2000', 12.0, 45.00, 0.00, 0.00, 0.0),
('C', 'LS2100', 12.0, 45.00, 0.00, 0.00, 0.0),
('C', 'LS6000', 12.0, 45.00, 0.00, 0.00, 0.0),
('C', 'LS7000', 12.0, 45.00, 0.00, 0.00, 0.0),
('C', 'LS7000/2', 12.0, 45.00, 0.00, 0.00, 0.0),
('C', 'LS8000', 12.0, 45.00, 0.00, 0.00, 0.0),
('C', 'LS8000/2', 12.0, 45.00, 0.00, 0.00, 0.0),
('C', 'LT9000', 12.0, 45.00, 0.00, 0.00, 0.0),
('C', 'FS10000', 12.0, 45.00, 0.00, 0.00, 0.0),
-- Exotic Materials (zeroed out)
('A', 'LS6000', 10.0, 0.00, 0.00, 0.00, 0.0),
('A', 'LS7000', 10.0, 0.00, 0.00, 0.00, 0.0),
('A', 'LS8000', 10.0, 0.00, 0.00, 0.00, 0.0),
('A', 'LT9000', 10.0, 0.00, 0.00, 0.00, 0.0),
('HC', 'LS6000', 10.0, 0.00, 0.00, 0.00, 0.0),
('HC', 'LS7000', 10.0, 0.00, 0.00, 0.00, 0.0),
('HC', 'LS8000', 10.0, 0.00, 0.00, 0.00, 0.0),
('HC', 'LT9000', 10.0, 0.00, 0.00, 0.00, 0.0),
('HB', 'LS6000', 10.0, 0.00, 0.00, 0.00, 0.0),
('HB', 'LS7000', 10.0, 0.00, 0.00, 0.00, 0.0),
('HB', 'LS8000', 10.0, 0.00, 0.00, 0.00, 0.0),
('HB', 'LT9000', 10.0, 0.00, 0.00, 0.00, 0.0),
('TT', 'LS6000', 10.0, 0.00, 0.00, 0.00, 0.0),
('TT', 'LS7000', 10.0, 0.00, 0.00, 0.00, 0.0),
('TT', 'LS8000', 10.0, 0.00, 0.00, 0.00, 0.0),
('TT', 'LT9000', 10.0, 0.00, 0.00, 0.00, 0.0);

-- Create a view for easy price calculations
CREATE VIEW price_calculator AS
SELECT 
    pm.model_number,
    pm.base_price,
    pm.base_length,
    pm.default_voltage,
    pm.default_material,
    pm.default_insulator,
    m.name as material_name,
    m.length_adder_per_foot,
    m.length_adder_per_inch,
    m.nonstandard_length_surcharge,
    m.max_length_with_coating,
    i.name as insulator_name,
    i.price_adder as insulator_price_adder,
    i.max_temp_rating as insulator_temp_rating
FROM product_models pm
LEFT JOIN materials m ON pm.default_material = m.code
LEFT JOIN insulators i ON pm.default_insulator = i.code;

-- Re-enable foreign key constraints
PRAGMA foreign_keys = ON; 