"""Subprocess execution for ACLI commands."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass

from adapters.acli.errors import AcliNotInstalledError, AcliTimeoutError


@dataclass(frozen=True)
class CommandResult:
    command: list[str]
    exit_code: int
    stdout: str
    stderr: str


class SubprocessRunner:
    """Executes ACLI commands with timeout and captured output."""

    def run(self, command: list[str], timeout_seconds: int) -> CommandResult:
        try:
            proc = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                check=False,
            )
        except FileNotFoundError as exc:
            raise AcliNotInstalledError("ACLI executable not found. Check ACLI_PATH.") from exc
        except subprocess.TimeoutExpired as exc:
            raise AcliTimeoutError(command=command, timeout_seconds=timeout_seconds) from exc

        return CommandResult(
            command=command,
            exit_code=proc.returncode,
            stdout=(proc.stdout or "").strip(),
            stderr=(proc.stderr or "").strip(),
        )

