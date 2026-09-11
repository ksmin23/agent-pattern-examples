# Copyright (c) 2025 OpenAI
# SPDX-License-Identifier: MIT
# Based on openai/openai-agents-python.
# Original source: https://github.com/openai/openai-agents-python/blob/25af629b3c877ba3d0e95189141bb636b21167a5/examples/sandbox/misc/workspace_shell.py
# See THIRD_PARTY_NOTICES.md at the repository root for the full license text.

"""Connect the Agents SDK shell tool to the active sandbox session.

WorkspaceShellCapability forwards model-generated shell commands to the bound
session and converts backend results into SDK shell-tool outputs.
"""

from __future__ import annotations

from agents.sandbox import Capability, Manifest
from agents.sandbox.session.base_sandbox_session import BaseSandboxSession
from agents.tool import (
    ShellCallOutcome,
    ShellCommandOutput,
    ShellCommandRequest,
    ShellResult,
    ShellTool,
    Tool,
)


class WorkspaceShellCapability(Capability):
    """Expose one shell tool for inspecting the active sandbox workspace."""

    def __init__(self) -> None:
        super().__init__(type="workspace_shell")
        self._session: BaseSandboxSession | None = None

    def bind(self, session: BaseSandboxSession) -> None:
        self._session = session

    def tools(self) -> list[Tool]:
        return [ShellTool(executor=self._execute_shell)]

    async def instructions(self, manifest: Manifest) -> str | None:
        _ = manifest
        return (
            "Use the `shell` tool to inspect the sandbox workspace before answering. "
            "The workspace root is the current working directory, so prefer relative paths "
            "with commands like `pwd`, `find .`, and `cat`. Only cite files you actually read."
        )

    async def _execute_shell(self, request: ShellCommandRequest) -> ShellResult:
        if self._session is None:
            raise RuntimeError("Workspace shell is not bound to a sandbox session.")

        # Zero is intentionally equivalent to no explicit Shell action timeout.
        timeout_ms = request.data.action.timeout_ms
        timeout_s = timeout_ms / 1000 if timeout_ms else None
        outputs: list[ShellCommandOutput] = []
        for command in request.data.action.commands:
            result = await self._session.exec(command, timeout=timeout_s, shell=True)
            outputs.append(
                ShellCommandOutput(
                    command=command,
                    stdout=result.stdout.decode("utf-8", errors="replace"),
                    stderr=result.stderr.decode("utf-8", errors="replace"),
                    outcome=ShellCallOutcome(type="exit", exit_code=result.exit_code),
                )
            )
        return ShellResult(output=outputs)
