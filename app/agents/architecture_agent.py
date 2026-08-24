import json

from agent_framework import Agent

from app.core.llm import get_chat_client
from app.core.prompts import ARCHITECTURE_PROMPT
from app.core.json_utils import extract_json


async def generate_architecture(
    requirements: dict,
) -> dict:

    client = get_chat_client()

    agent = Agent(
        client=client,
        name="ArchitectureAgent",
        instructions=ARCHITECTURE_PROMPT,
    )

    response = await agent.run(
        f"""
Create a high-level solution architecture.

REQUIREMENTS
------------
{json.dumps(requirements, indent=2)}
------------

Return only valid JSON.
"""
    )

    try:
        result = extract_json(response.text)
    except Exception as exc:
        raise ValueError(
            "Architecture Agent returned invalid JSON.\n\n"
            f"{exc}"
        ) from exc

    if not isinstance(result, dict):
        raise ValueError(
            "Architecture Agent did not return a JSON object."
        )

    return result
