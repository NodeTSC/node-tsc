from enum import Enum
from node import *


class NodeType(Enum):
    INPUT_NODE = InputNode
    APPLY_MODEL_NODE = ApplyModelNode
    PREP_NODE = PrepNode
    SHAPELET_TRANSFORM_NODE = ShapeletTransform


class NodeFactory():
    @staticmethod
    def create_node(node_type: NodeType, name=None, **kwargs) -> NodeImpl:
        node = node_type.value()
        node.__init__(name, **kwargs)
        return node
