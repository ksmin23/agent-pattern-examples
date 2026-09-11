# Copyright (c) 2025 OpenAI
# SPDX-License-Identifier: MIT
# Based on openai/openai-agents-python.
# Original source: https://github.com/openai/openai-agents-python/blob/25af629b3c877ba3d0e95189141bb636b21167a5/examples/research_bot/agents/planner_agent.py
# See THIRD_PARTY_NOTICES.md at the repository root for the full license text.

"""Define the planner agent and its structured search-plan output.

ResearchManager runs this agent first to turn a broad query into independent
web searches that the search stage can execute concurrently.
"""

from openai.types.shared.reasoning import Reasoning
from pydantic import BaseModel

from agents import Agent, ModelSettings

PROMPT = (
    "You are a helpful research assistant. Given a query, come up with a set of web searches "
    "to perform to best answer the query. Output between 5 and 20 terms to query for."
)


class WebSearchItem(BaseModel):
    reason: str
    "Your reasoning for why this search is important to the query."

    query: str
    "The search term to use for the web search."


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem]
    """A list of web searches to perform to best answer the query."""


planner_agent = Agent(
    name="PlannerAgent",
    instructions=PROMPT,
    model="gpt-5.6-sol",
    model_settings=ModelSettings(reasoning=Reasoning(effort="medium")),
    output_type=WebSearchPlan,
)
