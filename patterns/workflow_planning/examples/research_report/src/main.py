# Copyright (c) 2025 OpenAI
# SPDX-License-Identifier: MIT
# Based on openai/openai-agents-python.
# Original source: https://github.com/openai/openai-agents-python/blob/25af629b3c877ba3d0e95189141bb636b21167a5/examples/research_bot/main.py
# See THIRD_PARTY_NOTICES.md at the repository root for the full license text.

"""Provide the command-line entry point for the research-report workflow.

The entry point collects a topic and delegates planning, parallel search, and
report writing to ResearchManager.
"""

import asyncio

from .manager import ResearchManager


async def main() -> None:
    query = input("What would you like to research? ")
    await ResearchManager().run(query)


if __name__ == "__main__":
    asyncio.run(main())
