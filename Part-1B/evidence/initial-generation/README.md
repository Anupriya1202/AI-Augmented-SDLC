# Initial generation snapshot

The initial Reminder Agent parser is preserved in `reminder_agent.py`. It returned the provider result directly without validating that the object matched the output contract. The malformed-provider regression example is described in `../harness-log.md`: a three-field response with an invalid date passed through unchanged. The final implementation adds output-contract validation and fails closed to clarification.
