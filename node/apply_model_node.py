from typing import Any
from node import ApplyNodeImpl
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report


class ApplyModelNode(ApplyNodeImpl):
    def _transform(self, x) -> Any:
        return self.model.get_output("model").predict(x)
    
    def get_visualize_data(self) -> dict[str, Any]:
        model = self.model.get_output("model")
        target_label = self.data.get_output("meta")["target"]
        x = self.data.get_output("data").drop(columns=target_label)
        
        data = self.model.get_visualize_data()
        # predicted data
        data["timeseries"] = x.values.tolist()
        data["score"] = self.get_report()
        data["predicted_labels"] = model.predict(x)
        data["actual_labels"] = self.data.get_output("data")[target_label].values.tolist()
        # classifier info
        data["model"] = self.model.info()
        return data

    def get_report(self, scores=True, confusion=True):
        report = {}
        model = self.model.get_output("model")
        data: pd.DataFrame = self.data.get_output("data")
        target_label = self.data.get_output("meta")["target"]
        x = data.drop(columns=target_label)
        y = data[target_label]
        y_pred = model.predict(x)        
        if scores:
            report["report"] = classification_report(y, y_pred, output_dict=True)
        if confusion:
            report["confusion_matrix"] = {
                "heatmap": confusion_matrix(y, y_pred).tolist(),
                "labels": sorted(y.unique().tolist())
            }
        return report
