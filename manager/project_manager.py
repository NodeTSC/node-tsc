from __future__ import annotations

from node import NodeImpl
from utils import NodeFactory, NodeType
from uuid import UUID


class ProjectManager():
    def __init__(self) -> None:
        self.nodes: list[NodeImpl] = []
        self.edges: list[EdgeInfo] = []
        
    def add_node(self, node: NodeImpl) -> None:
        self.nodes.append(node)
    
    def delete_node(self, node: NodeImpl) -> None:
        self.nodes.remove(node)
    
    def update_node(self, node: NodeImpl, name: str, **kwargs):
        pass
    
    def add_edge(self, edge: EdgeInfo):
        pass
    
    def delete_edge(self, edge: EdgeInfo):
        # TODO: reverse connection
        # 1. change destination's input to None based on its type
        pass

    def save(self):
        # TODO: save neccessary things into json/ymal or else
        pass
    
    def load(self):
        # TODO: must satisfy the following steps
        # 1. recreate all nodes with their attributes
        # 2. reconnect all nodes using edges
        pass


class EdgeInfo():
    def __init__(self, source: NodeImpl, dest: NodeImpl, port: str) -> None:
        self.source = source
        self.dest = dest
        self.port = port
