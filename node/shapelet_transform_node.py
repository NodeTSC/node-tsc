from typing import Any
from uuid import UUID
from node import NodeImpl, DataInput
from pyts.transformation import ShapeletTransform
import pandas as pd
import numpy as np


class ShapeletTransformNode(NodeImpl, DataInput):
    def __init__(self, name: str = "ShapeletTransform", id_: UUID = None, **kwargs) -> None:
        self.st = ShapeletTransform(**kwargs)
        super().__init__(name, id_, **kwargs)
        self.output["model"] = self.st
        self.parameters = self.st.get_params()

    def execute(self):
        if self.data is not None:
            # reading data
            data = self.data.get_output("data")
            # dropping columns that is not time series data
            target_label = self.data.get_output("meta")["target"]
            X_train = data.drop(columns=target_label)
            y_train = data[target_label]
            # fitting model
            self.st.fit(X_train, y_train)
            # transforming training data
            self.output["data"] = pd.DataFrame(
                self.st.transform(X_train),
                columns=[f"shapelet_{i}" for i in range(len(self.st.shapelets_))]
            )
            self.output["data"][target_label] = y_train
            
    def priority(self) -> int:
        try:
            return self.data.priority() + 1
        except:
            return None
    
    def set_parameters(self, **kwargs):
        super().set_parameters(**kwargs)
        self.st.set_params(**kwargs)

    def get_parameters(self) -> list[str]:
        parameters = list(self.st.get_params().keys())
        return parameters
    
    def get_visualize_data(self):
        shapelets = self.st.shapelets_.tolist()
        # solve unequal length conversion to list
        for idx, s in enumerate(shapelets):
            if isinstance(s, np.ndarray):
                shapelets[idx] = s.tolist()
        indices = self.st.indices_
        df = self.data.get_output("data")
        drop_cols = self.get_output("meta")["target"]
        return {
            # fit data
            "shapelet_transformation": {
                "shapelets": shapelets,
                "labels": list(df.loc[self.st.indices_[:, 0], self.data.get_output("meta")["target"]]),
                "scores": self.st.scores_.tolist(),
                "criterion": self.st.criterion,
                "indices": indices.tolist(),
                "timeseries": df.drop(columns=drop_cols).loc[indices[:, 0]].values.tolist(),
            },
            # transformed data
            "transformed_data": {
                "timeseries_labels": df[self.data.get_output("meta")["target"]].values.tolist(),
                "transformed_data": self.st.transform(df.drop(columns=drop_cols)).tolist(),
            }
        }
