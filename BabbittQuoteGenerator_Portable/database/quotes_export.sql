BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "insulators" (
	"id"	INTEGER,
	"code"	TEXT NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"description"	TEXT,
	"price_adder"	REAL DEFAULT 0.0,
	"max_temp_rating"	TEXT,
	"standard_length"	REAL DEFAULT 4.0,
	"compatible_models"	TEXT,
	"created_at"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "length_pricing" (
	"id"	INTEGER,
	"material_code"	TEXT NOT NULL,
	"model_family"	TEXT NOT NULL,
	"base_length"	REAL NOT NULL,
	"adder_per_foot"	REAL DEFAULT 0.0,
	"adder_per_inch"	REAL DEFAULT 0.0,
	"nonstandard_surcharge"	REAL DEFAULT 0.0,
	"nonstandard_threshold"	REAL DEFAULT 0.0,
	"created_at"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("material_code") REFERENCES "materials"("code")
);
CREATE TABLE IF NOT EXISTS "materials" (
	"id"	INTEGER,
	"code"	TEXT NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"description"	TEXT,
	"base_price_adder"	REAL DEFAULT 0.0,
	"length_adder_per_foot"	REAL DEFAULT 0.0,
	"length_adder_per_inch"	REAL DEFAULT 0.0,
	"nonstandard_length_surcharge"	REAL DEFAULT 0.0,
	"max_length_with_coating"	REAL,
	"compatible_models"	TEXT,
	"created_at"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "options" (
	"id"	INTEGER,
	"code"	TEXT NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"description"	TEXT,
	"price"	REAL NOT NULL,
	"price_type"	TEXT DEFAULT 'fixed',
	"category"	TEXT,
	"compatible_models"	TEXT,
	"exclusions"	TEXT,
	"created_at"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "product_models" (
	"id"	INTEGER,
	"model_number"	TEXT NOT NULL UNIQUE,
	"description"	TEXT NOT NULL,
	"base_price"	REAL NOT NULL,
	"base_length"	REAL NOT NULL DEFAULT 10.0,
	"default_voltage"	TEXT NOT NULL,
	"default_material"	TEXT NOT NULL,
	"default_insulator"	TEXT NOT NULL,
	"max_temp_rating"	TEXT,
	"max_pressure"	TEXT,
	"housing_type"	TEXT,
	"output_type"	TEXT,
	"application_notes"	TEXT,
	"created_at"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "quote_items" (
	"id"	INTEGER,
	"quote_id"	INTEGER NOT NULL,
	"part_number"	TEXT NOT NULL,
	"description"	TEXT,
	"quantity"	INTEGER DEFAULT 1,
	"unit_price"	REAL NOT NULL,
	"total_price"	REAL NOT NULL,
	"created_at"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("quote_id") REFERENCES "quotes"("id")
);
CREATE TABLE IF NOT EXISTS "quotes" (
	"id"	INTEGER,
	"quote_number"	TEXT NOT NULL UNIQUE,
	"customer_name"	TEXT,
	"customer_email"	TEXT,
	"status"	TEXT DEFAULT 'draft',
	"total_price"	REAL DEFAULT 0.0,
	"created_at"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	"updated_at"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "voltages" (
	"id"	INTEGER,
	"model_family"	TEXT NOT NULL,
	"voltage"	TEXT NOT NULL,
	"price_adder"	REAL DEFAULT 0.0,
	"is_default"	BOOLEAN DEFAULT 0,
	"created_at"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "insulators" VALUES (1,'U','UHMWPE','Ultra High Molecular Weight Polyethylene',0.0,'180F',4.0,'["LS2000"]','2025-07-07 04:39:17');
INSERT INTO "insulators" VALUES (2,'TEF','Teflon','Teflon Insulator',40.0,'450F',4.0,'["LS2100","LS6000","LS7000","LS7000/2","LS8000","LS8000/2","LT9000"]','2025-07-07 04:39:17');
INSERT INTO "insulators" VALUES (3,'DEL','Delrin','Delrin Insulator',0.0,'250F',4.0,'["LS6000","LS7500","LS8500"]','2025-07-07 04:39:17');
INSERT INTO "insulators" VALUES (4,'PEEK','PEEK','PEEK Insulator',120.0,'550F',4.0,'["LS6000","LS7000"]','2025-07-07 04:39:17');
INSERT INTO "insulators" VALUES (5,'CER','Ceramic','Ceramic Insulator',200.0,'800F',4.0,'["LS6000","LS7000"]','2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (1,'S','LS2000',10.0,45.0,3.75,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (2,'H','LS2000',10.0,110.0,9.17,300.0,72.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (3,'U','LS2000',4.0,0.0,40.0,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (4,'T','LS2000',4.0,0.0,50.0,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (5,'S','LS2100',10.0,45.0,3.75,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (6,'H','LS2100',10.0,110.0,9.17,300.0,72.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (7,'S','LS6000',10.0,45.0,3.75,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (8,'H','LS6000',10.0,110.0,9.17,300.0,72.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (9,'TS','LS6000',10.0,60.0,5.0,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (10,'CPVC','LS6000',4.0,0.0,50.0,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (11,'S','LS7000',10.0,45.0,3.75,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (12,'H','LS7000',10.0,110.0,9.17,300.0,72.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (13,'TS','LS7000',10.0,60.0,5.0,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (14,'CPVC','LS7000',4.0,0.0,50.0,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (15,'H','LS7000/2',10.0,110.0,9.17,300.0,72.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (16,'TS','LS7000/2',10.0,60.0,5.0,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (17,'S','LS8000',10.0,45.0,3.75,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (18,'H','LS8000',10.0,110.0,9.17,300.0,72.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (19,'TS','LS8000',10.0,60.0,5.0,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (20,'H','LS8000/2',10.0,110.0,9.17,300.0,72.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (21,'S','LS8000/2',10.0,45.0,3.75,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (22,'TS','LS8000/2',10.0,60.0,5.0,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (23,'H','LT9000',10.0,110.0,9.17,300.0,72.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (24,'TS','LT9000',10.0,60.0,5.0,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (25,'S','FS10000',6.0,45.0,3.75,0.0,0.0,'2025-07-07 04:39:17');
-- Exotic Materials
INSERT INTO "length_pricing" VALUES (26,'A','LS6000',10.0,75.0,6.25,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (27,'A','LS7000',10.0,75.0,6.25,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (28,'A','LS8000',10.0,75.0,6.25,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (29,'A','LT9000',10.0,75.0,6.25,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (30,'HC','LS6000',10.0,85.0,7.08,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (31,'HC','LS7000',10.0,85.0,7.08,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (32,'HC','LS8000',10.0,85.0,7.08,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (33,'HC','LT9000',10.0,85.0,7.08,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (34,'HB','LS6000',10.0,80.0,6.67,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (35,'HB','LS7000',10.0,80.0,6.67,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (36,'HB','LS8000',10.0,80.0,6.67,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (37,'HB','LT9000',10.0,80.0,6.67,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (38,'TT','LS6000',10.0,70.0,5.83,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (39,'TT','LS7000',10.0,70.0,5.83,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (40,'TT','LS8000',10.0,70.0,5.83,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "length_pricing" VALUES (41,'TT','LT9000',10.0,70.0,5.83,0.0,0.0,'2025-07-07 04:39:17');
INSERT INTO "materials" VALUES (1,'S','316 Stainless Steel','316 Stainless Steel Probe',0.0,45.0,3.75,0.0,999.0,'["LS2000","LS2100","LS6000","LS7000","LS8000","FS10000","LS7500","LS8500"]','2025-07-07 04:39:17');
INSERT INTO "materials" VALUES (2,'H','Halar Coated','Halar Coated Probe',110.0,110.0,9.17,300.0,72.0,'["LS2000","LS2100","LS6000","LS7000","LS7000/2","LS8000","LS8000/2","LT9000"]','2025-07-07 04:39:17');
INSERT INTO "materials" VALUES (3,'U','UHMWPE Blind End','UHMWPE Blind End Probe',20.0,0.0,40.0,0.0,999.0,'["LS2000"]','2025-07-07 04:39:17');
INSERT INTO "materials" VALUES (4,'T','Teflon Blind End','Teflon Blind End Probe',60.0,0.0,50.0,0.0,999.0,'["LS2000","LS2100"]','2025-07-07 04:39:17');
INSERT INTO "materials" VALUES (5,'TS','Teflon Sleeve','Teflon Sleeve Probe',80.0,60.0,5.0,0.0,999.0,'["LS2000","LS2100","LS6000","LS7000","LS7000/2","LS8000","LS8000/2","LT9000"]','2025-07-07 04:39:17');

INSERT INTO "materials" VALUES (7,'CPVC','CPVC Blind End','CPVC Blind End Probe with Integrated NPT Nipple',400.0,0.0,50.0,0.0,999.0,'["LS6000","LS7000"]','2025-07-07 04:39:17');
INSERT INTO "materials" VALUES (8,'A','Alloy 20','Alloy 20 Probe (Manual Pricing)',500.0,75.0,6.25,0.0,999.0,'["LS6000","LS7000","LS8000","LT9000"]','2025-07-07 04:39:17');
INSERT INTO "materials" VALUES (9,'HC','Hastelloy-C-276','Hastelloy-C-276 Probe (Manual Pricing)',600.0,85.0,7.08,0.0,999.0,'["LS6000","LS7000","LS8000","LT9000"]','2025-07-07 04:39:17');
INSERT INTO "materials" VALUES (10,'HB','Hastelloy-B','Hastelloy-B Probe (Manual Pricing)',580.0,80.0,6.67,0.0,999.0,'["LS6000","LS7000","LS8000","LT9000"]','2025-07-07 04:39:17');
INSERT INTO "materials" VALUES (11,'TT','Titanium','Titanium Probe (Manual Pricing)',450.0,70.0,5.83,0.0,999.0,'["LS6000","LS7000","LS8000","LT9000"]','2025-07-07 04:39:17');
INSERT INTO "options" VALUES (1,'XSP','Extra Static Protection','Extra Static Protection for plastic pellets/resins',30.0,'fixed','protection','["LS2000"]',NULL,'2025-07-07 04:39:17');
INSERT INTO "options" VALUES (2,'VR','Vibration Resistant','Vibration Resistant Construction',50.0,'fixed','protection','["LS2000","LS2100","LS6000","LS7000","LS8000"]',NULL,'2025-07-07 04:39:17');
INSERT INTO "options" VALUES (3,'BP','Bent Probe','Bent Probe Configuration',50.0,'fixed','probe','["LS2000","LS2100","LS6000","LS7000","LS8000","LT9000"]',NULL,'2025-07-07 04:39:17');

INSERT INTO "options" VALUES (5,'SST','Stainless Steel Tag','Stainless Steel Identification Tag',30.0,'fixed','other','["LS2000","LS2100","LS6000","LS7000","LS8000","LS8000/2","LT9000"]',NULL,'2025-07-07 04:39:17');
INSERT INTO "options" VALUES (6,'TEF','Teflon Insulator','Teflon Insulator (instead of standard)',40.0,'fixed','insulator','["LS2000","LS6000"]',NULL,'2025-07-07 04:39:17');
INSERT INTO "options" VALUES (7,'PEEK','PEEK Insulator','PEEK Insulator (550F rating)',120.0,'fixed','insulator','["LS6000","LS7000"]',NULL,'2025-07-07 04:39:17');
INSERT INTO "options" VALUES (8,'SSH','Stainless Steel Housing','Stainless Steel Housing (NEMA 4X)',285.0,'fixed','housing','["LS7000"]',NULL,'2025-07-07 04:39:17');
INSERT INTO "options" VALUES (9,'3QD','3/4" Diameter Probe','3/4" Diameter Probe (175 base + 175/foot)',175.0,'base_plus_per_foot','probe','["LS6000","LS7000"]','{"per_foot_price": 175.0}','2025-07-07 04:39:17');
INSERT INTO "product_models" VALUES (1,'LS2000','LS2000 Level Switch',425.0,10.0,'115VAC','S','U','180F','300 PSI','NEMA 7, C, D; NEMA 9, E, F, G','10 Amp SPDT Relay','Limited static protection. 24VDC option at no extra charge. 12VDC and 240VAC not available.','2025-07-07 04:39:17');
INSERT INTO "product_models" VALUES (2,'LS2100','LS2100 Loop Powered Level Switch',460.0,10.0,'24VDC','S','TEF','450F','300 PSI','NEMA 7, C, D; NEMA 9, E, F, G','8mA-16mA Loop Powered','Loop powered switch operates between 8mA and 16mA. 16-32 VDC operating range.','2025-07-07 04:39:17');
INSERT INTO "product_models" VALUES (3,'LS6000','LS6000 Level Switch',550.0,10.0,'115VAC','S','DEL','250F','1500 PSI','Explosion Proof Class I, Groups C & D','5 Amp DPDT Relay','Delrin insulators standard for SS probes. 3/4" NPT optional at no charge.','2025-07-07 04:39:17');
INSERT INTO "product_models" VALUES (4,'LS7000','LS7000 Level Switch',680.0,10.0,'115VAC','S','TEF','450F','1500 PSI','NEMA 7, D; NEMA 9, E, F, G','2 Form C contacts 5 Amp DPDT','On board timer available. 3/4" NPT optional at no charge.','2025-07-07 04:39:17');
INSERT INTO "product_models" VALUES (5,'LS7000/2','LS7000/2 Dual Point Level Switch',770.0,10.0,'115VAC','H','TEF','450F','1500 PSI','NEMA 7, D; NEMA 9, E, F, G','2 Form C contacts 5 Amp DPDT','Auto fill/empty only. Must use Halar probe in conductive liquids.','2025-07-07 04:39:17');
INSERT INTO "product_models" VALUES (6,'LS8000','LS8000 Remote Mounted Level Switch',715.0,10.0,'115VAC','S','TEF','450F','300 PSI','NEMA 7, C, D; NEMA 9, E, F, G','5 Amp DPDT Relay','Remote mounted system with transmitter/receiver. Multiple sensitivities available.','2025-07-07 04:39:17');
INSERT INTO "product_models" VALUES (7,'LS8000/2','LS8000/2 Remote Mounted Dual Point Switch',850.0,10.0,'115VAC','H','TEF','450F','300 PSI','NEMA 7, C, D; NEMA 9, E, F, G','10 Amp SPDT Relay','Remote dual point system. Extra transmitter available.','2025-07-07 04:39:17');
INSERT INTO "product_models" VALUES (8,'LT9000','LT9000 Level Transmitter',855.0,10.0,'115VAC','H','TEF','350F','1500 PSI','NEMA 7, D; NEMA 9, E, F, G','4-20mA','For electrically conductive liquids. Must be grounded to fluid.','2025-07-07 04:39:17');
INSERT INTO "product_models" VALUES (9,'FS10000','FS10000 Flow Switch',1980.0,6.0,'115VAC','S','TEF','450F','300 PSI','NEMA 7, C, D; NEMA 9, E, F, G','5 Amp DPDT Relay','Flow/No-flow detection. Max 24" probe length recommended.','2025-07-07 04:39:17');
INSERT INTO "product_models" VALUES (10,'LS7500','LS7500 Presence/Absence Switch',800.0,10.0,'115VAC','S','DEL','450F','150 PSI','NEMA 7, C, D; NEMA 9, E, F, G','2 Form C Contacts 5 Amp DPDT','Replacement for Princo L3515. Flange mounted.','2025-07-07 04:39:17');
INSERT INTO "product_models" VALUES (11,'LS8500','LS8500 Presence/Absence Switch',900.0,10.0,'115VAC','S','DEL','450F','150 PSI','NEMA 7, C, D; NEMA 9, E, F, G','2 Form C Contacts 5 Amp DPDT','Replacement for Princo L3545. Flange mounted.','2025-07-07 04:39:17');
-- Simplified Voltages Table - Core 4 voltages only
INSERT INTO "voltages" VALUES (1,'ALL','115VAC',0.0,1,'2025-07-07 04:39:17');
INSERT INTO "voltages" VALUES (2,'ALL','24VDC',0.0,0,'2025-07-07 04:39:17');
INSERT INTO "voltages" VALUES (3,'ALL','230VAC',0.0,0,'2025-07-07 04:39:17');
INSERT INTO "voltages" VALUES (4,'ALL','12VDC',0.0,0,'2025-07-07 04:39:17');
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
CREATE INDEX IF NOT EXISTS "idx_insulators_code" ON "insulators" (
	"code"
);
CREATE INDEX IF NOT EXISTS "idx_length_pricing_material_model" ON "length_pricing" (
	"material_code",
	"model_family"
);
CREATE INDEX IF NOT EXISTS "idx_materials_code" ON "materials" (
	"code"
);
CREATE INDEX IF NOT EXISTS "idx_options_category" ON "options" (
	"category"
);
CREATE INDEX IF NOT EXISTS "idx_options_code" ON "options" (
	"code"
);
CREATE INDEX IF NOT EXISTS "idx_product_models_model" ON "product_models" (
	"model_number"
);
CREATE INDEX IF NOT EXISTS "idx_quote_items_quote" ON "quote_items" (
	"quote_id"
);
CREATE INDEX IF NOT EXISTS "idx_quotes_number" ON "quotes" (
	"quote_number"
);
CREATE INDEX IF NOT EXISTS "idx_voltages_model_voltage" ON "voltages" (
	"model_family",
	"voltage"
);
COMMIT;
