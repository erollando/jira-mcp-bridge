"""Safe command builders for Jira ACLI operations."""

from __future__ import annotations

from server.config import Settings


def build_search_command(settings: Settings, jql: str, limit: int) -> list[str]:
    capped_limit = min(limit, settings.max_results)
    return [
        settings.acli_path,
        "jira",
        "issue",
        "search",
        "--jql",
        jql,
        "--limit",
        str(capped_limit),
        "--output",
        "json",
    ]


def build_get_issue_command(settings: Settings, issue_key: str) -> list[str]:
    return [
        settings.acli_path,
        "jira",
        "issue",
        "get",
        issue_key,
        "--output",
        "json",
    ]


def build_add_comment_command(settings: Settings, issue_key: str, text: str) -> list[str]:
    return [
        settings.acli_path,
        "jira",
        "issue",
        "comment",
        "add",
        issue_key,
        "--text",
        text,
        "--output",
        "json",
    ]


def build_transition_command(settings: Settings, issue_key: str, transition: str) -> list[str]:
    return [
        settings.acli_path,
        "jira",
        "issue",
        "transition",
        issue_key,
        "--transition",
        transition,
        "--output",
        "json",
    ]

