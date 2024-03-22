from node import NodeImpl, DataInput, ModelInput
import pandas as pd
from uuid import UUID


class ApplyTransformerNode(NodeImpl, DataInput, ModelInput):
    def __init__(self, name: str = "ApplyTransformer", id_: UUID = None, **kwargs) -> None:
        super().__init__(name, id_, **kwargs)
        self.output["data"] = None
        
    def add_data_node(self, data: NodeImpl):
        try:
            self.output["meta"] = data.get_output("meta")
        except:
            pass
        return super().add_data_node(data)
    
    def execute(self) -> None:
        if self.data is not None and self.model is not None:
            model = self.model.get_output("model")
            data = self.data.get_output("data")
            
            # data has target label
            if self.output["meta"]["target"] is not None:
                target = self.output["meta"]["target"]
                
                X = data.drop(columns=target)
                transformed_X = model.transform(X)
            
                self.output["data"] = pd.concat([pd.DataFrame(transformed_X), data[target]], axis=1)
            else:
                pass
        return super().execute()
    
    def priority(self) -> int:
        try:
            return self.data.priority() + self.model.priority() + 1
        except:
            return None
        
    def get_parameters(self) -> list[str]:
        return []