def render_architecture(result: dict) -> str:

    architecture = result.get(
        "architecture",
        {},
    )

    technology = result.get(
        "technology",
        {},
    )

    validation = result.get(
        "validation",
        {},
    )

    output = []

    # =========================================================
    # TITLE
    # =========================================================

    output.append(
        f"# {architecture.get('project_summary', 'Solution Architecture')}"
    )

    # =========================================================
    # ARCHITECTURE STYLE
    # =========================================================

    style = architecture.get(
        "architecture_style",
        {},
    )

    output.append("\n## Architecture Style")

    if isinstance(style, dict):

        output.append(
            f"**{style.get('name', 'N/A')}**"
        )

        output.append(
            style.get(
                "description",
                "",
            )
        )

    else:

        output.append(str(style))

    # =========================================================
    # DIAGRAM
    # =========================================================

    output.append("\n## High-Level Architecture")

    output.append(
        generate_mermaid_diagram(
            architecture
        )
    )

    # =========================================================
    # COMPONENTS
    # =========================================================

    output.append("\n## Architecture Components")

    for component in architecture.get(
        "components",
        [],
    ):

        output.append(
            f"""
### {component.get('name', 'Component')}

**Technology:** {component.get('technology', 'N/A')}

**Responsibility:** {component.get('responsibility', 'N/A')}

**Alternative:** {', '.join(component.get('alternatives', [])) or 'None'}

**Rationale:** {component.get('rationale', 'N/A')}
"""
        )

    # =========================================================
    # DATA FLOW
    # =========================================================

    data_flow = architecture.get(
        "data_flow",
        [],
    )

    if data_flow:

        output.append("\n## Data Flow")

        for item in data_flow:

            output.append(
                f"- {item}"
            )

    # =========================================================
    # INTEGRATIONS
    # =========================================================

    integrations = architecture.get(
        "integrations",
        [],
    )

    if integrations:

        output.append("\n## External Integrations")

        for item in integrations:

            output.append(
                f"- {item}"
            )

    # =========================================================
    # TECHNOLOGY STACK
    # =========================================================

    recommendations = technology.get(
        "recommendations",
        [],
    )

    if recommendations:

        output.append(
            "\n## Technology Stack"
        )

        for item in recommendations:

            output.append(
                f"""
### {item.get('category', 'Technology')}

**Technology:** {item.get('technology', 'N/A')}

**Description:** {item.get('description', 'N/A')}

**Alternative:** {', '.join(item.get('alternatives', [])) or 'None'}

**Rationale:** {item.get('rationale', 'N/A')}

**Risks:** {', '.join(item.get('risks', [])) or 'None'}
"""
            )

    # =========================================================
    # SECURITY
    # =========================================================

    security = architecture.get(
        "security_considerations",
        [],
    )

    if security:

        output.append(
            "\n## Security Considerations"
        )

        for item in security:

            output.append(
                f"- {item}"
            )

    # =========================================================
    # SCALABILITY
    # =========================================================

    scalability = architecture.get(
        "scalability_considerations",
        [],
    )

    if scalability:

        output.append(
            "\n## Scalability Considerations"
        )

        for item in scalability:

            output.append(
                f"- {item}"
            )

    # =========================================================
    # VALIDATION
    # =========================================================

    output.append("\n## Architecture Validation")

    output.append(
        f"**Status:** {validation.get('overall_status', 'N/A')}"
    )

    strengths = validation.get(
        "strengths",
        [],
    )

    if strengths:

        output.append("\n### Strengths")

        for item in strengths:

            output.append(
                f"- {item}"
            )

    issues = validation.get(
        "issues",
        [],
    )

    if issues:

        output.append("\n### Issues")

        for item in issues:

            output.append(
                f"- {item}"
            )

    risks = validation.get(
        "risks",
        [],
    )

    if risks:

        output.append("\n### Risks")

        for item in risks:

            output.append(
                f"- {item}"
            )

    return "\n".join(output)


def generate_mermaid_diagram(
    architecture: dict,
) -> str:

    """
    Generate a simple presentation-friendly Mermaid diagram.

    The diagram intentionally stays high-level.
    """

    components = architecture.get(
        "components",
        [],
    )

    frontend = None
    backend = None
    database = None
    cache = None

    for component in components:

        name = component.get(
            "name",
            "",
        ).lower()

        technology = component.get(
            "technology",
            "",
        )

        if "frontend" in name:

            frontend = technology

        elif (
            "backend" in name
            or "api" in name
        ):

            backend = technology

        elif (
            "database" in name
            or "data" in name
        ):

            database = technology

        elif (
            "cache" in name
            or "redis" in technology.lower()
        ):

            cache = technology

    frontend = frontend or "Web Application"

    backend = backend or "API / Backend"

    database = database or "PostgreSQL"

    lines = [
        "```mermaid",
        "flowchart TD",
        "    U[Users]",
        f"    F[{_safe_mermaid(frontend)}]",
        f"    B[{_safe_mermaid(backend)}]",
        f"    D[{_safe_mermaid(database)}]",
    ]

    lines.extend(
        [
            "    U --> F",
            "    F -->|HTTPS / REST| B",
            "    B --> D",
        ]
    )

    if cache:

        lines.append(
            f"    C[{_safe_mermaid(cache)}]"
        )

        lines.append(
            "    B --> C"
        )

    lines.append(
        "```"
    )

    return "\n".join(lines)


def _safe_mermaid(value: str) -> str:

    return (
        str(value)
        .replace("[", "")
        .replace("]", "")
        .replace("(", "")
        .replace(")", "")
        .replace('"', "'")
    )
