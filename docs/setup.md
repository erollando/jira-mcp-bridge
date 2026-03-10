# Setup

## 1. Install Atlassian ACLI

Install ACLI on your machine and ensure the executable is available in `PATH`, or set `ACLI_PATH`.

## 2. Authenticate ACLI

Authenticate ACLI to your Jira Cloud environment according to your ACLI distribution's login flow.

The MCP bridge relies on ACLI auth state and never handles Jira tokens directly.

## 3. Install and run jira-mcp-bridge

```bash
python -m venv .venv
. .venv/bin/activate  # Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -e ".[dev]"
python -m server
```

## 4. Configure environment

```bash
export ACLI_PATH=acli
export JIRA_PROJECT_ALLOWLIST=ABC,PLAT
export MAX_RESULTS=50
export COMMENT_MAX_LENGTH=4000
export COMMAND_TIMEOUT=30
export TRANSITION_ALLOWLIST="In Progress,Done"
```

Windows PowerShell:

```powershell
$env:ACLI_PATH = "acli"
$env:JIRA_PROJECT_ALLOWLIST = "ABC,PLAT"
$env:MAX_RESULTS = "50"
$env:COMMENT_MAX_LENGTH = "4000"
$env:COMMAND_TIMEOUT = "30"
$env:TRANSITION_ALLOWLIST = "In Progress,Done"
```

## 5. Configure Codex MCP client

Add a server entry in your MCP client configuration:

```json
{
  "mcpServers": {
    "jira-mcp-bridge": {
      "command": "python",
      "args": ["-m", "server"],
      "env": {
        "ACLI_PATH": "acli"
      }
    }
  }
}
```

