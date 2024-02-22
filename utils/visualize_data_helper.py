import pandas as pd


def get_dataframe_column_types(df: pd.DataFrame) -> list[tuple[str, str]]:
    col_types = []
    for col, type_ in df.dtypes.to_dict().items():
        col_types.append((col, str(type_)))
    return col_types