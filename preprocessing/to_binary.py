import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelBinarizer

def standardize_value(x, min_val, max_val, new_min=0, new_max=5):
    return round((x - min_val) * (new_max - new_min) / (max_val - min_val) + new_min)
    
def to_binary(df, target=None):
    for column in df.columns:
        if target is not None and column == target:
            continue
        df[column] = df[column].apply(standardize_value, min_val=df[column].min(), max_val=df[column].max())
        print("Standarization applied for column: "+column)

    return df 


