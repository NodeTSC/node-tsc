from __future__ import annotations
from typing import Any
from abc import ABC, abstractmethod
from uuid import uuid4, UUID
import pandas as pd
from sklearn.base import *
import logging


class NodeImpl(ABC):
    def __init__(self, name: str = None, id_: UUID = None, **kwargs) -> None:
        self.id = uuid4() if id_ is None else id_
        self.name = name
        self.parameters: dict = {k: None for k in self.get_parameters()}
        self.set_parameters(**kwargs)
        self.output: dict[str, Any] = {
            "meta": {
                "target": None,
                "exclude": [],
            }
        }

    def get_output(self, key):
        return self.output[key]
    
    @abstractmethod
    def execute(self) -> None:
        pass
    
    @abstractmethod
    def priority(self) -> int:
        pass
    
    def __lt__(self, other: NodeImpl):
        return self.priority() < other.priority()
    
    def __str__(self) -> str:
        return f'<<{self.__class__.__name__}, name: {self.name}>>'
    
    def set_parameters(self, **kwargs):
        for key, val in kwargs.items():
            if key in self.get_parameters():
                self.parameters[key] = val
    
    @abstractmethod
    def get_parameters(self) -> list[str]:
        """Returns list of available keyword attributes."""
        return []
    
    def set_id(self, uuid: UUID):
        self.id = uuid
    
    def set_meta(self, meta_dict: dict[str, Any]):
        self.output["meta"] = meta_dict    
    
    def info(self):
        return {"name": self.name, "id": str(self.id), "kwargs": self.parameters, "type": self.__class__.__name__}
        
    def get_visualize_data(self) -> dict[str, Any]:
        return {}


class ModelInput(ABC):
    def __init__(self) -> None:
        self.model: NodeImpl = None
        
    def add_model_node(self, model: NodeImpl):
        self.model = model


class DataInput(ABC):
    def __init__(self) -> None:
        self.data: NodeImpl = None
        
    def add_data_node(self, data: NodeImpl):
        self.data = data


class ClassifierImpl(ClassifierMixin, BaseEstimator, TransformerMixin):
    
    def fit(self, *args, **kwargs):
        pass

    def predict(self, *args, **kwargs):
        pass


class ClassifierNode(NodeImpl, DataInput):
    
    classifier: ClassifierImpl
    
    def __init__(self, name: str = None, id_: UUID = None, **kwargs) -> None:
        self.__set_classifier(**kwargs)
        super().__init__(name, id_, **kwargs)
        self.output["model"] = self.classifier
        self.parameters = self.classifier.get_params()
        
        # TODO: add confusion matrix in scores
        self.scores = {}
    
    def __set_classifier(self, **kwargs):
        pass
    
    def execute(self) -> None:
        if self.data is not None:
            # reading data
            data: pd.DataFrame = self.data.get_output("data")
            # dropping columns that is not time series elements
            target_label = self.data.get_output("meta")["target"]
            x_train = data.drop(columns=target_label)
            y_train = data[target_label]
            # fitting model
            self.classifier.fit(x_train, y_train)
            # transforming training data
            self.output["data"] = self.classifier.predict(x_train)
            # logging
            logging.info(f'f"{self.name} train score: {self.classifier.score(x_train, y_train)}')
            # update scores
            self.scores["accuracy"] = self.classifier.score(x_train, y_train)
            # TODO: add more score, such as, f1 and confusion matrix
            
    def priority(self) -> int:
        try:
            return self.data.priority() + 1
        except:
            return None
        
    def get_parameters(self) -> list[str]:
        return list(self.classifier.get_params().keys())
 