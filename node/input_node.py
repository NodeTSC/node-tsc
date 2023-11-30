from node import NodeImpl
import pandas as pd
from scipy.io import arff


class InputNode(NodeImpl):
    def __init__(self, project_path: str, **kwargs) -> None:
        super().__init__(project_path, **kwargs)
        
        self.source = kwargs.get("source")
        self.source_type:str = kwargs.get("source_type")
        self.is_executed = False
        self.output = None
        
    def execute(self):
        if not self.is_executed:
            match self.source_type.lower():
                case 'arff':
                    self.output = pd.DataFrame(arff.loadarff(self.source)[0])
                case _:
                    raise ValueError(f'"{self.source_type}" is not supported!')
            self.is_executed = True
        
    def get_output(self):
        self.execute()
        return self.output

