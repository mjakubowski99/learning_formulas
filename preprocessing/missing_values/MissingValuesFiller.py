from preprocessing.missing_values.Treshold import Treshold
from preprocessing.DataTransformer import DataTransformer
import pandas as pd 
import typing as t 

fill_na_default_treshold = 0.1
drop_na_default_treshold = 0.4

class MissingValuesFiller(DataTransformer):

    def default(self, df):
        return self.make_default_tresholds(df.columns) 
    
    def process(self, df: pd.DataFrame, target, tresholds: dict[t.Any, Treshold]) -> pd.DataFrame:
        rows_count = len(df)

        for column in df.columns:
            missing = df[column].isnull().sum()/rows_count
            if missing == 0:
                continue

            fill_na_treshold = tresholds[column].fill_na_treshold
            drop_na_treshold = tresholds[column].drop_na_treshold 

            missing = df[column].isnull().sum()/rows_count
            
            if target != column and missing <= fill_na_treshold and df[column].dtype.kind in 'biufc':
                df[column]=df[column].fillna(df[column].mean())
            if missing <= fill_na_treshold and df[column].dtype == "object":
                df[column] = df[column].fillna("Not assigned")
            elif missing <= drop_na_treshold:
                df = df.dropna(subset=[column]) 
            else:
                df = df.drop(columns=[column])

        return df
         
    def make_default_tresholds(self, columns) -> dict[t.Any, Treshold]:
        tresholds = {}
        for column in columns:
            tresholds[column] = Treshold(
                fill_na_treshold=fill_na_default_treshold, 
                drop_na_treshold=drop_na_default_treshold
            )
        return tresholds
        