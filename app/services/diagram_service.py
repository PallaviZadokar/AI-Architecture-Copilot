from graphviz import Digraph
from pathlib import Path


def generate_architecture_diagram(
    architecture: dict,
    output_path: str
) -> str:

    Path(output_path).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    dot = Digraph(
        "Architecture",
        format="png"
    )

    dot.attr(
        rankdir="LR",
        bgcolor="white"
    )

    dot.attr(
        "node",
        shape="box",
        style="rounded,filled",
        fontname="Arial",
        fontsize="11",
        margin="0.2"
    )

    components = architecture.get(
        "components",
        []
    )

    component_nodes = {}

    for index, component in enumerate(components):

        name = component.get(
            "component",
            f"Component {index}"
        )

        technology = component.get(
            "technology",
            ""
        )

        node_id = f"component_{index}"

        component_nodes[name] = node_id

        dot.node(
            node_id,
            f"{name}\n{technology}",
            fillcolor="#E8F1FF"
        )

    # Connect components sequentially for a simple HLD view.
    for i in range(len(components) - 1):

        current = components[i].get(
            "component"
        )

        next_component = components[i + 1].get(
            "component"
        )

        if current in component_nodes and next_component in component_nodes:

            dot.edge(
                component_nodes[current],
                component_nodes[next_component]
            )

    output = dot.render(
        output_path,
        cleanup=True
    )

    return output
