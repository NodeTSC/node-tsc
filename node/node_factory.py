from __future__ import annotations

from enum import Enum
from node import InputNode, PrepNode, ShapeletTransformNode, ApplyModelNode, DecisionTreeNode, NodeImpl
from uuid import UUID


class NodeType(Enum):
    INPUT = "input"
    PREP = "prep"
    SHAPELET_TRAINSFORM = "shapelet_transform"
    APPLY = "apply"
    DECISION_TREE = "decision_tree"


class NodeFactory(Enum):
    @staticmethod
    def create_node(node_type: NodeType, name: str = None, id_: UUID = None, **kwargs):
        node: NodeImpl = None
        match node_type:
            case NodeType.INPUT:
                node = InputNode
            case NodeType.PREP:
                node = PrepNode
            case NodeType.SHAPELET_TRAINSFORM:
                node = ShapeletTransformNode
            case NodeType.APPLY:
                node = ApplyModelNode
            case NodeType.DECISION_TREE:
                node = DecisionTreeNode
        node = node(name, id_, **kwargs)
        return node
