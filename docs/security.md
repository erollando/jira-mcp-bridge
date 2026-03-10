# Security Model

## Core principles

- Local-only MCP server over stdio
- ACLI authentication is external and pre-established
- No Jira token exposure to AI agents
- No arbitrary shell passthrough from MCP
- Constrained typed operations only

## Guardrails

- Issue key format validation (`ABC-123`)
- JQL maximum length limit
- Comment maximum length limit
- Optional Jira project allowlist
- Optional transition allowlist
- No destructive endpoints exposed in v0.1

## Command safety

ACLI commands are built from fixed command templates in code:

- `jira issue search`
- `jira issue get`
- `jira issue comment add`
- `jira issue transition`

No user-provided command fragments are executed as shell strings.

## Logging

Structured JSON logs capture:

- tool invocation and completion
- command execution failures
- policy violations

Sensitive credentials are not logged.

## Failure handling

Common ACLI failures are surfaced as typed errors:

- ACLI missing
- authentication missing
- command timeout
- malformed ACLI output

