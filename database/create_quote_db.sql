-- Quote Generator Database Schema
-- Simplified design focused on quote generation needs
-- Created from internal_data.txt and db7.2-1107.sql

PRAGMA foreign_keys = ON;

-- Drop existing tables if they exist
DROP TABLE IF EXISTS product_models;
DROP TABLE IF EXISTS materials;
DROP TABLE IF EXISTS options;
DROP TABLE IF EXISTS insulators;
DROP TABLE IF EXISTS voltages;
DROP TABLE IF EXISTS length_pricing;
DROP TABLE IF EXISTS quotes;
DROP TABLE IF EXISTS quote_items;

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
    standard_length REAL DEFAULT 4.0,
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
INSERT INTO product_models (model_number, description, base_price, base_length, default_voltage, default_material, default_insulator, max_temp_rating, max_pressure, housing_type, output_type, application_notes) VALUES
('LS2000', 'LS2000 Level Switch', 425.00, 10.0, '115VAC', 'S', 'U', '180F', '300 PSI', 'NEMA 7, C, D; NEMA 9, E, F, G', '10 Amp SPDT Relay', 'Limited static protection. 24VDC option at no extra charge. 12VDC and 240VAC not available.'),
('LS2100', 'LS2100 Loop Powered Level Switch', 460.00, 10.0, '24VDC', 'S', 'TEF', '450F', '300 PSI', 'NEMA 7, C, D; NEMA 9, E, F, G', '8mA-16mA Loop Powered', 'Loop powered switch operates between 8mA and 16mA. 16-32 VDC operating range.'),
('LS6000', 'LS6000 Level Switch', 550.00, 10.0, '115VAC', 'S', 'DEL', '250F', '1500 PSI', 'Explosion Proof Class I, Groups C & D', '5 Amp DPDT Relay', 'Delrin insulators standard for SS probes. 3/4" NPT optional at no charge.'),
('LS7000', 'LS7000 Level Switch', 680.00, 10.0, '115VAC', 'S', 'TEF', '450F', '1500 PSI', 'NEMA 7, D; NEMA 9, E, F, G', '2 Form C contacts 5 Amp DPDT', 'On board timer available. 3/4" NPT optional at no charge.'),
('LS7000/2', 'LS7000/2 Dual Point Level Switch', 770.00, 10.0, '115VAC', 'H', 'TEF', '450F', '1500 PSI', 'NEMA 7, D; NEMA 9, E, F, G', '2 Form C contacts 5 Amp DPDT', 'Auto fill/empty only. Must use Halar probe in conductive liquids.'),
('LS8000', 'LS8000 Remote Mounted Level Switch', 715.00, 10.0, '115VAC', 'S', 'TEF', '450F', '300 PSI', 'NEMA 7, C, D; NEMA 9, E, F, G', '5 Amp DPDT Relay', 'Remote mounted system with transmitter/receiver. Multiple sensitivities available.'),
('LS8000/2', 'LS8000/2 Remote Mounted Dual Point Switch', 850.00, 10.0, '115VAC', 'H', 'TEF', '450F', '300 PSI', 'NEMA 7, C, D; NEMA 9, E, F, G', '10 Amp SPDT Relay', 'Remote dual point system. Extra transmitter available.'),
('LT9000', 'LT9000 Level Transmitter', 855.00, 10.0, '115VAC', 'H', 'TEF', '350F', '1500 PSI', 'NEMA 7, D; NEMA 9, E, F, G', '4-20mA', 'For electrically conductive liquids. Must be grounded to fluid.'),
('FS10000', 'FS10000 Flow Switch', 1980.00, 6.0, '115VAC', 'S', 'TEF', '450F', '300 PSI', 'NEMA 7, C, D; NEMA 9, E, F, G', '5 Amp DPDT Relay', 'Flow/No-flow detection. Max 24" probe length recommended.'),
('LS7500', 'LS7500 Presence/Absence Switch', 800.00, 10.0, '115VAC', 'S', 'DEL', '450F', '150 PSI', 'NEMA 7, C, D; NEMA 9, E, F, G', '2 Form C Contacts 5 Amp DPDT', 'Replacement for Princo L3515. Flange mounted.'),
('LS8500', 'LS8500 Presence/Absence Switch', 900.00, 10.0, '115VAC', 'S', 'DEL', '450F', '150 PSI', 'NEMA 7, C, D; NEMA 9, E, F, G', '2 Form C Contacts 5 Amp DPDT', 'Replacement for Princo L3545. Flange mounted.');

-- POPULATE MATERIALS
INSERT INTO materials (code, name, description, base_price_adder, length_adder_per_foot, length_adder_per_inch, nonstandard_length_surcharge, max_length_with_coating, compatible_models) VALUES
('S', '316 Stainless Steel', '316 Stainless Steel Probe', 0.00, 45.00, 3.75, 0.00, 999.0, '["LS2000","LS2100","LS6000","LS7000","LS8000","FS10000","LS7500","LS8500"]'),
('H', 'Halar Coated', 'Halar Coated Probe', 110.00, 110.00, 9.17, 300.00, 72.0, '["LS2000","LS2100","LS6000","LS7000","LS7000/2","LS8000","LS8000/2","LT9000"]'),
('U', 'UHMWPE Blind End', 'UHMWPE Blind End Probe', 20.00, 40.00, 40.00, 0.00, 999.0, '["LS2000"]'),
('T', 'Teflon Blind End', 'Teflon Blind End Probe', 60.00, 50.00, 50.00, 0.00, 999.0, '["LS2000","LS2100"]'),
('TS', 'Teflon Sleeve', 'Teflon Sleeve Probe', 80.00, 60.00, 5.00, 0.00, 999.0, '["LS2000","LS2100","LS6000","LS7000","LS7000/2","LS8000","LS8000/2","LT9000"]'),
('C', 'Ceramic', 'Ceramic Probe', 150.00, 70.00, 5.83, 0.00, 999.0, '["LS6000","LS7000"]'),
('CPVC', 'CPVC Blind End', 'CPVC Blind End Probe with Integrated NPT Nipple', 400.00, 50.00, 50.00, 0.00, 999.0, '["LS6000","LS7000"]');

-- POPULATE OPTIONS
INSERT INTO options (code, name, description, price, price_type, category, compatible_models) VALUES
('XSP', 'Extra Static Protection', 'Extra Static Protection for plastic pellets/resins', 30.00, 'fixed', 'protection', '["LS2000"]'),
('VR', 'Vibration Resistant', 'Vibration Resistant Construction', 75.00, 'fixed', 'protection', '["LS2000","LS2100","LS6000","LS7000","LS8000"]'),
('BP', 'Bent Probe', 'Bent Probe Configuration', 50.00, 'fixed', 'probe', '["LS2000","LS2100","LS6000","LS7000","LS8000","LT9000"]'),
('CP', 'Cable Probe', 'Cable Probe Configuration', 80.00, 'fixed', 'probe', '["LS2000","LS2100","LS6000","LS7000","LS8000","LT9000"]'),
('SST', 'Stainless Steel Tag', 'Stainless Steel Identification Tag', 30.00, 'fixed', 'other', '["LS2000","LS2100","LS6000","LS7000","LS8000","LS8000/2","LT9000"]'),
('TEF', 'Teflon Insulator', 'Teflon Insulator (instead of standard)', 40.00, 'fixed', 'insulator', '["LS2000","LS6000"]'),
('PEEK', 'PEEK Insulator', 'PEEK Insulator (550F rating)', 120.00, 'fixed', 'insulator', '["LS6000","LS7000"]'),
('SSH', 'Stainless Steel Housing', 'Stainless Steel Housing (NEMA 4X)', 285.00, 'fixed', 'housing', '["LS7000"]'),
('3QD', '3/4" Diameter Probe', '3/4" Diameter Probe x 10"', 175.00, 'fixed', 'probe', '["LS6000","LS7000"]');

-- POPULATE INSULATORS
INSERT INTO insulators (code, name, description, price_adder, max_temp_rating, standard_length, compatible_models) VALUES
('U', 'UHMWPE', 'Ultra High Molecular Weight Polyethylene', 0.00, '180F', 4.0, '["LS2000"]'),
('TEF', 'Teflon', 'Teflon Insulator', 40.00, '450F', 4.0, '["LS2100","LS6000","LS7000","LS7000/2","LS8000","LS8000/2","LT9000"]'),
('DEL', 'Delrin', 'Delrin Insulator', 0.00, '250F', 4.0, '["LS6000","LS7500","LS8500"]'),
('PEEK', 'PEEK', 'PEEK Insulator', 120.00, '550F', 4.0, '["LS6000","LS7000"]'),
('CER', 'Ceramic', 'Ceramic Insulator', 200.00, '800F', 4.0, '["LS6000","LS7000"]');

-- POPULATE VOLTAGES
INSERT INTO voltages (model_family, voltage, price_adder, is_default) VALUES
('LS2000', '115VAC', 0.00, 1),
('LS2000', '24VDC', 0.00, 0),
('LS2100', '24VDC', 0.00, 1),
('LS6000', '115VAC', 0.00, 1),
('LS6000', '12VDC', 0.00, 0),
('LS6000', '24VDC', 0.00, 0),
('LS6000', '240VAC', 0.00, 0),
('LS7000', '115VAC', 0.00, 1),
('LS7000', '12VDC', 0.00, 0),
('LS7000', '24VDC', 0.00, 0),
('LS7000', '240VAC', 0.00, 0),
('LS7000/2', '115VAC', 0.00, 1),
('LS7000/2', '12VDC', 0.00, 0),
('LS7000/2', '24VDC', 0.00, 0),
('LS7000/2', '240VAC', 0.00, 0),
('LS8000', '115VAC', 0.00, 1),
('LS8000', '12VDC', 0.00, 0),
('LS8000', '24VDC', 0.00, 0),
('LS8000', '240VAC', 0.00, 0),
('LS8000/2', '115VAC', 0.00, 1),
('LS8000/2', '12VDC', 0.00, 0),
('LS8000/2', '24VDC', 0.00, 0),
('LS8000/2', '240VAC', 0.00, 0),
('LT9000', '115VAC', 0.00, 1),
('LT9000', '24VDC', 0.00, 0),
('LT9000', '230VAC', 0.00, 0),
('FS10000', '115VAC', 0.00, 1),
('FS10000', '12VDC', 0.00, 0),
('FS10000', '24VDC', 0.00, 0),
('FS10000', '240VAC', 0.00, 0),
('LS7500', '115VAC', 0.00, 1),
('LS7500', '12VDC', 0.00, 0),
('LS7500', '24VDC', 0.00, 0),
('LS7500', '220VAC', 0.00, 0),
('LS8500', '115VAC', 0.00, 1),
('LS8500', '12VDC', 0.00, 0),
('LS8500', '24VDC', 0.00, 0),
('LS8500', '220VAC', 0.00, 0);

-- POPULATE LENGTH PRICING
INSERT INTO length_pricing (material_code, model_family, base_length, adder_per_foot, adder_per_inch, nonstandard_surcharge, nonstandard_threshold) VALUES
('S', 'LS2000', 10.0, 45.00, 3.75, 0.00, 0.0),
('H', 'LS2000', 10.0, 110.00, 9.17, 300.00, 72.0),
('U', 'LS2000', 4.0, 0.00, 40.00, 0.00, 0.0),
('T', 'LS2000', 4.0, 0.00, 50.00, 0.00, 0.0),
('S', 'LS2100', 10.0, 45.00, 3.75, 0.00, 0.0),
('H', 'LS2100', 10.0, 110.00, 9.17, 300.00, 72.0),
('S', 'LS6000', 10.0, 45.00, 3.75, 0.00, 0.0),
('H', 'LS6000', 10.0, 110.00, 9.17, 300.00, 72.0),
('TS', 'LS6000', 10.0, 60.00, 5.00, 0.00, 0.0),
('CPVC', 'LS6000', 4.0, 0.00, 50.00, 0.00, 0.0),
('S', 'LS7000', 10.0, 45.00, 3.75, 0.00, 0.0),
('H', 'LS7000', 10.0, 110.00, 9.17, 300.00, 72.0),
('TS', 'LS7000', 10.0, 60.00, 5.00, 0.00, 0.0),
('CPVC', 'LS7000', 4.0, 0.00, 50.00, 0.00, 0.0),
('H', 'LS7000/2', 10.0, 110.00, 9.17, 300.00, 72.0),
('TS', 'LS7000/2', 10.0, 60.00, 5.00, 0.00, 0.0),
('S', 'LS8000', 10.0, 45.00, 3.75, 0.00, 0.0),
('H', 'LS8000', 10.0, 110.00, 9.17, 300.00, 72.0),
('TS', 'LS8000', 10.0, 60.00, 5.00, 0.00, 0.0),
('H', 'LS8000/2', 10.0, 110.00, 9.17, 300.00, 72.0),
('S', 'LS8000/2', 10.0, 45.00, 3.75, 0.00, 0.0),
('TS', 'LS8000/2', 10.0, 60.00, 5.00, 0.00, 0.0),
('H', 'LT9000', 10.0, 110.00, 9.17, 300.00, 72.0),
('TS', 'LT9000', 10.0, 60.00, 5.00, 0.00, 0.0),
('S', 'FS10000', 6.0, 45.00, 3.75, 0.00, 0.0);

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