from typing import Any
from node import NodeImpl, DataInput
from pyts.transformation import ShapeletTransform


class ShapeletTransformNode(NodeImpl, DataInput):
    def __init__(self, project_path: str, **kwargs) -> None:
        super().__init__(project_path, **kwargs)
        
        self.output = {
            "model": ShapeletTransform(**kwargs)
        }
        
    def execute(self):
        if self.data is not None:
            # reading data
            data = self.data.get_output("data")
            # dropping columns that is not time series data
            target_label = self.data.get_output("label")["target"]
            X_train = data.drop(columns=target_label)
            y_train = data[target_label].astype(int)
            # fitting model
            self.output["model"].fit(X_train, y_train)
            self.is_executed = True
