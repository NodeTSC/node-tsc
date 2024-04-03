import json
import pandas as pd
import numpy as np


def get_dataframe_column_types(df: pd.DataFrame) -> list[tuple[str, str]]:
    col_types = []
    for col, type_ in df.dtypes.to_dict().items():
        col_types.append((col, str(type_)))
    return col_types


class NpEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        return super(NpEncoder, self).default(o)
