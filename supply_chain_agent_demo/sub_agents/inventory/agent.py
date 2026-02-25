import os

from google.adk.agents import LlmAgent
from toolbox_core import ToolboxSyncClient

GEMINI_2_5_FLASH = "gemini-2.5-flash"

# MCP Toolbox endpoint (default local run).
toolbox_url = os.getenv("TOOLBOX_URL", "http://localhost:5000")
tools = []
toolbox_error = None
toolbox = None
try:
    toolbox = ToolboxSyncClient(toolbox_url)
    tools = toolbox.load_toolset("inventory_toolset")
except Exception as exc:
    toolbox_error = str(exc)
    if toolbox is not None:
        try:
            toolbox.close()
        except Exception:
            pass

inventory_agent = LlmAgent(
    name="inventory_agent",
    model=GEMINI_2_5_FLASH,
    description="Checks inventory, fetches item details, and calculates restock cost.",
    instruction="""
You are an inventory management agent for an electronics store.

Use tools from MCP toolbox:
- get_inventory_levels: check available quantity for an item.
- get_item_details: fetch item metadata and pricing.
- calculate_total_cost: calculate total cost for ordering quantity of an item.

Behavior:
- Ask clarifying questions only if item identity or quantity is missing.
- Return concise, structured answers with quantity, unit_price, and total_cost when relevant.
"""
    + (
        f"""

Runtime note:
- MCP toolbox is currently unavailable at `{toolbox_url}`.
- Last error: {toolbox_error}
- Tell the user tools are unavailable and ask them to retry after toolbox/auth is fixed.
"""
        if toolbox_error
        else ""
    ),
    tools=tools,
)
