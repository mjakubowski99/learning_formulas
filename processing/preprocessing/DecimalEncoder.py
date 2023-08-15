import typing as t
import numpy as np
import pandas as pd 
from processing.preprocessing.DataTransformer import DataTransformer

default_multiplier = 100

class DecimalEncoder(DataTransformer):

    def default(self, df):
        return self.make_default_multipliers(df.columns)
    
    def process(self, df: pd.DataFrame, target, multipliers: dict[t.Any, float]) -> pd.DataFrame:
        float_columns = df.select_dtypes(include=[np.float64])

        for column in float_columns:
            if target is not None and column == target:
                continue
            
            df[column] = df[column] * multipliers[column] 
            df[column] = df[column].round(0).astype(np.int64)

        return df
            
    def make_default_multipliers(self, columns) -> dict[t.Any, float]:
        multipliers = {}

        for column in columns:
            multipliers[column] = default_multiplier

        return multipliers