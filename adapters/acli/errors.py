"""Custom errors for ACLI integration."""

from __future__ import annotations


class AcliError(RuntimeError):
    """Base error type for ACLI failures."""


class AcliNotInstalledError(AcliError):
    """ACLI executable was not found."""


class AcliTimeoutError(AcliError):
    """ACLI command exceeded timeout."""

    def __init__(self, command: list[str], timeout_seconds: int) -> None:
        super().__init__(f"ACLI command timed out after {timeout_seconds}s")
        self.command = command
        self.timeout_seconds = timeout_seconds


class AcliAuthError(AcliError):
    """ACLI authentication missing or invalid."""


class AcliCommandError(AcliError):
    """ACLI returned a non-zero exit code."""

    def __init__(self, command: list[str], exit_code: int, stderr: str) -> None:
        super().__init__(f"ACLI command failed with exit code {exit_code}")
        self.command = command
        self.exit_code = exit_code
        self.stderr = stderr


class AcliOutputParseError(AcliError):
    """ACLI output could not be parsed or normalized."""

