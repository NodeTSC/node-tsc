from __future__ import annotations
from typing import Any
from abc import ABC, abstractmethod
from uuid import uuid4


class NodeImpl(ABC):
    def __init__(self, name: str = None, **kwargs) -> None:
        self.id = uuid4()
        self.name = name
        self.parameters: dict = {k: None for k in self.get_parameters()}
        self.set_parameters(**kwargs)
        self.output: Any = None

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
    
    def set_parameters(self, **kwargs):
        for key, val in kwargs.items():
            if key in self.get_parameters():
                self.parameters[key] = val
    
    @abstractmethod
    def get_parameters(self) -> list[str]:
        """Returns list of available keyword attributes."""
        return []


class ModelInput(ABC):
    def __init__(self) -> None:
        self.model = None
        
    def add_model_node(self, model: NodeImpl):
        self.model = model


class DataInput(ABC):
    def __init__(self) -> None:
        self.data = None
        
    def add_data_node(self, data: NodeImpl):
        self.data = data
