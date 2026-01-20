# HITL CX Copilot (Local POC)

## Architecture Overview

**Goal:** A local-first, read-only, Human-in-the-Loop CX Copilot for Gorgias-driven ecommerce support. The system only drafts suggestions and internal notes. It never sends responses, issues refunds, or triggers external actions.

### Key Components

1. **Flask Web App (`app.py`)**
   - Serves the dashboard UI and lightweight APIs.
   - Enforces a simple internal auth token guardrail.
   - Displays risk assessments, suggested drafts, and analytics summaries.

2. **Policy & Risk Engine (`services/policy_engine.py`)**
   - Applies a conservative safety-first heuristic.
   - Flags legal/ACCC risk and conflict conditions.
   - Outputs a clear explanation and recommended handling steps.

3. **Analytics & Summaries (`services/analytics.py`)**
   - Generates daily/weekly/monthly summaries from ticket data.
   - Highlights notable events, trends, and repeat issues.

4. **Audit Logging (`services/audit_log.py`)**
   - Writes append-only JSONL logs for replayable decision history.
   - Structured to map directly to Google Sheets columns later.

5. **Sample Data (`services/sample_data.py`)**
   - Enables a runnable POC without external integrations.
   - Models typical Gorgias tickets and risk conditions.

### External Integrations (Read-Only, POC Stub)

- **Gorgias**: Ticket fetch (read-only) – placeholder.
- **Google Sheets**: Logging proposed actions – currently local JSONL file.
- **Shopify / Okendo / Slack / Gmail**: Read-only connectors planned.

## Running Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000/?token=local-dev`.

## Assumptions & Next Steps

- Local-only POC, no persistence beyond audit logs.
- External system calls are stubbed; production would implement read-only clients.
- Future evolutions include:
  - Real Gorgias API pulls.
  - Google Sheets logging via service account.
  - Auth integration (SSO / internal VPN).
  - Decision tree editor + learning approval workflow.
