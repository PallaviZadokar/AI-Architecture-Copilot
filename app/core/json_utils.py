import json
import re
from typing import Any


def extract_json(text: str) -> Any:
    """
    Safely extract JSON from an LLM response.

    Handles responses such as:

    {
        "name": "value"
    }

    and:

    ```json
    {
        "name": "value"
    }
    ```

    and responses where the model accidentally adds
    explanatory text before/after the JSON.
    """

    if not text:
        raise ValueError("LLM returned an empty response.")

    text = text.strip()

    # ---------------------------------------------------------
    # 1. Remove Markdown code fences
    # ---------------------------------------------------------

    if text.startswith("```"):
        text = re.sub(
            r"^```(?:json)?\s*",
            "",
            text,
            flags=re.IGNORECASE,
        )

        text = re.sub(
            r"\s*```$",
            "",
            text,
        )

        text = text.strip()

    # ---------------------------------------------------------
    # 2. Try parsing the complete response
    # ---------------------------------------------------------

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # ---------------------------------------------------------
    # 3. Try to find JSON object
    # ---------------------------------------------------------

    object_match = re.search(
        r"\{.*\}",
        text,
        flags=re.DOTALL,
    )

    if object_match:
        candidate = object_match.group(0)

        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    # ---------------------------------------------------------
    # 4. Try to find JSON array
    # ---------------------------------------------------------

    array_match = re.search(
        r"\[.*\]",
        text,
        flags=re.DOTALL,
    )

    if array_match:
        candidate = array_match.group(0)

        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    # ---------------------------------------------------------
    # 5. Give useful debugging information
    # ---------------------------------------------------------

    preview = text[:2000]

    raise ValueError(
        "Unable to parse LLM response as JSON.\n\n"
        f"LLM response:\n{preview}"
    )
