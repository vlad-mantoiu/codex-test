"""Gorgias read-only client helpers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests

from models.tickets import Ticket


@dataclass
class GorgiasConfig:
    base_url: str
    username: str
    password: str
    timeout_s: int = 10


class GorgiasClient:
    """Minimal, read-only Gorgias API client."""

    def __init__(self, config: GorgiasConfig) -> None:
        self.config = config

    def list_tickets(self, limit: int = 5) -> List[Ticket]:
        """Fetch recent tickets and map to internal Ticket objects."""
        url = f"{self.config.base_url.rstrip('/')}/tickets"
        response = requests.get(
            url,
            auth=(self.config.username, self.config.password),
            params={"limit": limit, "order_by": "updated_datetime:desc"},
            timeout=self.config.timeout_s,
        )
        response.raise_for_status()
        payload = response.json()
        tickets = []
        for item in payload.get("data", []):
            ticket_id = str(item.get("id", ""))
            tickets.append(
                Ticket(
                    ticket_id=ticket_id,
                    channel=item.get("via", {}).get("channel", "unknown"),
                    customer=_safe_customer_name(item.get("customer")),
                    subject=item.get("subject", "(no subject)"),
                    last_message=self._latest_message(ticket_id) or "",
                    order_number=_extract_order_number(item),
                    tags=[tag.get("name") for tag in item.get("tags", []) if tag.get("name")],
                    history=[],
                    sentiment="neutral",
                    intent="general",
                    risk_factors=[],
                    draft_response="",
                    internal_note="",
                    proposed_resolution="",
                )
            )
        return tickets

    def _latest_message(self, ticket_id: str) -> Optional[str]:
        """Fetch the latest message for a ticket."""
        if not ticket_id:
            return None
        url = f"{self.config.base_url.rstrip('/')}/tickets/{ticket_id}/messages"
        response = requests.get(
            url,
            auth=(self.config.username, self.config.password),
            params={"limit": 1, "order_by": "created_datetime:desc"},
            timeout=self.config.timeout_s,
        )
        response.raise_for_status()
        payload = response.json()
        messages = payload.get("data", [])
        if not messages:
            return None
        return messages[0].get("body_text") or messages[0].get("body")


def _safe_customer_name(customer: Dict[str, Any] | None) -> str:
    if not customer:
        return "Unknown"
    return customer.get("name") or customer.get("email") or "Unknown"


def _extract_order_number(ticket: Dict[str, Any]) -> str:
    """Best-effort extraction of order number from custom fields or metadata."""
    for key in ("order_number", "order_id", "shopify_order_number"):
        if key in ticket:
            return str(ticket.get(key))
    custom_fields = ticket.get("custom_fields", {})
    if isinstance(custom_fields, dict):
        for key in ("order_number", "order_id"):
            if key in custom_fields:
                return str(custom_fields.get(key))
    return ""
