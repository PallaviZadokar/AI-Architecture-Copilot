import json

from agent_framework import Agent

from app.core.llm import get_chat_client
from app.core.prompts import REQUIREMENTS_PROMPT
from app.core.json_utils import extract_json


async def analyze_requirements(project_input: str) -> dict:

    client = get_chat_client()

    agent = Agent(
        client=client,
        name="RequirementsAgent",
        instructions=REQUIREMENTS_PROMPT,
    )

    response = await agent.run(
        f"""
Analyze this project.

PROJECT INPUT
-------------
{project_input}
-------------

Return only the required JSON object.
"""
    )

    raw_text = response.text

    try:
        result = extract_json(raw_text)
    except Exception as exc:
        raise ValueError(
            "Requirements Agent returned invalid JSON.\n\n"
            f"{exc}"
        ) from exc

    if not isinstance(result, dict):
        raise ValueError(
            "Requirements Agent did not return a JSON object."
        )

    return result
