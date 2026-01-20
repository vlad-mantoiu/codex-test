"""Analytics helpers for summaries."""
from __future__ import annotations

from collections import Counter
from datetime import datetime
from typing import List

from models.tickets import Ticket


def build_daily_summary(tickets: List[Ticket]) -> dict:
    """Create a daily summary payload for the dashboard."""
    intents = Counter(ticket.intent for ticket in tickets)
    risks = Counter(ticket.sentiment for ticket in tickets)
    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "ticket_volume": len(tickets),
        "top_intents": intents.most_common(3),
        "sentiment_breakdown": risks,
        "notable": _detect_notable_events(tickets),
    }


def build_periodic_summary(tickets: List[Ticket], period: str) -> dict:
    """Generate weekly/monthly summaries.

    In a production system this would query historical data. In the POC
    we reuse the current sample set and focus on structure.
    """
    return {
        "period": period,
        "high_risk_tickets": [ticket.ticket_id for ticket in tickets if ticket.sentiment == "angry"],
        "repeat_issues": _repeat_issue_signals(tickets),
    }


def _detect_notable_events(tickets: List[Ticket]) -> List[str]:
    notable = []
    for ticket in tickets:
        if "accc" in " ".join(ticket.risk_factors).lower():
            notable.append(f"Legal/ACCC risk in ticket {ticket.ticket_id}")
        if ticket.intent == "replacement":
            notable.append(f"Replacement consideration in {ticket.ticket_id}")
    return notable


def _repeat_issue_signals(tickets: List[Ticket]) -> List[str]:
    counts = Counter(ticket.intent for ticket in tickets)
    return [intent for intent, count in counts.items() if count > 1]
