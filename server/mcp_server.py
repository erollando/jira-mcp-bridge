"""Local stdio MCP server exposing constrained Jira tools."""

from __future__ import annotations

import logging
from typing import Any

from adapters.acli.client import AcliJiraClient
from mcp.server.fastmcp import FastMCP
from server.config import Settings
from server.logging import configure_logging
from server.tool_handlers import JiraToolService


settings = Settings.from_env()
configure_logging(settings.log_level)
logger = logging.getLogger("jira-mcp-bridge")
client = AcliJiraClient(settings=settings)
service = JiraToolService(settings=settings, client=client, logger=logger)

mcp = FastMCP(name="jira-mcp-bridge")


@mcp.tool()
def jira_search(jql: str, limit: int | None = None) -> dict[str, Any]:
    """Search Jira issues by JQL and return normalized issue results."""
    return service.jira_search(jql=jql, limit=limit)


@mcp.tool()
def jira_get_issue(issue_key: str) -> dict[str, Any]:
    """Get a single Jira issue by key."""
    return service.jira_get_issue(issue_key=issue_key)


@mcp.tool()
def jira_add_comment(issue_key: str, text: str) -> dict[str, Any]:
    """Add a comment to a Jira issue."""
    return service.jira_add_comment(issue_key=issue_key, text=text)


@mcp.tool()
def jira_transition_issue(issue_key: str, transition: str) -> dict[str, Any]:
    """Transition a Jira issue."""
    return service.jira_transition_issue(issue_key=issue_key, transition=transition)


def run() -> None:
    """Run the server with stdio transport."""
    logger.info("server_start", extra={"extra": {"transport": "stdio"}})
    mcp.run(transport="stdio")


if __name__ == "__main__":
    run()

