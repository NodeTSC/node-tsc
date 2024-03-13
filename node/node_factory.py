from __future__ import annotations

from enum import Enum
from node import InputNode, PrepNode, ShapeletTransformNode, ApplyModelNode, DecisionTreeNode, KnnNode, NodeImpl
from uuid import UUID


class NodeType(Enum):
    INPUT = "input"
    PREP = "prep"
    SHAPELET_TRANSFORM = "shapelet_transform"
    APPLY = "apply"
    DECISION_TREE = "decision_tree"
    KNN = "knn"


class NodeFactory():
    @staticmethod
    def create_node(node_type: NodeType, name: str = None, id_: UUID = None, **kwargs):
        node: NodeImpl = None
        match node_type:
            case NodeType.INPUT:
                node = InputNode
            case NodeType.PREP:
                node = PrepNode
            case NodeType.SHAPELET_TRANSFORM:
                node = ShapeletTransformNode
            case NodeType.APPLY:
                node = ApplyModelNode
            case NodeType.DECISION_TREE:
                node = DecisionTreeNode
            case NodeType.KNN:
                node = KnnNode
        node = node(name, id_, **kwargs)
        return node
