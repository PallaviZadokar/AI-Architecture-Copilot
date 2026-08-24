import json

from agent_framework import Agent

from app.core.llm import get_chat_client
from app.core.prompts import VALIDATION_PROMPT
from app.core.json_utils import extract_json


async def validate_architecture(
    requirements: dict,
    architecture: dict,
    technology: dict,
) -> dict:

    client = get_chat_client()

    agent = Agent(
        client=client,
        name="ValidationAgent",
        instructions=VALIDATION_PROMPT,
    )

    response = await agent.run(
        f"""
Validate the following solution architecture.

REQUIREMENTS
------------
{json.dumps(requirements, indent=2)}
------------

ARCHITECTURE
------------
{json.dumps(architecture, indent=2)}
------------

TECHNOLOGY STACK
----------------
{json.dumps(technology, indent=2)}
------------

Return only valid JSON.
"""
    )

    try:
        result = extract_json(response.text)
    except Exception as exc:
        raise ValueError(
            "Validation Agent returned invalid JSON.\n\n"
            f"{exc}"
        ) from exc

    if not isinstance(result, dict):
        raise ValueError(
            "Validation Agent did not return a JSON object."
        )

    return result
