"""Audit log utilities.

Writes to a JSONL file for easy replay and future Google Sheets sync.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


@dataclass
class LogEntry:
    timestamp: str
    ticket_id: str
    order_number: str
    customer: str
    channel: str
    issue_category: str
    proposed_resolution: str
    cost_estimate: str
    ai_confidence: str
    human_decision: str
    notes: str

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]) -> "LogEntry":
        now = datetime.utcnow().isoformat()
        return cls(
            timestamp=payload.get("timestamp", now),
            ticket_id=payload.get("ticket_id", "unknown"),
            order_number=payload.get("order_number", ""),
            customer=payload.get("customer", ""),
            channel=payload.get("channel", ""),
            issue_category=payload.get("issue_category", ""),
            proposed_resolution=payload.get("proposed_resolution", ""),
            cost_estimate=payload.get("cost_estimate", ""),
            ai_confidence=payload.get("ai_confidence", ""),
            human_decision=payload.get("human_decision", ""),
            notes=payload.get("notes", ""),
        )


class AuditLogger:
    """Append-only audit log to preserve decision history."""

    def __init__(self, log_path: str) -> None:
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, entry: LogEntry) -> None:
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry.__dict__) + "\n")
