from __future__ import annotations

import networkx as nx
from node import NodeImpl


def visualize_node_graph(nodes: list[NodeImpl]) -> None:
    g = nx.DiGraph(directed=True)
    color_map = []

    for node in nodes:
        p = node.priority()
        if p is not None:
            g.add_node(
                node.id,
                name=f"{node.name}\n(priority: {p})"
            )
            color_map.append("blue")
        else:
            g.add_node(
                node.id,
                name=f"{node.name}\n(invalid input)"
            )
            color_map.append("red")
    
    for node in nodes:
        if hasattr(node, 'data') and node.data is not None:
            g.add_edge(node.data.id, node.id, label="data")
        if hasattr(node, 'model') and node.model is not None:
            g.add_edge(node.model.id, node.id, label="model")

    # draw graph
    pos = nx.spring_layout(g)
    nx.draw_networkx_nodes(g, pos, alpha=0.5, node_shape='s', node_color=color_map)
    nx.draw_networkx_labels(g, pos, font_size=10, labels=nx.get_node_attributes(g, "name"))
    nx.draw_networkx_edges(g, pos)
    nx.draw_networkx_edge_labels(
        g, pos, edge_labels=nx.get_edge_attributes(g, 'label')
    )
