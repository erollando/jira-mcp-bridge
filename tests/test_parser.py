from adapters.acli.errors import AcliOutputParseError
from adapters.acli.parser import parse_get_issue_output, parse_search_output


def test_parse_search_output_normalizes_fields() -> None:
    stdout = """
    {"issues":[{"key":"ABC-1","fields":{"summary":"hello","status":{"name":"In Progress"},"assignee":{"displayName":"Jane"}},"url":"https://example.atlassian.net/browse/ABC-1"}]}
    """.strip()
    result = parse_search_output(stdout)
    assert result["count"] == 1
    issue = result["issues"][0]
    assert issue["key"] == "ABC-1"
    assert issue["status"] == "In Progress"
    assert issue["assignee"] == "Jane"


def test_parse_get_issue_output_accepts_wrapped_issue() -> None:
    stdout = """
    {"issue":{"key":"ABC-2","fields":{"summary":"wrapped issue"}}}
    """.strip()
    issue = parse_get_issue_output(stdout)
    assert issue["key"] == "ABC-2"
    assert issue["summary"] == "wrapped issue"


def test_parse_output_rejects_malformed_json() -> None:
    try:
        parse_search_output("not-json")
        assert False, "expected AcliOutputParseError"
    except AcliOutputParseError:
        assert True

