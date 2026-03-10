# jira-mcp-bridge

`jira-mcp-bridge` is a local-only MCP server that gives AI coding agents a safe, typed Jira tool interface while using Atlassian ACLI internally.

## Why this exists

- Public contract: MCP tools (`jira_search`, `jira_get_issue`, `jira_add_comment`, `jira_transition_issue`)
- Internal implementation: ACLI subprocess calls
- Security objective: AI agents do not receive Jira tokens; ACLI owns auth state

## Architecture

AI Agent -> MCP Client -> `jira-mcp-bridge` (stdio MCP server) -> Atlassian ACLI -> Jira Cloud

See [architecture.md](docs/architecture.md) for details.

## Repository layout

```text
/server
/adapters/acli
/policies
/tests
/docs
README.md
LICENSE
.gitignore
```

## Features in v0.1

- Local stdio MCP server
- Typed and constrained Jira tools
- Input validation and policy guardrails
- ACLI adapter with timeout, output capture, error mapping
- Structured JSON logging
- Unit tests for validation, parsing, builders, and failure scenarios

## Configuration

Configuration is loaded from environment variables and optional JSON config file:

- `ACLI_PATH` (default: `acli`)
- `JIRA_PROJECT_ALLOWLIST` (csv; optional)
- `MAX_RESULTS` (default: `50`)
- `COMMENT_MAX_LENGTH` (default: `4000`)
- `COMMAND_TIMEOUT` (seconds; default: `30`)
- `TRANSITION_ALLOWLIST` (csv; optional)
- `JIRA_MCP_CONFIG` (path to JSON config; default: `jira-mcp-bridge.json` if present)
- `LOG_LEVEL` (default: `INFO`)

Example config file (`jira-mcp-bridge.json`):

```json
{
  "acli_path": "acli",
  "jira_project_allowlist": "ABC,PLAT",
  "max_results": 50,
  "comment_max_length": 4000,
  "command_timeout": 30,
  "transition_allowlist": "In Progress,Done",
  "log_level": "INFO"
}
```

## Run locally

```bash
python -m venv .venv
. .venv/bin/activate  # Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -e ".[dev]"
python -m server
```

## Configure MCP client (example)

```json
{
  "mcpServers": {
    "jira-mcp-bridge": {
      "command": "python",
      "args": ["-m", "server"],
      "env": {
        "ACLI_PATH": "acli",
        "JIRA_PROJECT_ALLOWLIST": "ABC,PLAT"
      }
    }
  }
}
```

## Tests

```bash
pytest
```

## Important notes

- ACLI command syntax can vary by ACLI version/distribution. If needed, update command builders in `adapters/acli/commands.py`.
- No direct Jira REST API calls are used in this version.
- No raw shell passthrough is exposed to MCP clients.

