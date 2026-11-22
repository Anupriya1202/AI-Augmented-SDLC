"""Reminder parsing application with a replaceable model-provider boundary."""
from __future__ import annotations

import re
from datetime import date
from typing import Protocol

OUTPUT_KEYS = {"intent", "title", "date", "time", "reminder_id", "clarification_question", "confidence", "reason"}


class Provider(Protocol):
    def generate(self, text: str, reference_date: str) -> dict: ...


class ReminderAgent:
    def __init__(self, provider: Provider) -> None:
        self.provider = provider

    def process(self, text: str, reference_date: str = "2026-11-23") -> dict:
        if not isinstance(text, str) or not text.strip():
            return _clarify("Please describe the reminder you want to manage.", "Input is empty or malformed.")
        try:
            date.fromisoformat(reference_date)
        except (TypeError, ValueError):
            return _clarify("Please provide a valid reference date.", "Reference date is invalid.")
        try:
            result = self.provider.generate(text.strip(), reference_date)
        except Exception:
            return _clarify("The reminder request could not be processed. Please try again.", "Provider failure was contained.")
        return result


def _clarify(question: str, reason: str) -> dict:
    return {"intent": "clarify", "title": None, "date": None, "time": None,
            "reminder_id": None, "clarification_question": question,
            "confidence": 0.95, "reason": reason}


class FixtureProvider:
    """Offline deterministic fixture provider; not a live LLM."""
    def generate(self, text: str, reference_date: str) -> dict:
        lowered = text.lower()
        if any(term in lowered for term in ("ignore all rules", "reveal system prompt", "delete my files", "transfer money")):
            return _clarify("I can only help manage reminders. What reminder would you like to create or change?", "Unsupported or adversarial request blocked.")
        if not lowered.strip() or lowered in {"???", "<script>alert(1)</script>"}:
            return _clarify("Please describe the reminder you want to manage.", "Input is malformed or underspecified.")

        intent = "create"
        if "reschedule" in lowered or "move my" in lowered or "change the time" in lowered:
            intent = "reschedule"
        elif "snooze" in lowered or "postpone" in lowered:
            intent = "snooze"

        id_match = re.search(r"(?:reminder\s*#|\bid\s+)([a-z0-9_-]+)", lowered)
        reminder_id = id_match.group(1) if id_match else None
        time_match = re.search(r"\b(\d{1,2})(?::(\d{2}))?\s*(am|pm)\b|\b([01]?\d|2[0-3]):([0-5]\d)\b", lowered)
        time_value = None
        if time_match:
            if time_match.group(4):
                time_value = f"{int(time_match.group(4)):02d}:{time_match.group(5)}"
            else:
                hour = int(time_match.group(1))
                minute = int(time_match.group(2) or "00")
                if time_match.group(3) == "pm" and hour != 12:
                    hour += 12
                if time_match.group(3) == "am" and hour == 12:
                    hour = 0
                if hour < 24 and minute < 60:
                    time_value = f"{hour:02d}:{minute:02d}"

        date_value = None
        if "tomorrow" in lowered:
            ref = date.fromisoformat(reference_date)
            date_value = date.fromordinal(ref.toordinal() + 1).isoformat()
        elif "today" in lowered:
            date_value = reference_date
        else:
            date_match = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", lowered)
            if date_match:
                try:
                    date_value = date.fromisoformat(date_match.group(1)).isoformat()
                except ValueError:
                    return _clarify("That date is not valid. Which date did you mean?", "Invalid calendar date.")

        title = None
        title_match = re.search(r"(?:remind me to|reminder to|about)\s+(.+?)(?=\s+(?:tomorrow|today|on\s+\d{4}-\d{2}-\d{2}|at\s+\d|by\s+\d)|$)", text, re.I)
        if title_match:
            title = title_match.group(1).strip(" .,!?")
        elif intent in {"reschedule", "snooze"}:
            title = None

        if intent == "create":
            if not title or not date_value or not time_value:
                missing = "the reminder title" if not title else "the date" if not date_value else "the time"
                return _clarify(f"What is {missing} for this reminder?", "Mandatory create field is missing.")
        elif intent == "reschedule":
            if not reminder_id or not date_value or not time_value:
                return _clarify("Which reminder ID should I reschedule, and what is its new date and time?", "Reschedule requires ID, date, and time.")
        elif intent == "snooze":
            if not reminder_id:
                return _clarify("Which reminder ID should be snoozed?", "Snooze requires a reminder ID.")

        return {"intent": intent, "title": title, "date": date_value, "time": time_value,
                "reminder_id": reminder_id, "clarification_question": None,
                "confidence": 0.91, "reason": "Parsed supported reminder intent and explicit fields."}
