import json

from agent_framework import Agent

from app.core.llm import get_chat_client
from app.core.prompts import TECHNOLOGY_PROMPT
from app.core.json_utils import extract_json


async def recommend_technology(
    requirements: dict,
    architecture: dict,
) -> dict:

    client = get_chat_client()

    agent = Agent(
        client=client,
        name="TechnologyAgent",
        instructions=TECHNOLOGY_PROMPT,
    )

    response = await agent.run(
        f"""
Select the technology stack for this solution.

REQUIREMENTS
------------
{json.dumps(requirements, indent=2)}
------------

ARCHITECTURE
------------
{json.dumps(architecture, indent=2)}
------------

Return only valid JSON.
"""
    )

    raw_text = response.text

    try:
        result = extract_json(raw_text)
    except Exception as exc:
        raise ValueError(
            "Technology Agent returned invalid JSON.\n\n"
            f"{exc}\n\n"
            f"Raw model response:\n{raw_text[:4000]}"
        ) from exc

    if not isinstance(result, dict):
        raise ValueError(
            "Technology Agent did not return a JSON object."
        )

    if "recommendations" not in result:
        raise ValueError(
            "Technology Agent JSON is missing "
            "'recommendations'."
        )

    return result
