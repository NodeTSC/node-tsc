from typing import Any
from node import ApplyNodeImpl


class ApplyTransformerNode(ApplyNodeImpl):
    def _transform(self, x) -> Any:
        return self.model.get_output("model").transform(x)
    
    def get_visualize_data(self) -> dict[str, Any]:
        target = self.data.get_output("meta")["target"]
        data = self.model.get_visualize_data()
        # transformed data
        data["transformed_data"]["timeseries_labels"] = self.output["data"][target].values.tolist()
        data["transformed_data"]["transformed_data"] = self.output["data"].drop(columns=target).values.tolist()
        # transformer info
        data["transformer"] = self.model.info()
        return data
