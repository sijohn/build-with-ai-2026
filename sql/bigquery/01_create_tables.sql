-- Project: sm-gemini-playground
-- Region: europe-north1
-- Dataset: supply_chain

CREATE SCHEMA IF NOT EXISTS `<GCP_PROJECT_ID>.supply_chain`
OPTIONS (
  location = 'europe-north1',
  description = 'Supply chain demo dataset for ADK multi-agent workshop'
);

CREATE TABLE IF NOT EXISTS `<GCP_PROJECT_ID>.supply_chain.inventory` (
  item_id STRING NOT NULL,
  item_name STRING NOT NULL,
  category STRING,
  brand STRING,
  unit_price NUMERIC,
  quantity INT64,
  reorder_threshold INT64,
  supplier_id STRING,
  warehouse_location STRING,
  updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `<GCP_PROJECT_ID>.supply_chain.suppliers` (
  supplier_id STRING NOT NULL,
  supplier_name STRING NOT NULL,
  contact_email STRING,
  city STRING,
  country STRING,
  lead_time_days INT64
);

CREATE TABLE IF NOT EXISTS `<GCP_PROJECT_ID>.supply_chain.shipping_rates` (
  shipping_method STRING NOT NULL,
  carrier STRING NOT NULL,
  eta_days INT64,
  base_cost NUMERIC,
  per_kg_cost NUMERIC,
  region STRING,
  is_active BOOL
);

CREATE TABLE IF NOT EXISTS `<GCP_PROJECT_ID>.supply_chain.purchase_orders` (
  po_id STRING NOT NULL,
  item_id STRING NOT NULL,
  quantity INT64,
  unit_price NUMERIC,
  total_cost NUMERIC,
  status STRING,
  requested_by STRING,
  requested_at TIMESTAMP,
  approved_by STRING,
  approved_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `<GCP_PROJECT_ID>.supply_chain.quote_documents` (
  quote_id STRING NOT NULL,
  quote_date DATE,
  supplier_name STRING,
  customer_name STRING,
  currency STRING,
  subtotal_amount NUMERIC,
  tax_amount NUMERIC,
  total_amount NUMERIC,
  source_filename STRING,
  extracted_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `<GCP_PROJECT_ID>.supply_chain.quote_line_items` (
  quote_id STRING NOT NULL,
  line_number INT64,
  item_id STRING,
  item_name STRING,
  quantity INT64,
  unit_price NUMERIC,
  line_total NUMERIC
);
