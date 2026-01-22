"""OpenAI client wrapper for drafting suggestions.

All outputs are drafts only. Nothing is sent externally.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Dict

import requests

from models.tickets import Ticket


@dataclass
class OpenAIConfig:
    api_key: str
    model: str = "gpt-4.1-mini"
    timeout_s: int = 20


class OpenAIClient:
    """Minimal client using OpenAI's Responses API."""

    def __init__(self, config: OpenAIConfig) -> None:
        self.config = config

    def draft_suggestions(self, ticket: Ticket, tone_guidelines: str) -> Dict[str, str]:
        """Return draft customer reply + internal note suggestions."""
        prompt = _build_prompt(ticket, tone_guidelines)
        response = requests.post(
            "https://api.openai.com/v1/responses",
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.config.model,
                "input": prompt,
                "temperature": 0.2,
            },
            timeout=self.config.timeout_s,
        )
        response.raise_for_status()
        payload = response.json()
        output_text = _extract_output_text(payload)
        return _parse_llm_json(output_text)


def _build_prompt(ticket: Ticket, tone_guidelines: str) -> str:
    return (
        "You are a Human-in-the-Loop CX Copilot. Provide drafts only. "
        "Never send messages, never approve refunds, replacements, or actions. "
        "If policy conflicts are detected, flag them and recommend escalation.\n\n"
        "Authority hierarchy: ACCC/legal > website policies > internal CX rules > macros > precedent.\n\n"
        "Draft TWO items in JSON format: customer_reply and internal_note. "
        "The customer_reply must be an editable draft only. The internal_note must include "
        "risk flags and questions for the human.\n\n"
        "Tone guidelines:\n"
        f"{tone_guidelines}\n\n"
        "Ticket context:\n"
        f"Ticket ID: {ticket.ticket_id}\n"
        f"Channel: {ticket.channel}\n"
        f"Customer: {ticket.customer}\n"
        f"Subject: {ticket.subject}\n"
        f"Last message: {ticket.last_message}\n"
        f"Order number: {ticket.order_number}\n"
        f"Tags: {', '.join(ticket.tags)}\n"
        f"History: {' | '.join(ticket.history)}\n"
        "Return JSON only. Example: {\"customer_reply\": \"...\", \"internal_note\": \"...\"}."
    )


def _extract_output_text(payload: Dict[str, object]) -> str:
    outputs = payload.get("output", [])
    for item in outputs:
        content = item.get("content", [])
        for block in content:
            if block.get("type") == "output_text":
                return block.get("text", "")
    return ""


def _parse_llm_json(output_text: str) -> Dict[str, str]:
    try:
        data = json.loads(output_text)
        return {
            "customer_reply": data.get("customer_reply", ""),
            "internal_note": data.get("internal_note", ""),
        }
    except json.JSONDecodeError:
        return {
            "customer_reply": "Draft unavailable. Please review manually.",
            "internal_note": "LLM output was not valid JSON. Escalate if needed.",
        }
