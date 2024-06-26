from __future__ import annotations

from enum import Enum
from uuid import UUID
import json
import pickle
import logging
from copy import deepcopy
from tqdm import tqdm
from node import NodeImpl, ModelInput, DataInput


class ProjectManager():
    def __init__(self) -> None:
        self.nodes: list[NodeImpl] = []
        self.edges: list[Edge] = []

    def add_node(self, node: NodeImpl) -> None:
        self.nodes.append(node)

    def delete_node(self, node: NodeImpl) -> None:
        for other_node in self.nodes:
            # skip self
            if other_node.id == node.id:
                continue
            # cascade remove
            if isinstance(other_node, DataInput):
                if other_node.data.id == node.id:
                    self.delete_edge(node.id, other_node.id, EdgePortType.DATA)
            if isinstance(other_node, ModelInput):
                if other_node.model.id == node.id:
                    self.delete_edge(node.id, other_node.id, EdgePortType.MODEL)
        self.nodes.remove(node)

    def update_node(self, node: NodeImpl, name: str = None, **kwargs):
        if name is not None:
            node.name = name
        node.set_parameters(**kwargs)

    def add_edge(self, source: UUID, dest: UUID, port: EdgePortType):
        source: NodeImpl = self.get_node_by_id(source)
        dest: NodeImpl = self.get_node_by_id(dest)
        match port:
            case EdgePortType.DATA:
                if isinstance(dest, DataInput):
                    dest.add_data_node(source)
            case EdgePortType.MODEL:
                if isinstance(dest, ModelInput):
                    dest.add_model_node(source)
        self.edges.append(Edge(source.id, dest.id, port))
        # label transfering
        dest.set_meta(deepcopy(source.get_output("meta")))
        logging.info(f'Add edge => {source}-{dest} type: {port.name}')

    def delete_edge(self, source: UUID, dest: UUID, port: EdgePortType):
        del_index = None
        for index, edge in enumerate(self.edges):
            if edge == Edge(source, dest, port):
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
        logging.info(f'Delete edge => {source}-{dest} type: {port.name}')

    def get_node_by_id(self, uuid: UUID) -> NodeImpl:
        for node in self.nodes:
            if node.id == uuid:
                return node
        return None

    def save(self, fname: str):
        with open(fname, "wb") as f:
            pickle.dump(
                {"nodes": self.nodes, "edges": self.edges},
                file=f
            )

    def load(self, fname: str):
        with open(fname, "rb") as f:
            obj = pickle.load(f)
            self.reset()
            self.nodes = obj["nodes"]
            self.edges = obj["edges"]

    def reset(self):
        self.nodes = []
        self.edges = []

    def execute(self):
        executable_node = []
        for node in self.nodes:
            if node.priority() is None:
                print(f"skip {node.name}...")
            else:
                executable_node.append(node)
        executable_node.sort()
        for e in tqdm(executable_node, desc="execute nodes"):
            print(f"priority {e.priority()} executing {e.name}... ({e.__class__})")
            e.execute()

    def json(self):
        return json.dumps({
            "nodes": [node.info() for node in self.nodes],
            "edges": [edge.info() for edge in self.edges]
        })


class Edge():
    def __init__(self, source: UUID, dest: UUID, port: EdgePortType) -> None:
        self.source = source
        self.dest = dest
        self.port = port

    def __eq__(self, other: Edge) -> bool:
        return self.source == other.source and self.dest == other.dest and self.port == other.port

    def info(self):
        return {
            "source": str(self.source),
            "dest": str(self.dest),
            "port": self.port.name
        }


class EdgePortType(Enum):
    MODEL = "model"
    DATA = "data"
