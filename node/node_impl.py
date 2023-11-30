from abc import ABC, abstractmethod
from uuid import uuid4


class NodeImpl(ABC):
    def __init__(self, project_path: str, **kwargs) -> None:
        self.id = uuid4()
        self.project_path = project_path
        self.parameters = kwargs
