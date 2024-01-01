from __future__ import annotations

from enum import Enum
from node import InputNode, PrepNode, ShapeletTransformNode, ApplyModelNode, NodeImpl


class NodeType(Enum):
    INPUT = "input"
    PREP = "prep"
    SHAPELET_TRAINSFORM = "shapelet_transform"
    APPLY = "apply"


class NodeFactory(Enum):
    @staticmethod
    def create_node(node_type: NodeType, name: str = None, **kwargs):
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
        node = node(name=name, **kwargs)
        return node
