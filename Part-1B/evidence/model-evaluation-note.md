# Model Evaluation Qualification

The checked-in 15-case evaluation was run with `FixtureProvider`, a deterministic offline adapter. Its schema, invariant and semantic scores validate the fixture pipeline only; they must not be presented as live LLM performance. `OpenAICompatibleProvider` is available for an optional live run with `REMINDER_PROVIDER=live` and `OPENAI_API_KEY` set in the environment. Record the actual model/version, provider response, parameters, outputs and errors separately. Never store credentials in this repository or in screenshots.
