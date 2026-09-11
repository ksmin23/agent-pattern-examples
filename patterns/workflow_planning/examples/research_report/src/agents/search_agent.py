# Copyright (c) 2025 OpenAI
# SPDX-License-Identifier: MIT
# Based on openai/openai-agents-python.
# Original source: https://github.com/openai/openai-agents-python/blob/25af629b3c877ba3d0e95189141bb636b21167a5/examples/research_bot/agents/search_agent.py
# See THIRD_PARTY_NOTICES.md at the repository root for the full license text.

"""Define the web-search agent used for each item in a research plan.

ResearchManager invokes this agent once per planned search and later passes the
collected summaries to the writer agent.
"""

from agents import Agent, WebSearchTool

INSTRUCTIONS = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce a concise summary of the results. The summary must be 2-3 paragraphs and less than 300 "
    "words. Capture the main points. Write succinctly, no need to have complete sentences or good "
    "grammar. This will be consumed by someone synthesizing a report, so its vital you capture the "
    "essence and ignore any fluff. Do not include any additional commentary other than the summary "
    "itself."
)

search_agent = Agent(
    name="Search agent",
    model="gpt-5.6-sol",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool()],
)
