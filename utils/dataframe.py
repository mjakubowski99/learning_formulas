import pandas as pd 

def target_to_begin(df: pd.DataFrame, target):
    if target not in df.columns:
        return

    data = df[target]
    df=df.drop(columns=[target])
    df.insert(0, target, data)
    return df

def insert_column_at(df: pd.DataFrame, index: int, column_name: str, data: list):
    if column_name in df.columns:
        return df
    df.insert(index, column_name, data)
    return df