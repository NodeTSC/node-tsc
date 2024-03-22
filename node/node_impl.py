from __future__ import annotations
from typing import Any
from abc import ABC, abstractmethod
from uuid import uuid4, UUID
import pandas as pd
from sklearn.base import *
from sklearn.metrics import confusion_matrix, classification_report
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


class ClassifierNodeImpl(NodeImpl, DataInput):
    
    classifier: ClassifierImpl
    
    def __init__(self, name: str = None, id_: UUID = None, **kwargs) -> None:
        self.__set_classifier(**kwargs)
        super().__init__(name, id_, **kwargs)
        self.output["model"] = self.classifier
        self.parameters = self.classifier.get_params()        
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
            self.scores = self.get_report()
            
    def priority(self) -> int:
        try:
            return self.data.priority() + 1
        except:
            return None
    
    def get_report(self, scores=True, confusion=True):
        report = {}
        data: pd.DataFrame = self.data.get_output("data")
        target_label = self.data.get_output("meta")["target"]
        x = data.drop(columns=target_label)
        y = data[target_label]
        y_pred = self.classifier.predict(x)
        
        if scores:
            report["report"] = classification_report(y, y_pred, output_dict=True)
        if confusion:
            report["confusion_matrix"] = {
                "heatmap": confusion_matrix(y, y_pred).tolist(),
                "labels": sorted(y.unique().tolist())
            }
        
        return report
        
    def get_parameters(self) -> list[str]:
        return list(self.classifier.get_params().keys())
 
 
class ApplyNodeImpl(NodeImpl, DataInput, ModelInput):
     
    def __init__(self, name: str = None, id_: UUID = None, **kwargs) -> None:
         super().__init__(name, id_, **kwargs)
         
    def add_data_node(self, data: NodeImpl):
        # get meta data from input data node
        try:
            self.output["meta"] = data.get_output("meta")
        except:
            pass
        return super().add_data_node(data)
    
    def execute(self) -> None:
        if self.data is not None and self.model is not None:
            model = self.model.get_output("model")
            data: pd.DataFrame = self.data.get_output("data")
            
            if self.output["meta"]["target"] is not None:
                target = self.output["meta"]["target"]
                
                x = data.drop(columns=target)
                transformed_x = self._transform(x)
                
                self.output["data"] = pd.concat([
                    pd.DataFrame(transformed_x),
                    data[target]
                ], axis=1)
            else:
                raise ValueError("Target label is not specified in input data node.")
    
    @abstractmethod
    def _transform(self, x) -> Any:
        pass
    
    def priority(self) -> int:
        try:
            return self.data.priority() + self.model.priority() + 1
        except:
            return None
    
    def get_parameters(self) -> list[str]:
        return []
