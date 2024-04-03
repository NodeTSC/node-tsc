from typing import Any
from uuid import UUID
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from node import ClassifierNodeImpl


class KnnNode(ClassifierNodeImpl):
    def __init__(self, name: str = "KnnClassifier", id_: UUID = None, **kwargs) -> None:
        self.__set_classifier(**kwargs)
        super().__init__(name, id_, **kwargs)

    def __set_classifier(self, **kwargs):
        self.classifier = KNeighborsClassifier(**kwargs)

    def get_visualize_data(self) -> dict[str, Any]:
        data: pd.DataFrame = self.data.get_output("data")
        target_label = self.data.get_output("meta")["target"]

        return {
            # fit data
            "knn": {
                "timeseries": data.drop(columns=target_label).values.tolist(),
                "labels": list(data[target_label]),
                "predicts": self.output["data"],
            },
            # predict data
            "timeseries": data.drop(columns=target_label).values.tolist(),
            "score": self.scores,
            "predicted_labels": list(data[target_label]),
            "actual_labels": self.output["data"],
        }
