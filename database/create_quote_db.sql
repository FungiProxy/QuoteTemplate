-- Quote Generator Database Schema
-- Simplified design focused on quote generation needs
-- Created from internal_data.txt and db7.2-1107.sql

-- Temporarily disable foreign keys for table recreation
PRAGMA foreign_keys = OFF;

-- Drop existing tables if they exist (in reverse dependency order)
DROP TABLE IF EXISTS quote_items;
DROP TABLE IF EXISTS quotes;
DROP TABLE IF EXISTS length_pricing;
DROP TABLE IF EXISTS process_connections;
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
    material_base_length REAL DEFAULT 10.0,
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

-- 6. PROCESS CONNECTIONS - All available process connection options
CREATE TABLE process_connections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,                    -- 'NPT', 'Flange', 'Tri-Clamp'
    size TEXT NOT NULL,                    -- '3/4"', '1"', '1-1/2"', '2"', '3"', '4"'
    material TEXT NOT NULL DEFAULT 'SS',   -- 'SS', 'CS' (Stainless Steel, Carbon Steel)
    rating TEXT,                           -- '150#', '300#' (for flanges only)
    price REAL DEFAULT 0.0,
    description TEXT,
    compatible_models TEXT,                -- JSON array of compatible models
    max_pressure TEXT,
    max_temperature TEXT,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 7. LENGTH PRICING - Length-based pricing rules
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

-- 8. QUOTES - Quote tracking (for future expansion)
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

-- 9. QUOTE ITEMS - Individual items in quotes
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

-- 10. SPARE PARTS - Replacement parts for all product models
CREATE TABLE spare_parts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    part_number TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    category TEXT, -- 'electronics', 'probe_assembly', 'housing', 'fuse', 'cable', 'card', 'transmitter', 'receiver'
    compatible_models TEXT, -- JSON array of compatible models
    notes TEXT,
    requires_voltage_spec BOOLEAN DEFAULT 0, -- True if voltage must be specified when ordering
    requires_length_spec BOOLEAN DEFAULT 0, -- True if length must be specified when ordering
    requires_sensitivity_spec BOOLEAN DEFAULT 0, -- True if sensitivity must be specified when ordering
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 11. PART_NUMBER_SHORTCUTS - User-defined shortcuts for common part numbers
CREATE TABLE part_number_shortcuts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shortcut TEXT NOT NULL UNIQUE,
    part_number TEXT NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_shortcut_alphanumeric CHECK (shortcut GLOB '[a-zA-Z0-9]*' AND LENGTH(shortcut) > 0)
);

-- 12. EMPLOYEES - Employee information for quote attribution
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    work_email TEXT NOT NULL UNIQUE,
    work_phone TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_email_format CHECK (work_email LIKE '%_@_%._%')
);

-- INDEXES for performance
CREATE INDEX idx_product_models_model ON product_models(model_number);
CREATE INDEX idx_materials_code ON materials(code);
CREATE INDEX idx_options_code ON options(code);
CREATE INDEX idx_options_category ON options(category);
CREATE INDEX idx_insulators_code ON insulators(code);
CREATE INDEX idx_process_connections_type ON process_connections(type);
CREATE INDEX idx_process_connections_size ON process_connections(size);
CREATE INDEX idx_process_connections_type_size ON process_connections(type, size);
CREATE INDEX idx_voltages_model_voltage ON voltages(model_family, voltage);
CREATE INDEX idx_length_pricing_material_model ON length_pricing(material_code, model_family);
CREATE INDEX idx_quotes_number ON quotes(quote_number);
CREATE INDEX idx_quote_items_quote ON quote_items(quote_id);
CREATE INDEX idx_spare_parts_part_number ON spare_parts(part_number);
CREATE INDEX idx_spare_parts_category ON spare_parts(category);
CREATE INDEX idx_part_number_shortcuts_shortcut ON part_number_shortcuts(shortcut);
CREATE INDEX idx_employees_email ON employees(work_email);
CREATE INDEX idx_employees_active ON employees(is_active);

-- POPULATE BASE MODELS
INSERT INTO product_models (model_number, description, base_price, base_length, default_voltage, default_material, default_insulator, default_process_connection_type, default_process_connection_material, default_process_connection_size, max_temp_rating, max_pressure, housing_type, output_type, application_notes) VALUES
('LS2000', 'LS2000 Level Switch', 455.00, 10.0, '115VAC', 'S', 'U', 'NPT', 'SS', '3/4"', '180F', '300 PSI', 'NEMA 7, C, D; NEMA 9, E, F, G', '10 Amp SPDT Relay', 'Limited static protection. 24VDC option at no extra charge. 12VDC and 240VAC not available.'),
('LS2100', 'LS2100 Loop Powered Level Switch', 520.00, 10.0, '24VDC', 'S', 'TEF', 'NPT', 'SS', '3/4"', '450F', '300 PSI', 'NEMA 7, C, D; NEMA 9, E, F, G', '8mA-16mA Loop Powered', 'Loop powered switch operates between 8mA and 16mA. 16-32 VDC operating range.'),
('LS6000', 'LS6000 Level Switch', 580.00, 10.0, '115VAC', 'S', 'DEL', 'NPT', 'SS', '1"', '250F', '1500 PSI', 'Explosion Proof Class I, Groups C & D', '5 Amp DPDT Relay', 'Delrin insulators standard for SS probes. 3/4" NPT optional at no charge.'),
('LS7000', 'LS7000 Level Switch', 715.00, 10.0, '115VAC', 'S', 'TEF', 'NPT', 'SS', '1"', '450F', '1500 PSI', 'NEMA 7, D; NEMA 9, E, F, G', '2 Form C contacts 5 Amp DPDT', 'On board timer available. 3/4" NPT optional at no charge.'),
('LS7000/2', 'LS7000/2 Dual Point Level Switch', 800.00, 10.0, '115VAC', 'H', 'TEF', 'NPT', 'SS', '1"', '450F', '1500 PSI', 'NEMA 7, D; NEMA 9, E, F, G', '2 Form C contacts 5 Amp DPDT', 'Auto fill/empty only. Must use Halar probe in conductive liquids.'),
('LS8000', 'LS8000 Remote Mounted Level Switch', 750.00, 10.0, '115VAC', 'S', 'TEF', 'NPT', 'SS', '3/4"', '450F', '300 PSI', 'NEMA 7, C, D; NEMA 9, E, F, G', '5 Amp DPDT Relay', 'Remote mounted system with transmitter/receiver. Multiple sensitivities available.'),
('LS8000/2', 'LS8000/2 Remote Mounted Dual Point Switch', 900.00, 10.0, '115VAC', 'H', 'TEF', 'NPT', 'SS', '3/4"', '450F', '300 PSI', 'NEMA 7, C, D; NEMA 9, E, F, G', '10 Amp SPDT Relay', 'Remote dual point system. Extra transmitter available.'),
('LT9000', 'LT9000 Level Transmitter', 950.00, 10.0, '115VAC', 'H', 'TEF', 'NPT', 'SS', '1"', '350F', '1500 PSI', 'NEMA 7, D; NEMA 9, E, F, G', '4-20mA', 'For electrically conductive liquids. Must be grounded to fluid.'),
('FS10000', 'FS10000 Flow Switch', 1920.00, 6.0, '115VAC', 'S', 'TEF', 'NPT', 'SS', '3/4"', '450F', '300 PSI', 'NEMA 7, C, D; NEMA 9, E, F, G', '5 Amp DPDT Relay', 'Flow/No-flow detection. Max 24" probe length recommended.'),
('LS7500FR', 'LS7500 Presence/Absence', 0.00, 10.0, '115VAC', 'S', 'DEL', 'Flange', 'SS', '1-1/2"', '450F', '150 PSI', 'NEMA 7, C, D; NEMA 9, E, F, G', '2 Form C Contacts 5 Amp DPDT', 'Replacement for Princo L3515. Flange mounted.'),
('LS8500FR', 'LS8500 Presence/Absence', 0.00, 10.0, '115VAC', 'S', 'DEL', 'Flange', 'SS', '1-1/2"', '450F', '150 PSI', 'NEMA 7, C, D; NEMA 9, E, F, G', '2 Form C Contacts 5 Amp DPDT', 'Replacement for Princo L3545. Flange mounted.');

-- POPULATE MATERIALS
INSERT INTO materials (code, name, description, base_price_adder, material_base_length, length_adder_per_foot, length_adder_per_inch, nonstandard_length_surcharge, max_length_with_coating, compatible_models) VALUES
('S', '316 Stainless Steel', '316 Stainless Steel Probe', 0.00, 10.0, 45.00, 0.00, 0.00, 999.0, 'ALL'),
('H', 'Halar Coated', 'Halar Coated Probe', 110.00, 10.0, 110.00, 0.00, 300.00, 999.0, 'ALL'),
('U', 'UHMWPE Blind End', 'UHMWPE Blind End Probe', 30.00, 4.0, 0.00, 40.00, 0.00, 999.0, 'ALL'),
('T', 'Teflon Blind End', 'Teflon Blind End Probe', 70.00, 4.0, 0.00, 50.00, 0.00, 999.0, 'ALL'),
('TS', 'Teflon Sleeve', 'Teflon Sleeve Probe', 80.00, 10.0, 60.00, 0.00, 0.00, 999.0, 'ALL'),
('CPVC', 'CPVC Blind End', 'CPVC Blind End Probe with Integrated NPT Nipple', 400.00, 4.0, 0.00, 50.00, 0.00, 999.0, 'ALL'),
('C', 'Cable', 'Cable Probe', 80.00, 12.0, 45.00, 0.00, 0.00, 999.0, 'ALL'),
('A20', 'Alloy 20', 'Alloy 20 Probe (Manual Pricing)', 0.00, 10.0, 0.00, 0.00, 0.00, 999.0, 'ALL'),
('HC', 'Hastelloy-C-276', 'Hastelloy-C-276 Probe (Manual Pricing)', 0.00, 10.0, 0.00, 0.00, 0.00, 999.0, 'ALL'),
('HB', 'Hastelloy-B', 'Hastelloy-B Probe (Manual Pricing)', 0.00, 10.0, 0.00, 0.00, 0.00, 999.0, 'ALL'),
('TIT', 'Titanium', 'Titanium Probe (Manual Pricing)', 0.00, 10.0, 0.00, 0.00, 0.00, 999.0, 'ALL');

-- POPULATE OPTIONS
INSERT INTO options (code, name, description, price, price_type, category, compatible_models, exclusions) VALUES
('XSP', 'Extra Static Protection', 'Extra Static Protection for plastic pellets/resins', 30.00, 'fixed', 'protection', 'ALL', NULL),
('VR', 'Vibration Resistant', 'Vibration Resistant Construction', 50.00, 'fixed', 'protection', 'ALL', NULL),
-- Bent Probe option removed - now handled as XDEG format in parser
('SSTAG', 'Stainless Steel Tag', 'Stainless Steel Identification Tag', 35.00, 'fixed', 'other', 'ALL', NULL),
-- TEF and PEEK removed from options - these are handled as insulators via XINS format
-- ('TEF', 'Teflon Insulator', 'Teflon Insulator (instead of standard)', 40.00, 'fixed', 'insulator', 'ALL', NULL),
-- ('PEEK', 'PEEK Insulator', 'PEEK Insulator (550F rating)', 120.00, 'fixed', 'insulator', 'ALL', NULL),
('SSHOUSING', 'Stainless Steel Housing', 'Stainless Steel Housing (NEMA 4X)', 285.00, 'fixed', 'housing', 'ALL', NULL),
('VRHOUSING', 'Epoxy Housing', 'Epoxy Housing (Chemical Resistant)', 150.00, 'fixed', 'housing', 'ALL', NULL),
('3/4"OD', '3/4" Diameter Probe', '3/4" Diameter Probe (175 base + 175/foot)', 175.00, 'base_plus_per_foot', 'probe', 'ALL', '{"per_foot_price": 175.0}');

-- POPULATE INSULATORS
INSERT INTO insulators (code, name, description, price_adder, max_temp_rating, compatible_models) VALUES
('U', 'UHMWPE', 'Ultra High Molecular Weight Polyethylene', 0.00, '180F', 'ALL'),
('TEF', 'Teflon', 'Teflon Insulator', 40.00, '450F', 'ALL'),
('DEL', 'Delrin', 'Delrin Insulator', 0.00, '250F', 'ALL'),
('PEEK', 'PEEK', 'PEEK Insulator', 120.00, '550F', 'ALL'),
('CER', 'Ceramic', 'Ceramic Insulator', 200.00, '800F', 'ALL');

-- POPULATE PROCESS CONNECTIONS
INSERT INTO process_connections (type, size, material, rating, price, description, compatible_models, notes) VALUES
-- NPT CONNECTIONS (Standard - No additional cost)
('NPT', '1/2"', 'SS', NULL, 70.0, '1/2" NPT Process Connection', 'ALL', 'Non-standard size - additional cost'),
('NPT', '3/4"', 'SS', NULL, 0.0, '3/4" NPT Process Connection', 'ALL', 'Most common size'),
('NPT', '1"', 'SS', NULL, 0.0, '1" NPT Process Connection', 'ALL', 'Heavy duty applications'),
('NPT', '1-1/2"', 'SS', NULL, 0.0, '1-1/2" NPT Process Connection', 'ALL', 'Large bore connection'),
('NPT', '2"', 'SS', NULL, 0.0, '2" NPT Process Connection', 'ALL', 'Large bore connection'),

-- FLANGE CONNECTIONS - 150# Rating
('Flange', '1"', 'SS', '150#', 0.0, '1" 150# RF Flange', 'ALL', 'Socket welded flange mounting'),
('Flange', '1-1/2"', 'SS', '150#', 0.0, '1-1/2" 150# RF Flange', 'ALL', 'Socket welded flange mounting'),
('Flange', '2"', 'SS', '150#', 0.0, '2" 150# RF Flange', 'ALL', 'Socket welded flange mounting'),
('Flange', '3"', 'SS', '150#', 0.0, '3" 150# RF Flange', 'ALL', 'Socket welded flange mounting'),
('Flange', '4"', 'SS', '150#', 0.0, '4" 150# RF Flange', 'ALL', 'Socket welded flange mounting'),

-- FLANGE CONNECTIONS - 300# Rating
('Flange', '1"', 'SS', '300#', 0.0, '1" 300# RF Flange', 'ALL', 'Socket welded flange mounting'),
('Flange', '1-1/2"', 'SS', '300#', 0.0, '1-1/2" 300# RF Flange', 'ALL', 'Socket welded flange mounting'),
('Flange', '2"', 'SS', '300#', 0.0, '2" 300# RF Flange', 'ALL', 'Socket welded flange mounting'),
('Flange', '3"', 'SS', '300#', 0.0, '3" 300# RF Flange', 'ALL', 'Socket welded flange mounting'),
('Flange', '4"', 'SS', '300#', 0.0, '4" 300# RF Flange', 'ALL', 'Socket welded flange mounting'),

-- FLANGE CONNECTIONS - Carbon Steel Options
('Flange', '1"', 'CS', '150#', 0.0, '1" 150# RF Flange - Carbon Steel', 'ALL', 'Socket welded flange mounting'),
('Flange', '1"', 'CS', '300#', 0.0, '1" 300# RF Flange - Carbon Steel', 'ALL', 'Socket welded flange mounting'),

-- TRI-CLAMP CONNECTIONS (Process connections only)
('Tri-Clamp', '1-1/2"', 'SS', NULL, 280.0, '1-1/2" Tri-Clamp Process Connection', 'ALL', 'Includes clamp and gasket'),
('Tri-Clamp', '2"', 'SS', NULL, 330.0, '2" Tri-Clamp Process Connection', 'ALL', 'Includes clamp and gasket');

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
('A20', 'LS6000', 10.0, 0.00, 0.00, 0.00, 0.0),
('A20', 'LS7000', 10.0, 0.00, 0.00, 0.00, 0.0),
('A20', 'LS8000', 10.0, 0.00, 0.00, 0.00, 0.0),
('A20', 'LT9000', 10.0, 0.00, 0.00, 0.00, 0.0),
('HC', 'LS6000', 10.0, 0.00, 0.00, 0.00, 0.0),
('HC', 'LS7000', 10.0, 0.00, 0.00, 0.00, 0.0),
('HC', 'LS8000', 10.0, 0.00, 0.00, 0.00, 0.0),
('HC', 'LT9000', 10.0, 0.00, 0.00, 0.00, 0.0),
('HB', 'LS6000', 10.0, 0.00, 0.00, 0.00, 0.0),
('HB', 'LS7000', 10.0, 0.00, 0.00, 0.00, 0.0),
('HB', 'LS8000', 10.0, 0.00, 0.00, 0.00, 0.0),
('HB', 'LT9000', 10.0, 0.00, 0.00, 0.00, 0.0),
('TIT', 'LS6000', 10.0, 0.00, 0.00, 0.00, 0.0),
('TIT', 'LS7000', 10.0, 0.00, 0.00, 0.00, 0.0),
('TIT', 'LS8000', 10.0, 0.00, 0.00, 0.00, 0.0),
('TIT', 'LT9000', 10.0, 0.00, 0.00, 0.00, 0.0);

-- POPULATE SPARE PARTS
INSERT INTO spare_parts (part_number, name, description, price, category, compatible_models, notes, requires_voltage_spec, requires_length_spec, requires_sensitivity_spec) VALUES
-- LS2000 SPARE PARTS
('LS2000-ELECTRONICS', 'LS2000 Electronics', 'LS2000 Electronics Assembly', 265.00, 'electronics', '["LS2000"]', 'Specify voltage when ordering', 1, 0, 0),
('LS2000-U-PROBE-ASSEMBLY-4', 'LS2000-U-Probe Assembly-4"', 'LS2000 UHMWPE Probe Assembly 4 inch', 210.00, 'probe_assembly', '["LS2000"]', NULL, 0, 0, 0),
('LS2000-T-PROBE-ASSEMBLY-4', 'LS2000-T-Probe Assembly-4"', 'LS2000 Teflon Probe Assembly 4 inch', 250.00, 'probe_assembly', '["LS2000"]', NULL, 0, 0, 0),
('LS2000-S-PROBE-ASSEMBLY-10', 'LS2000-S-Probe Assembly-10"', 'LS2000 Stainless Steel Probe Assembly 10 inch', 195.00, 'probe_assembly', '["LS2000"]', NULL, 0, 0, 0),
('LS2000-H-PROBE-ASSEMBLY-10', 'LS2000-H-Probe Assembly-10"', 'LS2000 Halar Coated Probe Assembly 10 inch', 320.00, 'probe_assembly', '["LS2000"]', NULL, 0, 0, 0),
('LS2000-HOUSING', 'LS2000 Housing', 'LS2000 Housing Assembly', 100.00, 'housing', '["LS2000"]', NULL, 0, 0, 0),

-- LS2100 SPARE PARTS
('LS2100-ELECTRONICS', 'LS2100 Electronics', 'LS2100 Electronics Assembly', 290.00, 'electronics', '["LS2100"]', NULL, 0, 0, 0),
('LS2100-S-PROBE-ASSEMBLY-10', 'LS2100-S-Probe Assembly-10"', 'LS2100 Stainless Steel Probe Assembly 10 inch', 230.00, 'probe_assembly', '["LS2100"]', NULL, 0, 0, 0),
('LS2100-H-PROBE-ASSEMBLY-10', 'LS2100-H-Probe Assembly-10"', 'LS2100 Halar Coated Probe Assembly 10 inch', 360.00, 'probe_assembly', '["LS2100"]', NULL, 0, 0, 0),
('LS2100-HOUSING', 'LS2100 Housing', 'LS2100 Housing Assembly', 100.00, 'housing', '["LS2100"]', NULL, 0, 0, 0),

-- LS6000 SPARE PARTS
('LS6000-ELECTRONICS', 'LS6000 Electronics', 'LS6000 Electronics Assembly', 295.00, 'electronics', '["LS6000"]', NULL, 0, 0, 0),
('LS6000-S-PROBE-ASSEMBLY-10', 'LS6000-S-Probe Assembly-10"', 'LS6000 Stainless Steel Probe Assembly 10 inch', 240.00, 'probe_assembly', '["LS6000"]', NULL, 0, 0, 0),
('LS6000-H-PROBE-ASSEMBLY-10', 'LS6000-H-Probe Assembly-10"', 'LS6000 Halar Coated Probe Assembly 10 inch', 370.00, 'probe_assembly', '["LS6000"]', NULL, 0, 0, 0),
('LS6000-HOUSING', 'LS6000 Housing', 'LS6000 Housing Assembly', 140.00, 'housing', '["LS6000"]', NULL, 0, 0, 0),
('LS6000-S-PROBE-ASSEMBLY-3/4-10', 'LS6000-S-Probe Assembly-3/4" Diameter-10"', 'LS6000 Stainless Steel 3/4" Diameter Probe Assembly 10 inch', 370.00, 'probe_assembly', '["LS6000"]', 'Add $175/ft for longer probes', 0, 1, 0),

-- LS7000 SPARE PARTS
('LS7000-PS-POWER-SUPPLY', 'LS7000-PS-Power Supply', 'LS7000 Power Supply', 230.00, 'electronics', '["LS7000", "LS7000/2"]', 'Specify voltage when ordering', 1, 0, 0),
('LS7000-SC-SENSING-CARD', 'LS7000-SC-Sensing Card', 'LS7000 Sensing Card', 235.00, 'card', '["LS7000"]', NULL, 0, 0, 0),
('LS7000-S-PROBE-ASSEMBLY-10', 'LS7000-S-Probe Assembly-10"', 'LS7000 Stainless Steel Probe Assembly 10 inch', 280.00, 'probe_assembly', '["LS7000"]', NULL, 0, 0, 0),
('LS7000-H-PROBE-ASSEMBLY-10', 'LS7000-H-Probe Assembly-10"', 'LS7000 Halar Coated Probe Assembly 10 inch', 370.00, 'probe_assembly', '["LS7000", "LS7000/2"]', NULL, 0, 0, 0),
('LS7000-HOUSING', 'LS7000 Housing', 'LS7000 Housing Assembly', 140.00, 'housing', '["LS7000", "LS7000/2"]', NULL, 0, 0, 0),
('LS7000-S-PROBE-ASSEMBLY-3/4-10', 'LS7000-S-Probe Assembly-3/4" Diameter-10"', 'LS7000 Stainless Steel 3/4" Diameter Probe Assembly 10 inch', 435.00, 'probe_assembly', '["LS7000"]', 'Add $175/ft for longer probes', 0, 1, 0),
('FUSE-1/2-AMP', 'Fuse (1/2 AMP)', '1/2 Amp Fuse', 10.00, 'fuse', '["LS7000", "LS7000/2", "LS8000", "LS8000/2", "LT9000"]', NULL, 0, 0, 0),

-- LS7000/2 SPARE PARTS
('LS7000/2-DP-DUAL-POINT-CARD', 'LS7000/2-DP Dual Point Card', 'LS7000/2 Dual Point Card', 255.00, 'card', '["LS7000/2"]', NULL, 0, 0, 0),

-- LS8000 SPARE PARTS
('LS8000-R-RECEIVER-CARD', 'LS8000-R-Receiver Card', 'LS8000 Receiver Card', 305.00, 'receiver', '["LS8000"]', 'Specify voltage when ordering', 1, 0, 0),
('LS8000-T-TRANSMITTER', 'LS8000-T-Transmitter', 'LS8000 Transmitter', 285.00, 'transmitter', '["LS8000", "LS8000/2"]', 'Specify size and sensitivity when ordering', 0, 0, 1),
('LS8000-S-PROBE-ASSEMBLY-10', 'LS8000-S-Probe Assembly-10"', 'LS8000 Stainless Steel Probe Assembly 10 inch', 230.00, 'probe_assembly', '["LS8000"]', NULL, 0, 0, 0),
('LS8000-H-PROBE-ASSEMBLY-10', 'LS8000-H-Probe Assembly-10"', 'LS8000 Halar Coated Probe Assembly 10 inch', 320.00, 'probe_assembly', '["LS8000", "LS8000/2"]', NULL, 0, 0, 0),
('LS8000-HOUSING', 'LS8000 Housing', 'LS8000 Housing Assembly', 100.00, 'housing', '["LS8000", "LS8000/2"]', NULL, 0, 0, 0),
('LS8000-S-PROBE-ASSEMBLY-3/4-10', 'LS8000-S-Probe Assembly-3/4" Diameter-10"', 'LS8000 Stainless Steel 3/4" Diameter Probe Assembly 10 inch', 445.00, 'probe_assembly', '["LS8000"]', 'Add $175/ft for longer probes', 0, 1, 0),
('LS8000-TRAN-EX-S-10', 'LS8000-TRAN-EX-S-10"', 'LS8000 Extra Transmitter with 3/4" Diameter Probe and Housing (No Receiver)', 565.00, 'transmitter', '["LS8000"]', 'Includes housing, probe assembly, and transmitter. Add $175/ft for longer probes', 0, 1, 0),

-- LS8000/2 SPARE PARTS
('LS8000/2-R-RECEIVER-CARD', 'LS8000/2-R-Receiver Card', 'LS8000/2 Receiver Card', 385.00, 'receiver', '["LS8000/2"]', 'Specify voltage when ordering', 1, 0, 0),

-- LT9000 SPARE PARTS
('LT9000-MA-PLUGIN-CARD', 'LT9000-MA (Plug-in card)', 'LT9000 MA Plug-in Card', 295.00, 'card', '["LT9000"]', NULL, 0, 0, 0),
('LT9000-BB-POWER-SUPPLY', 'LT9000-BB (Power Supply)', 'LT9000 BB Power Supply', 295.00, 'electronics', '["LT9000"]', 'Specify voltage when ordering', 1, 0, 0),
('LT9000-H-PROBE-ASSEMBLY-10', 'LT9000-H-Probe Assembly-10"', 'LT9000 Halar Coated Probe Assembly 10 inch', 370.00, 'probe_assembly', '["LT9000"]', NULL, 0, 0, 0),
('LT9000-HOUSING', 'LT9000 Housing', 'LT9000 Housing Assembly', 140.00, 'housing', '["LT9000"]', NULL, 0, 0, 0),

-- FS10000 SPARE PARTS
('FS10000-ELECTRONICS', 'FS10000 Electronics', 'FS10000 Electronics Assembly', 1440.00, 'electronics', '["FS10000"]', 'Specify voltage when ordering', 1, 0, 0),
('FS10000-PROBE-ASSEMBLY-6', 'FS10000-Probe Assembly-6"', 'FS10000 Probe Assembly 6 inch', 200.00, 'probe_assembly', '["FS10000"]', 'Specify length when ordering', 0, 1, 0),
('FS10000-NEMA-4X-WINDOWED-ENCLOSURE', 'FS10000-NEMA 4X Windowed Enclosure', 'FS10000 NEMA 4X Windowed Enclosure', 300.00, 'housing', '["FS10000"]', NULL, 0, 0, 0),
('FS10000-REDDOT-GALB-2-OR', 'FS10000-REDDOT-GALB-2-OR', 'FS10000 Aluminum Probe Housing', 100.00, 'housing', '["FS10000"]', 'Aluminum Probe Housing', 0, 0, 0),
('FS10000-COAXIAL-CABLE-15FT', '15 Feet Coaxial Cable w/ Connectors', 'FS10000 15 Feet Coaxial Cable with Connectors', 100.00, 'cable', '["FS10000"]', NULL, 0, 0, 0);

-- POPULATE MODEL SHORTCUTS - Quick access to base models
INSERT INTO part_number_shortcuts (shortcut, part_number, description) VALUES
('2',  'LS2000-115VAC-S-10"',     'LS2000 Base Model'),
('21', 'LS2100-24VDC-S-10"',      'LS2100 Base Model'),
('6',  'LS6000-115VAC-S-10"',     'LS6000 Base Model'),
('7',  'LS7000-115VAC-S-10"',     'LS7000 Base Model'),
('72', 'LS7000/2-115VAC-H-10"',   'LS7000/2 Base Model'),
('75', 'LS7500FR-115VAC-S-10"',   'LS7500 Base Model'),
('8',  'LS8000-115VAC-S-10"',     'LS8000 Base Model'),
('82', 'LS8000/2-115VAC-H-10"',   'LS8000/2 Base Model'),
('85', 'LS8500FR-115VAC-S-10"',   'LS8500 Base Model'),
('9',  'LT9000-115VAC-H-10"',     'LT9000 Base Model'),
('10', 'FS10000-115VAC-S-6"',     'FS10000 Base Model');

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

-- Create a view for spare parts by model
CREATE VIEW spare_parts_by_model AS
SELECT 
    sp.part_number,
    sp.name,
    sp.description,
    sp.price,
    sp.category,
    sp.compatible_models,
    sp.notes,
    sp.requires_voltage_spec,
    sp.requires_length_spec,
    sp.requires_sensitivity_spec,
    CASE 
        WHEN sp.compatible_models LIKE '%LS2000%' THEN 'LS2000'
        WHEN sp.compatible_models LIKE '%LS2100%' THEN 'LS2100'
        WHEN sp.compatible_models LIKE '%LS6000%' THEN 'LS6000'
        WHEN sp.compatible_models LIKE '%LS7000/2%' THEN 'LS7000/2'
        WHEN sp.compatible_models LIKE '%LS7000%' THEN 'LS7000'
        WHEN sp.compatible_models LIKE '%LS8000/2%' THEN 'LS8000/2'
        WHEN sp.compatible_models LIKE '%LS8000%' THEN 'LS8000'
        WHEN sp.compatible_models LIKE '%LT9000%' THEN 'LT9000'
        WHEN sp.compatible_models LIKE '%FS10000%' THEN 'FS10000'
        ELSE 'MULTIPLE'
    END as primary_model
FROM spare_parts sp;

-- Re-enable foreign key constraints
PRAGMA foreign_keys = ON; 