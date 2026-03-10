# Architecture

## Goal

Expose a minimal Jira capability surface to AI agents through MCP, while enforcing local guardrails and keeping ACLI as a private implementation detail.

## Data flow

1. AI agent calls a typed MCP tool.
2. MCP server validates input and applies policy restrictions.
3. ACLI adapter builds a fixed command list and runs ACLI as subprocess.
4. ACLI output is parsed and normalized to stable JSON objects.
5. MCP tool returns structured response.

## Components

- `server/mcp_server.py`
  - Registers MCP tools and runs stdio transport
- `server/tool_handlers.py`
  - Tool orchestration, policy enforcement, error normalization
- `adapters/acli/commands.py`
  - Fixed command builders (no passthrough)
- `adapters/acli/runner.py`
  - Process execution, timeout handling, stdout/stderr capture
- `adapters/acli/parser.py`
  - JSON parse + normalization layer
- `policies/*`
  - Validation, allowlists, and write restrictions

## Public contract vs internal detail

- Public contract: MCP tools and their typed inputs/JSON outputs
- Internal detail: ACLI command syntax and subprocess implementation

This separation keeps clients stable if ACLI invocation details change.

