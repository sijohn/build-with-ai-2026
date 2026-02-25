# Supply Chain Agent Demo (Electronics Store)

Multi-agent ADK demo with:
- `orchestrator_agent` (root coordinator)
- `inventory_agent` (MCP toolbox + BigQuery)
- `document_intake_agent` (optional multimodal quote/proforma extraction)
- `finance_agent` (remote A2A server)
- `logistics_agent` (shipping options + execution)


## Project structure

```text
supply_chain_agent_demo/
  __init__.py
  agent.py
  sub_agents/
    inventory/agent.py
    logistics/agent.py
    finance/agent.py
    document_intake/agent.py
remote_agent/
  finance_agent/
    agent.py
    tools.py
mcp-toolbox/
  tools.yaml
sql/bigquery/
  01_create_tables.sql
  02_insert_test_data.sql
demo_assets/
  proforma_quote_alpha_retail.md
demo.md
```

## Prerequisites

- Python 3.10+
- `uv` installed
- Google Cloud access to project `<GCP_PROJECT_ID>`
- BigQuery permissions for dataset/table create + query
- ADC configured (`gcloud auth application-default login`) if using Vertex AI/BigQuery locally

## 1. Clone and install

```bash
git clone <YOUR_REPO_URL>
cd supply_chain_agent
uv sync
```

## 2. Environment setup

Create `.env` from template:

```bash
cp .env.example .env
```

Recommended runtime exports (from `how_to_run.txt`):

```bash
export TOOLBOX_URL=http://127.0.0.1:5100
export A2A_HOST=127.0.0.1
export A2A_PORT=8001
export GOOGLE_GENAI_USE_VERTEXAI=True
export GOOGLE_CLOUD_PROJECT=<GCP_PROJECT_ID>
export GOOGLE_CLOUD_LOCATION=us-central1
```

Note:
- BigQuery dataset/table location in this demo is `europe-north1`.
- The Vertex AI model location can still be `us-central1` as shown above.

## 3. BigQuery setup

Run these SQL files in BigQuery:

1. `supply_chain_agent/sql/bigquery/01_create_tables.sql`
2. `build-with-ai-2026/supply_chain_agent/sql/bigquery/02_insert_test_data.sql`

They create and seed:
- `inventory`
- `suppliers`
- `shipping_rates`
- `purchase_orders`
- `quote_documents`
- `quote_line_items`

## 4. Start services (3 terminals)

### Terminal 1: MCP toolbox server

```bash

export TOOLBOX_URL=http://127.0.0.1:5100
./toolbox --tools-file mcp-toolbox/tools.yaml --address 127.0.0.1 --port 5100
```

### Terminal 2: Remote finance A2A agent server

```bash

export A2A_HOST=127.0.0.1
export A2A_PORT=8001
export GOOGLE_GENAI_USE_VERTEXAI=True
export GOOGLE_CLOUD_PROJECT=<GCP_PROJECT_ID>
export GOOGLE_CLOUD_LOCATION=us-central1
uv run uvicorn remote_agent.finance_agent.agent:a2a_app --host 127.0.0.1 --port 8001
```

Agent card check:

```bash
curl http://localhost:8001/.well-known/agent-card.json
```

### Terminal 3: ADK web UI

```bash

export TOOLBOX_URL=http://127.0.0.1:5100
uv run adk web --port 8002
```

Open ADK UI and load package `supply_chain_agent_demo`.


## Troubleshooting

- If toolbox connection fails, verify `TOOLBOX_URL` matches actual toolbox port.
- If BigQuery calls fail, verify ADC auth and dataset permissions.
- If finance sub-agent fails, verify `http://localhost:8001/.well-known/agent-card.json` is reachable.
