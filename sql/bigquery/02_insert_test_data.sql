-- Test data for electronics-store supply chain demo.

INSERT INTO `<GCP_PROJECT_ID>.supply_chain.suppliers`
(supplier_id, supplier_name, contact_email, city, country, lead_time_days)
VALUES
('SUP-001', 'Nordic Power Systems', 'ops@nordicpower.example', 'Helsinki', 'Finland', 6),
('SUP-002', 'Baltic Device Components', 'sales@balticdevice.example', 'Tallinn', 'Estonia', 5),
('SUP-003', 'Scandi Cable Works', 'support@scandicable.example', 'Stockholm', 'Sweden', 4);

INSERT INTO `<GCP_PROJECT_ID>.supply_chain.inventory`
(item_id, item_name, category, brand, unit_price, quantity, reorder_threshold, supplier_id, warehouse_location, updated_at)
VALUES
('ELEC-CHG-65W', 'USB-C Fast Charger 65W', 'Chargers', 'VoltEdge', 50.00, 90, 120, 'SUP-001', 'EU-NORTH-WH1', CURRENT_TIMESTAMP()),
('ELEC-HDP-1000', 'Over-Ear Bluetooth Headphones', 'Audio', 'SonicPeak', 129.00, 40, 60, 'SUP-002', 'EU-NORTH-WH1', CURRENT_TIMESTAMP()),
('ELEC-MSE-WL', 'Wireless Mouse', 'Accessories', 'ClickPro', 25.00, 300, 150, 'SUP-003', 'EU-NORTH-WH2', CURRENT_TIMESTAMP()),
('ELEC-KBD-MECH', 'Mechanical Keyboard', 'Accessories', 'KeyForge', 85.00, 55, 80, 'SUP-003', 'EU-NORTH-WH2', CURRENT_TIMESTAMP()),
('ELEC-SSD-1TB', 'Portable SSD 1TB', 'Storage', 'DataSwift', 110.00, 35, 50, 'SUP-002', 'EU-NORTH-WH1', CURRENT_TIMESTAMP());

INSERT INTO `<GCP_PROJECT_ID>.supply_chain.shipping_rates`
(shipping_method, carrier, eta_days, base_cost, per_kg_cost, region, is_active)
VALUES
('Standard Ground', 'NordicParcel', 5, 350.00, 2.20, 'EU', TRUE),
('Express Air', 'SkyExpress', 1, 1200.00, 5.50, 'EU', TRUE);

INSERT INTO `<GCP_PROJECT_ID>.supply_chain.purchase_orders`
(po_id, item_id, quantity, unit_price, total_cost, status, requested_by, requested_at, approved_by, approved_at)
VALUES
('PO-2026-0001', 'ELEC-MSE-WL', 100, 25.00, 2500.00, 'APPROVED', 'store_manager', TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 10 DAY), 'finance_bot', TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 10 DAY)),
('PO-2026-0002', 'ELEC-SSD-1TB', 20, 110.00, 2200.00, 'PENDING', 'inventory_bot', TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY), NULL, NULL);


