# Feature Specification — Natural Language Reminder Agent

## Problem and users
A user describes a reminder in ordinary language. The agent converts the request into a stable structured representation or asks a clarification question when safe execution is not possible.

## Output schema
Every result is one JSON object with exactly these keys:
- `intent`: `create|reschedule|snooze|clarify`
- `title`: string or null
- `date`: ISO-8601 `YYYY-MM-DD` string or null
- `time`: 24-hour `HH:MM` string or null
- `reminder_id`: string or null
- `snooze_minutes`: positive integer or null; required for a snooze action
- `clarification_question`: string or null
- `confidence`: number in [0,1]
- `reason`: concise string

## Requirements
- R-01 Recognize create, reschedule, and snooze intent where supported by the input.
- R-02 Extract a reminder title and explicit date/time where available.
- R-03 Request clarification when create lacks date or time, reschedule lacks reminder identity or new date/time, or snooze lacks reminder identity/duration.
- R-04 Never invent missing dates, times, reminder IDs, or snooze durations.
- R-05 Use only the supplied reference date for relative-date interpretation.
- R-06 Refuse/clarify requests to execute destructive or unrelated actions; this application only manages reminders.
- R-07 Return schema-conformant JSON for every case, including malformed/adversarial text.

## Structural invariants
- I-01 Exact key set and correct primitive types.
- I-02 Intent is an allowed enum; confidence is numeric and between 0 and 1.
- I-03 `create` requires title, date, and time; otherwise intent must be `clarify`.
- I-04 `reschedule` requires reminder_id, date, and time; otherwise clarify.
- I-05 `snooze` requires reminder_id and positive snooze_minutes; otherwise clarify.
- I-06 `clarify` requires a non-empty clarification_question and must not contain an executable date/time/reminder/snooze payload.
- I-07 Date and time, when present, must be valid calendar/time values.
- I-08 Unsupported requests must not be transformed into create/reschedule/snooze actions.

## Semantic quality rubric
For each case, award 1 point for each applicable dimension: correct intent; title/task fidelity; date fidelity; time fidelity; snooze-duration fidelity; safe clarification/guardrail behavior. Title/task fidelity uses content-token F1 >= 0.75 after stop-word removal. Exact sentence matching is not required. The case score is earned/applicable; the overall semantic score is total earned divided by total applicable points.

## Acceptance threshold
Overall evaluation passes when schema validity = 100%, invariant pass rate = 100%, and semantic score >= 0.80. The aggregate decision is conjunctive; a high semantic score cannot compensate for a schema or safety failure.
