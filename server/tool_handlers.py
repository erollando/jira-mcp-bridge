"""Business logic for MCP tool execution."""

from __future__ import annotations

import logging
from typing import Any

from adapters.acli.client import AcliJiraClient
from adapters.acli.errors import AcliError
from policies.errors import PolicyError
from policies.restrictions import (
    enforce_issue_project_allowlist,
    enforce_jql_allowlist,
    enforce_transition_allowlist,
)
from policies.validation import (
    validate_comment_text,
    validate_issue_key,
    validate_jql,
    validate_limit,
    validate_transition,
)
from server.config import Settings


class JiraToolService:
    """Validates input, enforces policy, invokes ACLI adapter, and normalizes errors."""

    def __init__(self, settings: Settings, client: AcliJiraClient, logger: logging.Logger) -> None:
        self.settings = settings
        self.client = client
        self.logger = logger

    def jira_search(self, jql: str, limit: int | None = None) -> dict[str, Any]:
        self.logger.info("tool_call", extra={"extra": {"tool": "jira_search"}})
        try:
            safe_jql = validate_jql(jql)
            enforce_jql_allowlist(safe_jql, self.settings.jira_project_allowlist)
            safe_limit = validate_limit(limit, self.settings.max_results)
            response = self.client.search_issues(safe_jql, safe_limit)
            self.logger.info(
                "tool_success",
                extra={"extra": {"tool": "jira_search", "count": response.get("count", 0)}},
            )
            return response
        except (PolicyError, AcliError) as exc:
            return self._error("jira_search", exc)

    def jira_get_issue(self, issue_key: str) -> dict[str, Any]:
        self.logger.info("tool_call", extra={"extra": {"tool": "jira_get_issue"}})
        try:
            safe_key = validate_issue_key(issue_key)
            enforce_issue_project_allowlist(safe_key, self.settings.jira_project_allowlist)
            response = self.client.get_issue(safe_key)
            self.logger.info(
                "tool_success",
                extra={"extra": {"tool": "jira_get_issue", "issue_key": safe_key}},
            )
            return response
        except (PolicyError, AcliError) as exc:
            return self._error("jira_get_issue", exc)

    def jira_add_comment(self, issue_key: str, text: str) -> dict[str, Any]:
        self.logger.info("tool_call", extra={"extra": {"tool": "jira_add_comment"}})
        try:
            safe_key = validate_issue_key(issue_key)
            safe_text = validate_comment_text(text, self.settings.comment_max_length)
            enforce_issue_project_allowlist(safe_key, self.settings.jira_project_allowlist)
            response = self.client.add_comment(safe_key, safe_text)
            self.logger.info(
                "tool_success",
                extra={"extra": {"tool": "jira_add_comment", "issue_key": safe_key}},
            )
            return response
        except (PolicyError, AcliError) as exc:
            return self._error("jira_add_comment", exc)

    def jira_transition_issue(self, issue_key: str, transition: str) -> dict[str, Any]:
        self.logger.info("tool_call", extra={"extra": {"tool": "jira_transition_issue"}})
        try:
            safe_key = validate_issue_key(issue_key)
            safe_transition = validate_transition(transition)
            enforce_issue_project_allowlist(safe_key, self.settings.jira_project_allowlist)
            enforce_transition_allowlist(safe_transition, self.settings.transition_allowlist)
            response = self.client.transition_issue(safe_key, safe_transition)
            self.logger.info(
                "tool_success",
                extra={"extra": {"tool": "jira_transition_issue", "issue_key": safe_key}},
            )
            return response
        except (PolicyError, AcliError) as exc:
            return self._error("jira_transition_issue", exc)

    def _error(self, tool_name: str, exc: Exception) -> dict[str, Any]:
        self.logger.error(
            "tool_failure",
            extra={"extra": {"tool": tool_name, "error_type": type(exc).__name__, "error": str(exc)}},
        )
        return {"ok": False, "error": {"type": type(exc).__name__, "message": str(exc)}}

