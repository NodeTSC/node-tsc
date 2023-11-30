from typing import Any
from node import NodeImpl
import pandas as pd
from pyts.transformation import ShapeletTransform


class ShapeletTransformNode(NodeImpl):
    def __init__(self, project_path: str, label: str, **kwargs) -> None:
        super().__init__(project_path, **kwargs)
        
        self.label = label
        self.input_node = None
        self.is_executed = False
        self.model = ShapeletTransform(**kwargs)
        
    def add_input(self, input: Any):
        self.input_node = input
        self.is_executed = False
        
    def execute(self):
        if not self.is_executed and self.input_node is not None:
            # reading data
            data = self.input_node.get_output()
            X_train = data.drop(columns=self.label)
            y_train = data[self.label].astype(int)
            # fitting model
            self.model.fit(X_train, y_train)
            self.is_executed = True
    
    def get_model(self):
        self.execute()
        return self.model
