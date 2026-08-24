def build_architecture_graph(
    architecture: dict,
) -> str:

    components = architecture.get(
        "components",
        [],
    )

    lines = [
        "digraph Architecture {",
        'rankdir=LR;',
        'bgcolor="white";',
        'node [shape=box, style="rounded,filled", '
        'fontname="Arial", fontsize=11, '
        'color="#334155", fillcolor="#EFF6FF"];',
        'edge [color="#64748B", arrowsize=0.8];',
    ]

    component_ids = []

    for index, component in enumerate(
        components
    ):

        node_id = f"component_{index}"

        component_ids.append(node_id)

        name = component.get(
            "name",
            f"Component {index + 1}",
        )

        technology = component.get(
            "technology",
            "",
        )

        label = (
            f"{name}\\n"
            f"{technology}"
        )

        safe_label = (
            label
            .replace('"', '\\"')
            .replace("\n", "\\n")
        )

        lines.append(
            f'{node_id} [label="{safe_label}"];'
        )

    for index in range(
        len(component_ids) - 1
    ):

        lines.append(
            f"{component_ids[index]} -> "
            f"{component_ids[index + 1]};"
        )

    lines.append("}")

    return "\n".join(lines)
