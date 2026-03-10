from policies.errors import PolicyError
from policies.restrictions import (
    enforce_command_allowlist,
    enforce_issue_project_allowlist,
    enforce_jql_allowlist,
    enforce_transition_allowlist,
)
from policies.validation import (
    validate_comment_text,
    validate_issue_key,
    validate_jql,
    validate_limit,
)


def test_validate_issue_key_accepts_valid_key() -> None:
    assert validate_issue_key("abc-123") == "ABC-123"


def test_validate_issue_key_rejects_invalid_key() -> None:
    try:
        validate_issue_key("abc123")
        assert False, "expected PolicyError"
    except PolicyError:
        assert True


def test_validate_jql_length_limit() -> None:
    long_jql = "x" * 1001
    try:
        validate_jql(long_jql)
        assert False, "expected PolicyError"
    except PolicyError:
        assert True


def test_validate_limit_caps_value() -> None:
    assert validate_limit(500, 50) == 50


def test_comment_text_rejects_oversized() -> None:
    try:
        validate_comment_text("x" * 11, 10)
        assert False, "expected PolicyError"
    except PolicyError:
        assert True


def test_issue_project_allowlist_rejects_wrong_project() -> None:
    try:
        enforce_issue_project_allowlist("XYZ-1", ("ABC",))
        assert False, "expected PolicyError"
    except PolicyError:
        assert True


def test_jql_allowlist_requires_project_clause() -> None:
    try:
        enforce_jql_allowlist("status = Open", ("ABC",))
        assert False, "expected PolicyError"
    except PolicyError:
        assert True


def test_transition_allowlist_rejects_disallowed() -> None:
    try:
        enforce_transition_allowlist("Done", ("In Progress",))
        assert False, "expected PolicyError"
    except PolicyError:
        assert True


def test_command_allowlist_rejects_unknown_action() -> None:
    try:
        enforce_command_allowlist(["acli", "jira", "project", "delete"], "acli")
        assert False, "expected PolicyError"
    except PolicyError:
        assert True
