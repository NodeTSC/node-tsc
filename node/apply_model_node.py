from typing import Any
from node import ApplyNodeImpl
import pandas as pd
from uuid import UUID


class ApplyModelNode(ApplyNodeImpl):
    def _transform(self, x) -> Any:
        return self.model.get_output("model").predict(x)
    
    def get_visualize_data(self) -> dict[str, Any]:
        return super().get_visualize_data()
