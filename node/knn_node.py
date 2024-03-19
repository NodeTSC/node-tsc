from typing import Any
from uuid import UUID
from node import ClassifierNode
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from .shapelet_transform_node import ShapeletTransformNode


class KnnNode(ClassifierNode):    
    def __init__(self, name: str = "KnnClassifier", id_: UUID = None, **kwargs) -> None:
        self.__set_classifier(**kwargs)
        super().__init__(name, id_, **kwargs)
        
    def __set_classifier(self, **kwargs):
        self.classifier = KNeighborsClassifier(**kwargs)
        
    def get_visualize_data(self) -> dict[str, Any]:
        return {
            "scores": self.scores
        }
