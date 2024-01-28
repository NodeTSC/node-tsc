from uuid import UUID
from node import NodeImpl, DataInput
from node.node_impl import NodeImpl


class DecisionTreeNode(NodeImpl, DataInput):
    def __init__(self, name: str = None, id_: UUID = None, **kwargs) -> None:
        super().__init__(name, id_, **kwargs)

    def add_data_node(self, data: NodeImpl):
        # TODO: implement this
        return super().add_data_node(data)
    
    def execute(self) -> None:
        # TODO: implement this
        return super().execute()
    
    def priority(self) -> int:
        try:
            return self.data.priority() + 1
        except:
            return None
    
    def get_parameters(self) -> list[str]:
        # TODO: implement this
        return super().get_parameters()
