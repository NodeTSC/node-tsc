import pandas as pd
import json
import numpy as np


def get_dataframe_column_types(df: pd.DataFrame) -> list[tuple[str, str]]:
    col_types = []
    for col, type_ in df.dtypes.to_dict().items():
        col_types.append((col, str(type_)))
    return col_types


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)