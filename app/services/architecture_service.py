from app.agents.requirements_agent import (
    analyze_requirements,
)

from app.agents.architecture_agent import (
    generate_architecture,
)

from app.agents.technology_agent import (
    recommend_technology,
)

from app.agents.validation_agent import (
    validate_architecture,
)

from app.agents.refinement_agent import (
    refine_architecture,
)


async def generate_initial_architecture(
    project_input: str,
) -> dict:

    requirements = await analyze_requirements(
        project_input
    )

    architecture = await generate_architecture(
        requirements
    )

    technology = await recommend_technology(
        requirements,
        architecture,
    )

    validation = await validate_architecture(
        requirements,
        architecture,
        technology,
    )

    return {
        "project_summary": requirements.get(
            "project_summary",
            "Architecture",
        ),
        "requirements": requirements,
        "architecture": architecture,
        "technology_stack": technology,
        "validation": validation,
        "developer_feedback": None,
        "change_summary": [],
    }


async def generate_final_architecture(
    initial_result: dict,
    feedback: str,
) -> dict:

    refined = await refine_architecture(
        requirements=initial_result[
            "requirements"
        ],
        architecture=initial_result[
            "architecture"
        ],
        technology=initial_result[
            "technology_stack"
        ],
        validation=initial_result[
            "validation"
        ],
        feedback=feedback,
    )

    if "architecture" not in refined:
        raise ValueError(
            "Refinement Agent did not return an architecture."
        )

    refined["requirements"] = (
        initial_result["requirements"]
    )

    refined["developer_feedback"] = feedback

    if "technology_stack" not in refined:
        refined["technology_stack"] = (
            initial_result["technology_stack"]
        )

    if "validation" not in refined:
        refined["validation"] = (
            initial_result["validation"]
        )

    return refined
