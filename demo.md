# Demo Script Questions (Electronics Store)

Use these questions in ADK web to demonstrate orchestrator + inventory + finance(A2A) + logistics.

1. "How does the stock of USB-C Fast Charger 65W look right now?"
2. "I need to order 500 USB-C Fast Charger 65W units. What is the total cost?"
3. "Can you send this for finance approval?"
4. "Yes, I approve this expense."
5. "Show shipping options to Berlin, Germany for this replenishment."
6. "Choose Express Air and execute the shipment."
7. "Summarize the final outcome with item, order value, approval status, and shipment details."

## Optional variations

1. "Check stock for Over-Ear Bluetooth Headphones and suggest reorder quantity."
2. "Calculate cost for ordering 20 Portable SSD 1TB units."
3. "If below finance threshold, proceed directly to logistics."

## Full flow with quote/proforma upload (optional multimodal path)

This adds `document_intake_agent` before finance approval.

How does the stock of USB-C Fast Charger 65W look right now?
I need to order 500 USB-C Fast Charger 65W units. What is the total cost?
I am uploading a quote/proforma now. Extract details and save it.
Use quote id Q-ALPHA-2026-0001 and validate against item ELEC-CHG-65W, quantity 500, expected total 25000.
Can you send this for finance approval?
Yes, I approve this expense.
can you Show shipping options to Praterstraße 1, 1020 Vienna Austria for this replenishment.
Choose Express Air and execute the shipment.
Summarize the final outcome with item, order value, quote_id, quote match status, approval status, and shipment details.

## Demo quote/proforma sample

- Customer: Alpha Retail
- Quote Id: Q-ALPHA-2026-0001
- Item: ELEC-CHG-65W (USB-C Fast Charger 65W)
- Quantity: 500
- Unit Price: 50.00 USD
- Total: 25,000.00 USD

===========
Stock-monitoring automation detects an item below threshold.
Procurement agent calculates order value and ingests quote/proforma into the system.
Validation/approval agents check quote match and route to finance for human approval.
Logistics agent books shipping and executes fulfillment.
Summary agent publishes a final audit trail (item, quote ID, value, match result, approval, shipment).
You can describe the chat prompts as a demo interface, while the same actions can run via scheduled jobs, event triggers, or API-to-agent orchestration in production.