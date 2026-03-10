"""Configuration handling for jira-mcp-bridge."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_CONFIG_PATH = "jira-mcp-bridge.json"


def _parse_csv(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return [str(item).strip().upper() for item in value if str(item).strip()]
    return [item.strip().upper() for item in str(value).split(",") if item.strip()]


def _parse_int(value: Any, fallback: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


@dataclass(frozen=True)
class Settings:
    """Application runtime settings."""

    acli_path: str = "acli"
    jira_project_allowlist: tuple[str, ...] = ()
    max_results: int = 50
    comment_max_length: int = 4000
    command_timeout: int = 30
    transition_allowlist: tuple[str, ...] = ()
    log_level: str = "INFO"
    config_path: str | None = None

    @staticmethod
    def from_env() -> "Settings":
        raw: dict[str, Any] = {}
        config_path = os.getenv("JIRA_MCP_CONFIG", DEFAULT_CONFIG_PATH)
        path = Path(config_path)
        if path.exists():
            loaded = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                raw = loaded

        env_acli_path = os.getenv("ACLI_PATH")
        env_allowlist = _parse_csv(os.getenv("JIRA_PROJECT_ALLOWLIST"))
        env_max_results = os.getenv("MAX_RESULTS")
        env_comment_max = os.getenv("COMMENT_MAX_LENGTH")
        env_timeout = os.getenv("COMMAND_TIMEOUT")
        env_transition_allowlist = _parse_csv(os.getenv("TRANSITION_ALLOWLIST"))
        env_log_level = os.getenv("LOG_LEVEL")

        acli_path = env_acli_path or raw.get("acli_path") or "acli"
        allowlist = tuple(env_allowlist or _parse_csv(raw.get("jira_project_allowlist")))
        max_results = _parse_int(env_max_results or raw.get("max_results"), 50)
        comment_max_length = _parse_int(env_comment_max or raw.get("comment_max_length"), 4000)
        command_timeout = _parse_int(env_timeout or raw.get("command_timeout"), 30)
        transition_allowlist = tuple(
            env_transition_allowlist or _parse_csv(raw.get("transition_allowlist"))
        )
        log_level = (env_log_level or raw.get("log_level") or "INFO").upper()

        return Settings(
            acli_path=acli_path,
            jira_project_allowlist=allowlist,
            max_results=max(1, max_results),
            comment_max_length=max(1, comment_max_length),
            command_timeout=max(1, command_timeout),
            transition_allowlist=transition_allowlist,
            log_level=log_level,
            config_path=str(path) if path.exists() else None,
        )
