from abc import ABC, abstractmethod
from uuid import uuid4


class NodeImpl(ABC):
    def __init__(self, project_path: str, **kwargs) -> None:
        self.id = uuid4()
        self.project_path = project_path
        self.parameters = kwargs
        self.output: str = None

    def get_output(self, key):
        return self.output[key]
    
    @abstractmethod
    def execute(self):
        pass


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
