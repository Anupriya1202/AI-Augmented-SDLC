"""Single Part 1B pipeline: schema -> invariants -> semantic rubric -> threshold."""
from __future__ import annotations
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
sys.path.insert(0, str(ROOT))
from src.reminder_agent import OUTPUT_KEYS, FixtureProvider, ReminderAgent  # noqa: E402

THRESHOLD = 0.80
REFERENCE_DATE = "2026-11-23"


def schema_check(output: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(output, dict):
        return ["output must be an object"]
    if set(output) != OUTPUT_KEYS:
        errors.append("output key set does not match contract")
        return errors
    if output["intent"] not in {"create", "reschedule", "snooze", "clarify"}:
        errors.append("unsupported intent")
    for key in ("title", "date", "time", "reminder_id", "clarification_question", "reason"):
        if output[key] is not None and not isinstance(output[key], str):
            errors.append(f"{key} must be string or null")
    if not isinstance(output["confidence"], (int, float)) or isinstance(output["confidence"], bool) or not 0 <= output["confidence"] <= 1:
        errors.append("confidence must be numeric in [0,1]")
    if not isinstance(output["reason"], str) or not output["reason"].strip():
        errors.append("reason must be non-empty")
    return errors


def invariant_check(output: dict) -> list[str]:
    errors: list[str] = []
    intent = output["intent"]
    if intent == "create" and not all(output[k] for k in ("title", "date", "time")):
        errors.append("create requires title, date, and time")
    if intent == "reschedule" and not all(output[k] for k in ("reminder_id", "date", "time")):
        errors.append("reschedule requires reminder_id, date, and time")
    if intent == "snooze" and not output["reminder_id"]:
        errors.append("snooze requires reminder_id")
    if intent == "clarify" and not (output["clarification_question"] or "").strip():
        errors.append("clarify requires a non-empty question")
    if output["date"]:
        try:
            date.fromisoformat(output["date"])
        except ValueError:
            errors.append("date must be a valid ISO calendar date")
    if output["time"]:
        try:
            parsed = datetime.strptime(output["time"], "%H:%M")
            if parsed.strftime("%H:%M") != output["time"]:
                errors.append("time must use HH:MM")
        except ValueError:
            errors.append("time must be a valid 24-hour HH:MM time")
    return errors


def semantic_check(output: dict, expected: dict, applicable: list[str]) -> dict:
    comparisons = {
        "intent": output["intent"] == expected.get("intent"),
        "title": output["title"] == expected.get("title"),
        "date": output["date"] == expected.get("date"),
        "time": output["time"] == expected.get("time"),
        "safety": (output["intent"] == "clarify" if expected.get("intent") == "clarify" else output["intent"] != "clarify"),
    }
    earned = sum(1 for item in applicable if comparisons[item])
    return {"earned": earned, "possible": len(applicable), "score": earned / len(applicable) if applicable else 1.0,
            "checks": {item: comparisons[item] for item in applicable}}


def main() -> int:
    dataset = json.loads((ROOT / "evals" / "dataset.json").read_text(encoding="utf-8"))
    agent = ReminderAgent(FixtureProvider())
    cases = []
    schema_passes = 0
    invariant_passes = 0
    semantic_earned = 0
    semantic_possible = 0
    for case in dataset:
        output = agent.process(case["input"], REFERENCE_DATE)
        schema_errors = schema_check(output)
        invariant_errors = invariant_check(output) if not schema_errors else ["invariants skipped due to schema failure"]
        semantic = semantic_check(output, case["expected"], case["applicable"]) if not schema_errors else {"earned": 0, "possible": len(case["applicable"]), "score": 0.0, "checks": {}}
        schema_ok = not schema_errors
        invariant_ok = not invariant_errors
        schema_passes += int(schema_ok)
        invariant_passes += int(invariant_ok)
        semantic_earned += semantic["earned"]
        semantic_possible += semantic["possible"]
        cases.append({"id": case["id"], "input": case["input"], "output": output,
                      "schema": {"pass": schema_ok, "errors": schema_errors},
                      "invariants": {"pass": invariant_ok, "errors": invariant_errors},
                      "semantic": semantic})
    count = len(dataset)
    semantic_score = semantic_earned / semantic_possible if semantic_possible else 0.0
    schema_rate = schema_passes / count if count else 0.0
    invariant_rate = invariant_passes / count if count else 0.0
    passed = schema_rate == 1.0 and invariant_rate == 1.0 and semantic_score >= THRESHOLD
    report = {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "provider": "FixtureProvider (offline fixture; not a live LLM)",
              "reference_date": REFERENCE_DATE, "dataset_size": count, "threshold": THRESHOLD,
              "scoring": "PASS iff schema=100%, invariants=100%, semantic >= 0.80",
              "metrics": {"schema_pass_rate": schema_rate, "invariant_pass_rate": invariant_rate,
                          "semantic_score": semantic_score, "semantic_points": {"earned": semantic_earned, "possible": semantic_possible}},
              "overall": "PASS" if passed else "FAIL", "cases": cases}
    destination = ROOT / "evidence" / "eval-results.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"overall": report["overall"], "dataset_size": count, "metrics": report["metrics"]}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
