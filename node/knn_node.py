from typing import Any
from uuid import UUID
from node import ClassifierNodeImpl
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pandas as pd
from .shapelet_transform_node import ShapeletTransformNode


class KnnNode(ClassifierNodeImpl):    
    def __init__(self, name: str = "KnnClassifier", id_: UUID = None, **kwargs) -> None:
        self.__set_classifier(**kwargs)
        super().__init__(name, id_, **kwargs)
        
    def __set_classifier(self, **kwargs):
        self.classifier = KNeighborsClassifier(**kwargs)
        
    def get_visualize_data(self) -> dict[str, Any]:
        data: pd.DataFrame = self.data.get_output("data")
        target_label = self.data.get_output("meta")["target"]
        
        predicted_label = self.classifier.predict(data.drop(columns=target_label))
        return {
            "knn": {
                "timeseries": data.drop(columns=target_label).values.tolist(),
                "labels": list(data[target_label]),
                "predicts": predicted_label,
            },
            "scores": self.scores
        }
