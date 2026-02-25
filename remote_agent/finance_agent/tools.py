from typing import Dict

APPROVAL_THRESHOLD_USD = 1000.0
_pending_sessions: Dict[str, dict] = {}


def get_approval_threshold() -> dict:
    """Returns the pre-approved budget threshold in USD."""
    return {
        "currency": "USD",
        "threshold": APPROVAL_THRESHOLD_USD,
        "message": "Expenses above this threshold require human confirmation.",
    }


def request_approval(session_id: str, amount_usd: float, reason: str) -> dict:
    """Evaluates an expense and returns approval status or human-approval request."""
    if amount_usd <= APPROVAL_THRESHOLD_USD:
        return {
            "status": "approved",
            "requires_human": False,
            "message": f"Approved automatically. Amount ${amount_usd:.2f} is within threshold.",
            "session_id": session_id,
        }

    _pending_sessions[session_id] = {
        "amount_usd": amount_usd,
        "reason": reason,
        "status": "pending_human_approval",
    }
    return {
        "status": "pending_human_approval",
        "requires_human": True,
        "message": (
            f"This expenditure requires human approval. The cost of ${amount_usd:.2f} "
            f"exceeds the pre-approved limit of ${APPROVAL_THRESHOLD_USD:.2f}."
        ),
        "session_id": session_id,
        "reason": reason,
    }


def finalize_approval(session_id: str, approve: bool) -> dict:
    """Finalizes human approval decision for a pending expense request."""
    pending = _pending_sessions.get(session_id)
    if not pending:
        return {
            "status": "not_found",
            "message": "No pending approval found for this session_id.",
            "session_id": session_id,
        }

    if approve:
        pending["status"] = "approved"
        return {
            "status": "approved",
            "message": "The expenditure has been approved.",
            "session_id": session_id,
            "amount_usd": pending["amount_usd"],
        }

    pending["status"] = "rejected"
    return {
        "status": "rejected",
        "message": "The expenditure has been rejected.",
        "session_id": session_id,
        "amount_usd": pending["amount_usd"],
    }
