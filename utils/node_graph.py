from __future__ import annotations

import networkx as nx
from node import NodeImpl


def visualize_node_graph(nodes: list[NodeImpl]) -> None:
    g = nx.DiGraph(directed=True)

    for node in nodes:
        g.add_node(
            node.id,
            name=f"{node.name}\n(priority: {node.priority()})"
        )
    
    for node in nodes:
        if hasattr(node, 'data'):
            g.add_edge(node.data.id, node.id, label="data")
        if hasattr(node, 'model'):
            g.add_edge(node.model.id, node.id, label="model")

    # draw graph
    pos = nx.spring_layout(g)
    nx.draw_networkx_nodes(g, pos, alpha=0.5, node_shape='s')
    nx.draw_networkx_labels(g, pos, font_size=10, labels=nx.get_node_attributes(g, "name"))
    nx.draw_networkx_edges(g, pos)
    nx.draw_networkx_edge_labels(
        g, pos, edge_labels=nx.get_edge_attributes(g, 'label')
    )
