"""Jira client implementation backed by ACLI."""

from __future__ import annotations

from typing import Any

from adapters.acli.commands import (
    build_add_comment_command,
    build_get_issue_command,
    build_search_command,
    build_transition_command,
)
from adapters.acli.errors import AcliAuthError, AcliCommandError
from adapters.acli.parser import (
    parse_comment_output,
    parse_get_issue_output,
    parse_search_output,
    parse_transition_output,
)
from adapters.acli.runner import CommandResult, SubprocessRunner
from policies.restrictions import enforce_command_allowlist
from server.config import Settings


AUTH_ERROR_MARKERS = (
    "not authenticated",
    "authentication",
    "login",
    "unauthorized",
    "forbidden",
)


class AcliJiraClient:
    """Typed Jira operations implemented via ACLI subprocess calls."""

    def __init__(self, settings: Settings, runner: SubprocessRunner | None = None) -> None:
        self.settings = settings
        self.runner = runner or SubprocessRunner()

    def search_issues(self, jql: str, limit: int) -> dict[str, Any]:
        command = build_search_command(self.settings, jql=jql, limit=limit)
        result = self._run_and_validate(command)
        return parse_search_output(result.stdout)

    def get_issue(self, issue_key: str) -> dict[str, Any]:
        command = build_get_issue_command(self.settings, issue_key=issue_key)
        result = self._run_and_validate(command)
        return parse_get_issue_output(result.stdout)

    def add_comment(self, issue_key: str, text: str) -> dict[str, Any]:
        command = build_add_comment_command(self.settings, issue_key=issue_key, text=text)
        result = self._run_and_validate(command)
        return parse_comment_output(result.stdout, issue_key=issue_key)

    def transition_issue(self, issue_key: str, transition: str) -> dict[str, Any]:
        command = build_transition_command(self.settings, issue_key=issue_key, transition=transition)
        result = self._run_and_validate(command)
        return parse_transition_output(result.stdout, issue_key=issue_key)

    def _run_and_validate(self, command: list[str]) -> CommandResult:
        enforce_command_allowlist(command, expected_executable=self.settings.acli_path)
        result = self.runner.run(command=command, timeout_seconds=self.settings.command_timeout)

        if result.exit_code != 0:
            stderr_lower = result.stderr.lower()
            if any(marker in stderr_lower for marker in AUTH_ERROR_MARKERS):
                raise AcliAuthError("ACLI is not authenticated. Run ACLI login first.")
            raise AcliCommandError(command=command, exit_code=result.exit_code, stderr=result.stderr)

        return result
