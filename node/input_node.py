from node import NodeImpl
import pandas as pd
from scipy.io import arff


class InputNode(NodeImpl):
    def __init__(self, project_path: str, **kwargs) -> None:
        super().__init__(project_path, **kwargs)
        
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
