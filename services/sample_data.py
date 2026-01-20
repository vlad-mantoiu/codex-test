"""Sample data to make the POC runnable without external dependencies."""
from __future__ import annotations

from models.tickets import Ticket

SAMPLE_TICKETS = [
    Ticket(
        ticket_id="GX-1042",
        channel="Email",
        customer="Ava Nguyen",
        subject="Order arrived leaking",
        last_message="My serum bottle arrived leaking all over the box 😞",
        order_number="SO-89214",
        tags=["damage", "priority"],
        history=["Customer placed order 3 days ago", "Shipping label created"],
        sentiment="upset",
        intent="replacement",
        risk_factors=["damage claim", "potential replacement"],
        draft_response=(
            "Hi Ava — I'm sorry your serum arrived like that. I can help draft "
            "next steps. Would you like us to review photos and explore options?"
        ),
        internal_note=(
            "Potential damage-in-transit. Request photos of packaging + item. "
            "If confirmed, propose replacement. Flag for HITL approval."
        ),
        proposed_resolution="Replacement (pending approval)",
    ),
    Ticket(
        ticket_id="GX-1043",
        channel="Instagram",
        customer="Luca Stone",
        subject="Still waiting for tracking",
        last_message="Hey team, tracking hasn't updated in 5 days. Any idea?",
        order_number="SO-89227",
        tags=["shipping"],
        history=["Order shipped 7 days ago", "Carrier delay noted"],
        sentiment="neutral",
        intent="shipping_update",
        risk_factors=["carrier delay"],
        draft_response=(
            "Hi Luca! I can draft an update explaining the carrier delay and "
            "offer to monitor tracking with you."
        ),
        internal_note=(
            "Carrier delay likely. No action until 10 business days. Offer to "
            "follow up."
        ),
        proposed_resolution="Provide tracking update",
    ),
    Ticket(
        ticket_id="GX-1044",
        channel="Chat",
        customer="Priya Shah",
        subject="Refund request for allergic reaction",
        last_message="I had a reaction and want a refund ASAP.",
        order_number="SO-89231",
        tags=["refund", "legal"],
        history=["First purchase", "No prior issues"],
        sentiment="angry",
        intent="refund_request",
        risk_factors=["ACCC risk", "medical concern"],
        draft_response=(
            "Hi Priya — I'm sorry to hear that. I can draft a response asking "
            "for details and explain next steps under our policy."
        ),
        internal_note=(
            "Escalate: medical concern + refund request. Review ACCC obligations "
            "and product safety. Do not make commitments without approval."
        ),
        proposed_resolution="Escalate to supervisor",
    ),
]
