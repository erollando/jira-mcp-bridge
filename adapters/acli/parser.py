"""Parsers that normalize ACLI output to predictable JSON."""

from __future__ import annotations

import json
from typing import Any

from adapters.acli.errors import AcliOutputParseError


def _load_json(stdout: str) -> Any:
    try:
        return json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise AcliOutputParseError("Malformed ACLI JSON output") from exc


def _get_nested(data: dict[str, Any], path: list[str]) -> Any:
    cursor: Any = data
    for key in path:
        if not isinstance(cursor, dict):
            return None
        cursor = cursor.get(key)
    return cursor


def normalize_issue(raw: dict[str, Any]) -> dict[str, Any]:
    fields = raw.get("fields", {}) if isinstance(raw.get("fields"), dict) else {}

    key = raw.get("key") or raw.get("issueKey") or fields.get("key")
    summary = fields.get("summary") or raw.get("summary")
    status = (
        _get_nested(fields, ["status", "name"])
        or raw.get("status")
        or _get_nested(raw, ["status", "name"])
    )
    assignee = (
        _get_nested(fields, ["assignee", "displayName"])
        or fields.get("assignee")
        or raw.get("assignee")
    )
    url = (
        raw.get("url")
        or raw.get("self")
        or fields.get("url")
        or _get_nested(raw, ["links", "browse"])
    )

    return {
        "key": key,
        "summary": summary,
        "status": status,
        "assignee": assignee,
        "url": url,
    }


def parse_search_output(stdout: str) -> dict[str, Any]:
    data = _load_json(stdout)

    if isinstance(data, list):
        issues = data
    elif isinstance(data, dict):
        issues = data.get("issues") or data.get("results") or []
    else:
        raise AcliOutputParseError("Unexpected search output shape")

    if not isinstance(issues, list):
        raise AcliOutputParseError("Search output did not contain a list of issues")

    normalized = [normalize_issue(issue) for issue in issues if isinstance(issue, dict)]
    return {
        "issues": normalized,
        "count": len(normalized),
    }


def parse_get_issue_output(stdout: str) -> dict[str, Any]:
    data = _load_json(stdout)

    if isinstance(data, dict) and "issue" in data and isinstance(data["issue"], dict):
        return normalize_issue(data["issue"])
    if isinstance(data, dict):
        return normalize_issue(data)
    raise AcliOutputParseError("Unexpected get-issue output shape")


def parse_comment_output(stdout: str, issue_key: str) -> dict[str, Any]:
    data = _load_json(stdout)
    if not isinstance(data, dict):
        raise AcliOutputParseError("Unexpected add-comment output shape")

    message = data.get("message") or data.get("result") or "comment added"
    issue_data = data.get("issue")
    issue = normalize_issue(issue_data) if isinstance(issue_data, dict) else {"key": issue_key}
    return {"ok": True, "message": str(message), "issue": issue}


def parse_transition_output(stdout: str, issue_key: str) -> dict[str, Any]:
    data = _load_json(stdout)
    if not isinstance(data, dict):
        raise AcliOutputParseError("Unexpected transition output shape")

    issue_data = data.get("issue")
    issue = normalize_issue(issue_data) if isinstance(issue_data, dict) else {"key": issue_key}
    transition = data.get("transition") or data.get("status") or data.get("message")
    return {"ok": True, "transition": transition, "issue": issue}

