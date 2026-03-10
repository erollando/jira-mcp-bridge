"""Execution restrictions and allowlist enforcement."""

from __future__ import annotations

import re

from policies.errors import PolicyError


PROJECT_EQ_PATTERN = re.compile(r"\bproject\s*=\s*([A-Za-z][A-Za-z0-9_]*)", flags=re.IGNORECASE)
PROJECT_IN_PATTERN = re.compile(r"\bproject\s+in\s*\(([^)]+)\)", flags=re.IGNORECASE)
ALLOWED_COMMAND_PREFIXES = (
    ("jira", "issue", "search"),
    ("jira", "issue", "get"),
    ("jira", "issue", "comment", "add"),
    ("jira", "issue", "transition"),
)


def enforce_issue_project_allowlist(issue_key: str, allowlist: tuple[str, ...]) -> None:
    if not allowlist:
        return
    project = issue_key.split("-", 1)[0].upper()
    if project not in allowlist:
        raise PolicyError(f"Project {project} is not allowed by JIRA_PROJECT_ALLOWLIST.")


def _extract_projects_from_jql(jql: str) -> set[str]:
    projects: set[str] = set()

    for match in PROJECT_EQ_PATTERN.finditer(jql):
        projects.add(match.group(1).strip().upper())

    for match in PROJECT_IN_PATTERN.finditer(jql):
        raw = match.group(1)
        for item in raw.split(","):
            token = item.strip().strip("'\"").upper()
            if token:
                projects.add(token)

    return projects


def enforce_jql_allowlist(jql: str, allowlist: tuple[str, ...]) -> None:
    if not allowlist:
        return

    allowed = {project.upper() for project in allowlist}
    projects = _extract_projects_from_jql(jql)

    if not projects:
        raise PolicyError(
            "JQL must include a project constraint when JIRA_PROJECT_ALLOWLIST is configured."
        )

    disallowed = sorted(project for project in projects if project not in allowed)
    if disallowed:
        raise PolicyError(
            f"JQL references disallowed project(s): {', '.join(disallowed)}."
        )


def enforce_transition_allowlist(transition: str, allowlist: tuple[str, ...]) -> None:
    if not allowlist:
        return
    allowed = {item.strip().lower() for item in allowlist if item.strip()}
    if transition.strip().lower() not in allowed:
        raise PolicyError("Transition is not in TRANSITION_ALLOWLIST.")


def enforce_command_allowlist(command: list[str], expected_executable: str) -> None:
    if not command:
        raise PolicyError("Refusing to execute empty ACLI command.")
    if command[0] != expected_executable:
        raise PolicyError("Refusing to execute unexpected ACLI executable.")

    command_body = tuple(command[1:])
    for allowed in ALLOWED_COMMAND_PREFIXES:
        if command_body[: len(allowed)] == allowed:
            return

    raise PolicyError("Command is not in allowed ACLI command list.")
