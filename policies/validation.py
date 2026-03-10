"""Input validation policies for MCP tools."""

from __future__ import annotations

import re

from policies.errors import PolicyError


ISSUE_KEY_PATTERN = re.compile(r"^[A-Z][A-Z0-9]+-\d+$")
MAX_JQL_LENGTH = 1000


def validate_issue_key(issue_key: str) -> str:
    value = issue_key.strip().upper()
    if not ISSUE_KEY_PATTERN.match(value):
        raise PolicyError("Invalid issue_key format. Expected format like ABC-123.")
    return value


def validate_jql(jql: str) -> str:
    value = jql.strip()
    if not value:
        raise PolicyError("JQL cannot be empty.")
    if len(value) > MAX_JQL_LENGTH:
        raise PolicyError(f"JQL exceeds max length of {MAX_JQL_LENGTH}.")
    return value


def validate_limit(limit: int | None, max_results: int) -> int:
    if limit is None:
        return max_results
    if limit <= 0:
        raise PolicyError("limit must be greater than zero.")
    return min(limit, max_results)


def validate_comment_text(text: str, max_length: int) -> str:
    value = text.strip()
    if not value:
        raise PolicyError("Comment text cannot be empty.")
    if len(value) > max_length:
        raise PolicyError(f"Comment exceeds max length of {max_length}.")
    return value


def validate_transition(transition: str) -> str:
    value = transition.strip()
    if not value:
        raise PolicyError("transition cannot be empty.")
    if len(value) > 64:
        raise PolicyError("transition is too long.")
    return value

