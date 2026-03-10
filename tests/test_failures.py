from adapters.acli.client import AcliJiraClient
from adapters.acli.errors import (
    AcliAuthError,
    AcliCommandError,
    AcliNotInstalledError,
    AcliOutputParseError,
)
from adapters.acli.runner import CommandResult, SubprocessRunner
from server.config import Settings


class FakeRunner:
    def __init__(self, result: CommandResult) -> None:
        self.result = result

    def run(self, command: list[str], timeout_seconds: int) -> CommandResult:
        return self.result


def test_acli_missing_installation_raises() -> None:
    runner = SubprocessRunner()
    try:
        runner.run(["definitely_missing_acli_binary"], timeout_seconds=1)
        assert False, "expected AcliNotInstalledError"
    except AcliNotInstalledError:
        assert True


def test_authentication_missing_error_mapping() -> None:
    result = CommandResult(
        command=["acli"],
        exit_code=1,
        stdout="",
        stderr="Not authenticated. Please login.",
    )
    client = AcliJiraClient(settings=Settings(), runner=FakeRunner(result))
    try:
        client.search_issues("project = ABC", 5)
        assert False, "expected AcliAuthError"
    except AcliAuthError:
        assert True


def test_transition_failure_returns_command_error() -> None:
    result = CommandResult(
        command=["acli"],
        exit_code=2,
        stdout="",
        stderr="Transition not valid for current status",
    )
    client = AcliJiraClient(settings=Settings(), runner=FakeRunner(result))
    try:
        client.transition_issue("ABC-1", "Done")
        assert False, "expected AcliCommandError"
    except AcliCommandError:
        assert True


def test_malformed_cli_output_raises_parse_error() -> None:
    result = CommandResult(
        command=["acli"],
        exit_code=0,
        stdout="garbled",
        stderr="",
    )
    client = AcliJiraClient(settings=Settings(), runner=FakeRunner(result))
    try:
        client.get_issue("ABC-1")
        assert False, "expected AcliOutputParseError"
    except AcliOutputParseError:
        assert True

