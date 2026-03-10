from adapters.acli.commands import (
    build_add_comment_command,
    build_get_issue_command,
    build_search_command,
    build_transition_command,
)
from server.config import Settings


def test_build_search_command_caps_limit() -> None:
    settings = Settings(max_results=25)
    command = build_search_command(settings, jql="project = ABC", limit=200)
    assert command == [
        "acli",
        "jira",
        "issue",
        "search",
        "--jql",
        "project = ABC",
        "--limit",
        "25",
        "--output",
        "json",
    ]


def test_build_get_issue_command() -> None:
    settings = Settings(acli_path="/usr/local/bin/acli")
    command = build_get_issue_command(settings, issue_key="ABC-1")
    assert command == [
        "/usr/local/bin/acli",
        "jira",
        "issue",
        "get",
        "ABC-1",
        "--output",
        "json",
    ]


def test_build_add_comment_command() -> None:
    settings = Settings()
    command = build_add_comment_command(settings, issue_key="ABC-1", text="hello")
    assert command[0:6] == ["acli", "jira", "issue", "comment", "add", "ABC-1"]
    assert "--text" in command


def test_build_transition_command() -> None:
    settings = Settings()
    command = build_transition_command(settings, issue_key="ABC-1", transition="Done")
    assert command[0:5] == ["acli", "jira", "issue", "transition", "ABC-1"]
    assert "--transition" in command

