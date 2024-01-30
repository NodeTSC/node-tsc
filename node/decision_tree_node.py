from uuid import UUID
from node import NodeImpl, DataInput
from node.node_impl import NodeImpl
from sklearn.tree import DecisionTreeClassifier
import pandas as pd


class DecisionTreeNode(NodeImpl, DataInput):
    def __init__(self, name: str = "DecisionTreeClassifier", id_: UUID = None, **kwargs) -> None:
        self.classifier = DecisionTreeClassifier(**kwargs)
        super().__init__(name, id_, **kwargs)
        self.output["model"] = self.classifier
        self.parameters = self.classifier.get_params()
    
    def execute(self) -> None:
        if self.data is not None:
            # reading data
            data = self.data.get_output("data")
            # dropping columns that is not time series data
            target_label = self.data.get_output("label")["target"]
            X_train = data.drop(columns=target_label)
            y_train = data[target_label]
            # fitting model
            self.classifier.fit(X_train, y_train)
            # transforming training data
            self.output["predict"] = self.classifier.predict(X_train)
            # debugging score
            print(f"{self.name} train score: {self.classifier.score(X_train, y_train)}")
    
    def priority(self) -> int:
        try:
            return self.data.priority() + 1
        except:
            return None
    
    def get_parameters(self) -> list[str]:
        return list(self.classifier.get_params().keys())
