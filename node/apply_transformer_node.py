from typing import Any
from node import ApplyNodeImpl


class ApplyTransformerNode(ApplyNodeImpl):
    def _transform(self, x) -> Any:
        return self.model.get_output("model").transform(x)
    
    def get_visualize_data(self) -> dict[str, Any]:
        return super().get_visualize_data()
