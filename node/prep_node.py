from typing import Any
from uuid import UUID
from node import NodeImpl, DataInput
import pandas as pd
from utils import get_dataframe_column_types


class PrepNode(NodeImpl, DataInput):
    def __init__(self, name: str = "Prep", id_: UUID = None, **kwargs) -> None:
        super().__init__(name, id_, **kwargs)
        if self.parameters["instructions"] is None:
            self.parameters["instructions"] = []
        self.output["data"] = None
        
    def execute(self):
        self.output["data"] = self.data.get_output("data")
        for i in self.parameters["instructions"]:
            command, column, to = i
            match command:
                case "set_role":
                    self.set_role(column, to)
                case "change_type":
                    match to:
                        case "int":
                            self.change_type(column, int)
                        case "float":
                            self.change_type(column, float)
                    
    def priority(self) -> int:
        try:
            return self.data.priority() + 1
        except:
            return None
    
    def get_parameters(self) -> list[str]:
        return ["instructions"]
    
    def set_role(self, column: str, role: str):
        self.output["meta"][role] = column
    
    def change_type(self, column: str, as_type: any):
        self.output["data"][column] = self.output["data"][column].astype(as_type)

    def get_visualize_data(self) -> dict[str, Any]:
        df: pd.DataFrame = self.get_output("data")
        try:
            target = self.get_output("meta")["target"]
            dist = df.groupby(df[target])[target].count().to_dict()
            labels = df[target].to_list()
            df = df.drop(columns=target)
        except:
            target = None
        viz = {
            "data": {
                "data": df.values.tolist(),
                "col_type": get_dataframe_column_types(df)
            },
            "meta": self.output["meta"]
        }
        if target is not None:
            viz["label_distribution"] = dist
            viz["data"]["labels"] = labels
        return viz
