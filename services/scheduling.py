"""Scheduling helper for summary timing."""
from __future__ import annotations

from datetime import datetime, time, timedelta


def next_summary_time(summary_time: time) -> str:
    """Return the next summary time for display (local time)."""
    now = datetime.now()
    target = datetime.combine(now.date(), summary_time)
    if now > target:
        target = target + timedelta(days=1)
    return target.strftime("%Y-%m-%d %H:%M")
