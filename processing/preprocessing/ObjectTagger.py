import typing as t
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from processing.preprocessing.DataTransformer import DataTransformer

default_max_unique = 20

class ObjectTagger(DataTransformer):

    def default(self, df):
        return self.__make_default_max_unique(df.columns)

    def process(self, df: pd.DataFrame, target=None, max_unique_counts: dict[t.Any, int]=None, encode_only=True) -> pd.DataFrame:
        self.taggers = {}

        for column in df.columns:
            if encode_only and column == target:
                continue
            
            if df[column].dtype.kind in 'biufc':
                continue

            if not encode_only and df[column].nunique() > max_unique_counts[column] and column != target:
                df = df.drop(columns=[column])
                continue

            self.taggers[column] = LabelEncoder() 
            df[column] = self.taggers[column].fit_transform(df[column])

        return df

    def __make_default_max_unique(self, columns) -> dict[t.Any, int]:
        max_unique_counts = {}
        
        for column in columns:
            max_unique_counts[column] = default_max_unique

        return max_unique_counts