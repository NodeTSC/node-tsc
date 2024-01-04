from node import NodeImpl, DataInput, ModelInput
from node.node_impl import NodeImpl
import pandas as pd
from uuid import UUID


class ApplyModelNode(NodeImpl, DataInput, ModelInput):
    def __init__(self, name: str = "ApplyModel", id_: UUID = None, **kwargs) -> None:
        super().__init__(name, id_, **kwargs)
        self.output = {
            "data": None
        }

    def add_data_node(self, data: NodeImpl):
        try:
            self.output["label"] = data.get_output("label")
        except:
            pass
        return super().add_data_node(data)

    def execute(self):
        if self.data is not None and self.model is not None:
            model = self.model.get_output("model")
            data = self.data.get_output("data")
            
            # data has target label
            if "target" in self.output["label"]:
                target = self.output["label"]["target"]
                
                X = data.drop(columns=target)
                transformed_X = model.transform(X)
                
                self.output["data"] = pd.concat([pd.DataFrame(transformed_X), data[target]], axis=1)
            else:
                self.output["data"] = model.transform(data)
                
    def priority(self) -> int:
        try:
            return self.data.priority() + self.model.priority() + 1
        except:
            return None

    def get_parameters(self) -> list[str]:
        return []