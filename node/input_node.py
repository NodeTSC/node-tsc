from typing import Any
from uuid import UUID
from node import NodeImpl
import pandas as pd
from scipy.io import arff
from utils import get_dataframe_column_types


class InputNode(NodeImpl):
    def __init__(self, name: str = "Input", id_: UUID = None, **kwargs) -> None:
        super().__init__(name, id_, **kwargs)
        self.output["data"] = None
        
    def execute(self):
        match self.parameters["source_type"].lower():
            case 'arff':
                self.output["data"] = pd.DataFrame(arff.loadarff(self.parameters["source"])[0])
            case _:
                raise ValueError(f'"{self.source_type}" is not supported!')
            
    def priority(self) -> int:
        return 0

    def get_parameters(self) -> list[str]:
        return ["source", "source_type"]

    def get_visualize_data(self) -> dict[str, Any]:
        # For convenience, unprepared data types will be cast into strings.
        df: pd.DataFrame = self.get_output("data")
        return {
            "data": {
                "data": df.astype(str).values.tolist(),
                "col_type": get_dataframe_column_types(df)
            }
        }