from __future__ import annotations

from enum import Enum
from node import NodeImpl, ModelInput, DataInput
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
    
    def update_node(self, node: NodeImpl, name: str = None, **kwargs):
        if name is not None:
            node.name = name
        node.set_parameters(**kwargs)
    
    def add_edge(self, source: UUID, dest: UUID, port: EdgePortType):
        source = self.get_node_by_id(source)
        dest = self.get_node_by_id(dest)
        match port:
            case EdgePortType.DATA:
                if isinstance(dest, DataInput):
                    dest.add_data_node(source)
            case EdgePortType.MODEL:
                if isinstance(dest, ModelInput):
                    dest.add_model_node(source)
        self.edges.append(EdgeInfo(source, dest, port))
    
    def delete_edge(self, source: UUID, dest: UUID, port: EdgePortType):
        del_index = None
        for index, edge in enumerate(self.edges):
            if edge == EdgeInfo(source, dest, port):
                del_index = index
        if del_index is None:
            raise ValueError("Edge not found...")
        self.edges.pop(del_index)
        source = self.get_node_by_id(source)
        dest = self.get_node_by_id(dest)
        match port:
            case EdgePortType.DATA:
                if isinstance(dest, DataInput) and dest.data == source:
                    dest.data = None
            case EdgePortType.MODEL:
                if isinstance(dest, ModelInput) and dest.model == source:
                    dest.model = None
                    
    def get_node_by_id(self, uuid: UUID) -> NodeImpl:
        for node in self.nodes:
            if node.id == uuid:
                return node
        return None

    def save(self):
        # TODO: save neccessary things into json/ymal or else
        pass
    
    def load(self):
        # TODO: must satisfy the following steps
        # 1. recreate all nodes with their attributes
        # 2. reconnect all nodes using edges
        pass
    
    def execute(self):
        for e in sorted(self.nodes):
            print(f"priority {e.priority()} executing {e.name}... ({e.__class__})")
            e.execute() 


class EdgeInfo():
    def __init__(self, source: UUID, dest: UUID, port: EdgePortType) -> None:
        self.source = source
        self.dest = dest
        self.port = port
        
    def __eq__(self, other: EdgeInfo) -> bool:
        return self.source == other.source and self.dest == other.dest and self.port == other.port
        

class EdgePortType(Enum):
    MODEL = "model"
    DATA = "data"
