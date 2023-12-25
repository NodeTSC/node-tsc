from node import NodeImpl
import pandas as pd
from scipy.io import arff


class InputNode(NodeImpl):
    def __init__(self, name: str = None, **kwargs) -> None:
        super().__init__(name, **kwargs)
        if name is None:
            self.name = "Input"
        self.source = kwargs.get("source")
        self.source_type:str = kwargs.get("source_type")
        self.output = {
            "data": None
        }
        
    def execute(self):
        match self.source_type.lower():
            case 'arff':
                self.output["data"] = pd.DataFrame(arff.loadarff(self.source)[0])
            case _:
                raise ValueError(f'"{self.source_type}" is not supported!')
            
    def priority(self) -> int:
        return 0
