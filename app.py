"""
Human-in-the-Loop CX Copilot (Local POC)

This Flask app is intentionally simple and highly commented to make
future evolution obvious. Every action is a suggestion or internal note
only; nothing is sent externally.
"""
from __future__ import annotations

import os
from datetime import datetime, time
from typing import List

from flask import Flask, jsonify, redirect, render_template, request, url_for

from models.tickets import Ticket
from services.analytics import build_daily_summary, build_periodic_summary
from services.audit_log import AuditLogger, LogEntry
from services.policy_engine import PolicyDecision, evaluate_ticket_risk
from services.sample_data import SAMPLE_TICKETS
from services.scheduling import next_summary_time


def create_app() -> Flask:
    """Application factory to keep things modular."""
    app = Flask(__name__)

    # Configuration kept intentionally explicit for auditability.
    app.config["INTERNAL_AUTH_TOKEN"] = os.environ.get("INTERNAL_AUTH_TOKEN", "local-dev")
    app.config["SUMMARY_TIME_AU"] = time(16, 0)

    audit_logger = AuditLogger(
        log_path=os.environ.get("HITL_LOG_PATH", "data/audit_log.jsonl")
    )

    @app.before_request
    def enforce_internal_auth() -> None:
        """Lightweight internal-only auth gate (POC)."""
        if request.endpoint in {"static", "auth_help"}:
            return
        token = request.headers.get("X-Internal-Token")
        if token is None:
            token = request.args.get("token")
        if token != app.config["INTERNAL_AUTH_TOKEN"]:
            # Keep it simple: redirect to a landing page with instructions.
            if request.endpoint != "auth_help":
                return redirect(url_for("auth_help"))

    @app.route("/auth")
    def auth_help() -> str:
        return render_template("auth.html")

    @app.route("/")
    def dashboard() -> str:
        """Main dashboard view with Action + Analytics tabs."""
        tickets: List[Ticket] = SAMPLE_TICKETS
        policy_decisions = {ticket.ticket_id: evaluate_ticket_risk(ticket) for ticket in tickets}
        daily_summary = build_daily_summary(tickets)
        weekly_summary = build_periodic_summary(tickets, period="weekly")
        monthly_summary = build_periodic_summary(tickets, period="monthly")
        next_daily_summary = next_summary_time(app.config["SUMMARY_TIME_AU"])

        return render_template(
            "index.html",
            tickets=tickets,
            policy_decisions=policy_decisions,
            daily_summary=daily_summary,
            weekly_summary=weekly_summary,
            monthly_summary=monthly_summary,
            next_daily_summary=next_daily_summary,
        )

    @app.route("/api/log", methods=["POST"])
    def log_action():
        """Log a human decision about a suggestion."""
        payload = request.json or {}
        entry = LogEntry.from_payload(payload)
        audit_logger.write(entry)
        return jsonify({"status": "logged"})

    @app.route("/api/tickets")
    def tickets_api():
        """Lightweight API for frontend to fetch tickets."""
        tickets: List[Ticket] = SAMPLE_TICKETS
        return jsonify([ticket.to_dict() for ticket in tickets])

    return app


if __name__ == "__main__":
    # Use 0.0.0.0 for container friendliness.
    create_app().run(host="0.0.0.0", port=5000, debug=True)
