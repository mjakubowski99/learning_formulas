import typing as t
import numpy as np
import pandas as pd 
from preprocessing.DataTransformer import DataTransformer

default_multiplier = 100

class DecimalEncoder(DataTransformer):
    def __init__(self, columns, multipliers: dict[t.Any, float]=None):
        if multipliers is None:
            self.multipliers = self.make_default_multipliers(columns)
        else:
            self.multipliers = multipliers
    
    def process(self, df: pd.DataFrame, target=None) -> pd.DataFrame:
        float_columns = df.select_dtypes(include=[np.float64])

        for column in float_columns:
            if target is not None and column == target:
                continue
            
            df[column] = df[column] * self.multipliers[column] 
            df[column] = df[column].round(0).astype(np.int64)

        return df
    
    def setMultiplier(self, column, multiplier: float):
        self.multipliers[column] = multiplier

    def getMultiplier(self, column) -> float:
        return self.multipliers[column]
            
    def make_default_multipliers(self, columns) -> dict[t.Any, float]:
        multipliers = {}

        for column in columns:
            multipliers[column] = default_multiplier

        return multipliers