# Clarifications
- Reference date is passed explicitly; the evaluator uses 2026-11-23 for fixture cases.
- This prototype parses a constrained English subset. It does not create calendar events or send notifications.
- A missing or ambiguous mandatory field results in `clarify`, never a guessed value.
- The default fixture provider is for offline harness verification only. Live model use requires a separately configured adapter and recording model/version/parameters.
