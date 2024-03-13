from typing import Any
from uuid import UUID
from node import NodeImpl, DataInput
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from .shapelet_transform_node import ShapeletTransformNode


class KnnNode(NodeImpl, DataInput):
    def __init__(self, name: str = None, id_: UUID = None, **kwargs) -> None:
        self.classifier = KNeighborsClassifier(**kwargs)
        super().__init__(name, id_, **kwargs)
        self.output["model"] = self.classifier
        self.parameters = self.classifier.get_params()

    def execute(self) -> None:
        if self.data is not None:
            # reading data
            data = self.data.get_output("data")
            target_label = self.data.get_output("meta")["target"]
            x_train = data.drop(columns=target_label)
            y_train = data[target_label]
            # fitting model
            self.classifier.fit(x_train, y_train)
            # transforming training data
            self.output["data"] = self.classifier.predict(x_train)
            # debugging score
            print(f"{self.name} train score: {self.classifier.score(x_train, y_train)}")

    def get_parameters(self) -> list[str]:
        return list(self.classifier.get_params().keys())
    
    def priority(self) -> int:
        try:
            return self.data.priority() + 1
        except:
            return None
        
    def get_visualize_data(self) -> dict[str, Any]:
        return super().get_visualize_data()
