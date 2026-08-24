import json

from agent_framework import Agent

from app.core.llm import get_chat_client
from app.core.prompts import REFINEMENT_PROMPT
from app.core.json_utils import extract_json


async def refine_architecture(
    requirements: dict,
    architecture: dict,
    technology: dict,
    validation: dict,
    feedback: str,
) -> dict:

    client = get_chat_client()

    agent = Agent(
        client=client,
        name="RefinementAgent",
        instructions=REFINEMENT_PROMPT,
    )

    response = await agent.run(
        f"""
REFINE THE ARCHITECTURE.

REQUIREMENTS
------------
{json.dumps(requirements, indent=2)}
------------

CURRENT ARCHITECTURE
--------------------
{json.dumps(architecture, indent=2)}
------------

CURRENT TECHNOLOGY
-------------------
{json.dumps(technology, indent=2)}
------------

VALIDATION
----------
{json.dumps(validation, indent=2)}
------------

DEVELOPER FEEDBACK
------------------
{feedback}
------------

Return only valid JSON.
"""
    )

    try:
        result = extract_json(response.text)
    except Exception as exc:
        raise ValueError(
            "Refinement Agent returned invalid JSON.\n\n"
            f"{exc}"
        ) from exc

    if not isinstance(result, dict):
        raise ValueError(
            "Refinement Agent did not return a JSON object."
        )

    return result
