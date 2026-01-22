"""Dataclasses for ticket data."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Ticket:
    """Represents a Gorgias ticket (read-only)."""

    ticket_id: str
    channel: str
    customer: str
    subject: str
    last_message: str
    order_number: str
    tags: List[str] = field(default_factory=list)
    history: List[str] = field(default_factory=list)
    sentiment: str = "neutral"
    intent: str = "general"
    risk_factors: List[str] = field(default_factory=list)
    draft_response: str = ""
    internal_note: str = ""
    proposed_resolution: str = ""

    def to_dict(self) -> Dict[str, str]:
        return {
            "ticket_id": self.ticket_id,
            "channel": self.channel,
            "customer": self.customer,
            "subject": self.subject,
            "last_message": self.last_message,
            "order_number": self.order_number,
            "tags": self.tags,
            "history": self.history,
            "sentiment": self.sentiment,
            "intent": self.intent,
            "risk_factors": self.risk_factors,
            "draft_response": self.draft_response,
            "internal_note": self.internal_note,
            "proposed_resolution": self.proposed_resolution,
        }
