from typing import Any
from uuid import UUID
from node import ClassifierNodeImpl
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from .shapelet_transform_node import ShapeletTransformNode


class DecisionTreeNode(ClassifierNodeImpl):
    def __init__(self, name: str = "DecisionTreeClassifier", id_: UUID = None, **kwargs) -> None:
        self.__set_classifier(**kwargs)
        super().__init__(name, id_, **kwargs)
        
    def __set_classifier(self, **kwargs):
        self.classifier = DecisionTreeClassifier(**kwargs)

    def get_visualize_data(self) -> dict[str, Any]:
        visualize_data = {
            "tree_rules": {
                "criterion": self.classifier.get_params()["criterion"],
                "tree_nodes": self.get_tree_rules(),
            },
            "score": self.scores
        }
        # get shapelets from shapelet transform nodes if any
        if isinstance(self.data, ShapeletTransformNode):
            visualize_data["shapelet_transformation"] = self.data.get_visualize_data()["shapelet_transformation"]
        return visualize_data

    def get_tree_rules(self) -> list[dict]:
        tree = self.classifier.tree_
        # lists of several node data
        n_nodes = tree.node_count
        children_left = tree.children_left
        children_right = tree.children_right
        feature = tree.feature
        values = tree.value
        threshold = tree.threshold
        impurity = tree.impurity
        # additional detail
        node_depth = np.zeros(shape=n_nodes, dtype=int)
        is_leaves = np.zeros(shape=n_nodes, dtype=bool)
        stack = [(0, 0)] # start with node id (0) and its depth (0)
        # stack
        while len(stack) > 0:
            node_id, depth = stack.pop()
            node_depth[node_id] = depth

            is_split_node = children_left[node_id] != children_right[node_id]

            if is_split_node:
                stack.append((children_left[node_id], depth+1))
                stack.append((children_right[node_id], depth+1))
            else:
                is_leaves[node_id] = True
        # json parsable format   
        data = []
        for i in range(n_nodes):
            temp = {
                        "node_id": i,
                        "depth": node_depth[i],
                        "values": values[i],
                        "impurity": impurity[i],
                    }
            if not is_leaves[i]:
                temp["left"] = children_left[i]
                temp["right"] = children_right[i]
                temp["feature"] = feature[i]
                temp["threshold"] = threshold[i]
            data.append(temp)
        return data
