from google.adk.agents import LlmAgent


def find_shipping_options(destination: str, total_weight_kg: float) -> list[dict]:
    """Return shipping options for a replenishment shipment."""
    options = [
        {
            "method": "Standard Ground",
            "eta_days": 5,
            "cost_usd": round(350 + (2.2 * total_weight_kg), 2),
            "destination": destination,
        },
        {
            "method": "Express Air",
            "eta_days": 1,
            "cost_usd": round(1200 + (5.5 * total_weight_kg), 2),
            "destination": destination,
        },
    ]
    return options


def execute_shipment(
    destination: str,
    shipping_method: str,
    quantity: int,
    item_name: str,
) -> dict:
    """Finalize shipment execution for the selected method."""
    return {
        "status": "scheduled",
        "destination": destination,
        "shipping_method": shipping_method,
        "quantity": quantity,
        "item_name": item_name,
        "tracking_reference": "ESC-TRACK-2026-001",
    }


GEMINI_2_5_FLASH = "gemini-2.5-flash"

logistics_agent = LlmAgent(
    name="logistics_agent",
    model=GEMINI_2_5_FLASH,
    description="Provides shipping options and executes replenishment shipment.",
    instruction="""
You are the logistics and shipping coordinator.

Use tools:
- find_shipping_options(destination, total_weight_kg)
- execute_shipment(destination, shipping_method, quantity, item_name)

Guidelines:
- Provide at least two options with ETA and cost.
- Ask user to choose one option before execution.
- Execute shipment only after explicit user confirmation.
""",
    tools=[find_shipping_options, execute_shipment],
)
