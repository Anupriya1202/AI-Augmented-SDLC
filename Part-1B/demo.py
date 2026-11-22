"""Run the reminder agent using offline fixtures or optional live provider."""
from __future__ import annotations
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from src.reminder_agent import FixtureProvider, ReminderAgent  # noqa: E402

mode = os.environ.get("REMINDER_PROVIDER", "fixture").lower()
if mode == "live":
    from src.reminder_agent import OpenAICompatibleProvider
    provider = OpenAICompatibleProvider()
else:
    provider = FixtureProvider()

agent = ReminderAgent(provider)
reference_date = os.environ.get("REFERENCE_DATE", "2026-11-23")
request = " ".join(sys.argv[1:]) or "Remind me to submit the assignment tomorrow at 9 am"
print(json.dumps(agent.process(request, reference_date), indent=2))
