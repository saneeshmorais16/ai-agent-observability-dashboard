# Project Status

## Current Build Status

Working starter version for local portfolio review. The API, SQLite storage, synthetic data generator, dashboard metrics and tests are implemented without any LLM API dependency.

## Completed Features

- Agent run tracking
- Tool-call tracking
- Token and cost estimation
- Latency monitoring
- Error and retry tracking
- Prompt risk detection
- Audit event logging
- Trace retrieval
- Dashboard metrics
- Risk, cost and error endpoints
- Synthetic data generator
- Simple HTML/CSS/JavaScript dashboard
- pytest test suite
- GitHub Actions workflow

## Remaining Improvements

- Add charts for cost and latency trends.
- Add OpenTelemetry-compatible trace export.
- Add configurable risk rules.
- Add provider-specific token pricing presets.
- Add screenshots after local dashboard review.
- Add authentication before any real deployment.

## Testing Status

Tests cover run creation, tool-call logging, cost estimation, latency/metric calculation, risk detection, dashboard metrics, health endpoint and trace retrieval.

Run:

```bash
pytest
```

## What Must Be Checked Before Making Public

- No `.env` files or credentials are present.
- No private prompts, private conversations or real agent logs are present.
- No personal data, private documents or customer data are present.
- No database files, logs, PDFs or generated outputs are committed.
- README does not claim production use, real users, clients or enterprise deployment.

## Files That Must Never Be Committed

- `.env` or `.env.*`
- API keys, tokens, credentials or passwords
- private prompts
- private conversations
- private agent logs
- personal data
- database files
- logs
- generated CV PDFs
- application packets
- generated outputs
- uploads
- local data
