import os
from typing import List

from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from toolbox_core import ToolboxSyncClient

GEMINI_2_5_FLASH = "gemini-2.5-flash"


class QuoteLineItem(BaseModel):
    line_number: int = Field(description="Line number from the quote/proforma.")
    item_id: str = Field(description="Inventory item id, if present.")
    item_name: str = Field(description="Line item description.")
    quantity: int = Field(description="Requested quantity.")
    unit_price: float = Field(description="Unit price in quote currency.")
    line_total: float = Field(description="Line total amount.")


class QuoteExtraction(BaseModel):
    quote_id: str = Field(description="Quote or proforma identifier.")
    quote_date: str = Field(description="Quote date in YYYY-MM-DD format.")
    supplier_name: str = Field(description="Supplier company name.")
    customer_name: str = Field(description="Customer name from quote.")
    currency: str = Field(description="ISO currency code, for example USD.")
    subtotal_amount: float = Field(description="Subtotal before tax.")
    tax_amount: float = Field(description="Tax amount.")
    total_amount: float = Field(description="Grand total amount.")
    line_items: List[QuoteLineItem] = Field(description="Extracted quote line items.")


# MCP Toolbox endpoint (default local run).
toolbox_url = os.getenv("TOOLBOX_URL", "http://localhost:5000")
tools = []
toolbox_error = None
toolbox = None
try:
    toolbox = ToolboxSyncClient(toolbox_url)
    tools = toolbox.load_toolset("document_intake_toolset")
except Exception as exc:
    toolbox_error = str(exc)
    if toolbox is not None:
        try:
            toolbox.close()
        except Exception:
            pass

document_intake_agent = LlmAgent(
    name="document_intake_agent",
    model=GEMINI_2_5_FLASH,
    description=(
        "Optional multimodal quote/proforma extractor that stores structured output "
        "and runs quote match validation."
    ),
    instruction="""
You are a document intake specialist for supply-chain quote/proforma processing.

When user uploads a quote/proforma image or PDF:
1. Extract structured fields using the QuoteExtraction schema.
2. Only use values visible in the document. Do not invent missing values.
3. Persist extracted data with these tool calls:
   - insert_quote_header for quote-level fields.
   - insert_quote_line_item for each line item.
4. Run validate_quote_match using expected item_id, quantity, and expected total.
5. Return concise output with:
   - quote_id
   - extracted total
   - matched quantity/total status
   - clear mismatch reason if not matched
""",
    output_schema=QuoteExtraction,
    tools=tools,
)
