from pathlib import Path
import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.a2a.utils.agent_to_a2a import to_a2a

from remote_agent.finance_agent.tools import (
    finalize_approval,
    get_approval_threshold,
    request_approval,
)

# Load environment variables from project root.
dotenv_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=dotenv_path)

GEMINI_2_5_FLASH = "gemini-2.5-flash"

root_agent = LlmAgent(
    name="FinanceAgent",
    model=GEMINI_2_5_FLASH,
    description="Handles stateful, multi-turn budget and financial approval process.",
    instruction="""
You are a financial controller. Your goal is to approve expenditures.

Use tools:
- get_approval_threshold for current policy.
- request_approval for initial expense review.
- finalize_approval only when user explicitly confirms approve/reject.

Rules:
- Explain approval decisions clearly.
- If approval is pending, ask the user a direct confirmation question.
- Do not execute logistics or inventory tasks.
""",
    tools=[get_approval_threshold, request_approval, finalize_approval],
)

# Expose this agent as an A2A server app.
a2a_host = os.getenv("A2A_HOST", "127.0.0.1")
a2a_port = int(os.getenv("A2A_PORT", "8001"))
a2a_protocol = os.getenv("A2A_PROTOCOL", "http")
a2a_app = to_a2a(
    root_agent,
    host=a2a_host,
    port=a2a_port,
    protocol=a2a_protocol,
)
