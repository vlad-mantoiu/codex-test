"""Risk and policy evaluation logic.

This module intentionally favors safety and escalation over automation.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

from models.tickets import Ticket


@dataclass
class PolicyDecision:
    risk_level: str
    reason: str
    recommended_handling: str
    conflict_detected: bool = False


def evaluate_ticket_risk(ticket: Ticket) -> PolicyDecision:
    """Return a human-readable risk assessment for a ticket."""
    risk_factors = [factor.lower() for factor in ticket.risk_factors]
    tags = [tag.lower() for tag in ticket.tags]

    if "accc risk" in risk_factors or "legal" in tags:
        return PolicyDecision(
            risk_level="red",
            reason="Potential legal obligation or regulatory risk detected.",
            recommended_handling="Escalate to supervisor and document carefully.",
            conflict_detected=True,
        )

    if "replacement" in ticket.intent or "damage" in tags:
        return PolicyDecision(
            risk_level="amber",
            reason="Replacement or damage claim requires approval.",
            recommended_handling="Collect evidence, propose replacement for approval.",
        )

    if "shipping" in tags:
        return PolicyDecision(
            risk_level="green",
            reason="Likely safe to provide status update.",
            recommended_handling="Share tracking update and set expectations.",
        )

    return PolicyDecision(
        risk_level="amber",
        reason="Unclear intent or limited context.",
        recommended_handling="Review ticket and ask clarifying questions.",
    )
