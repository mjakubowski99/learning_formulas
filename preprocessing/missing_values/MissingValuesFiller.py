from preprocessing.missing_values.Treshold import Treshold
from preprocessing.DataTransformer import DataTransformer
import pandas as pd 
import typing as t 

fill_na_default_treshold = 0.1
drop_na_default_treshold = 0.4

class MissingValuesFiller(DataTransformer):

    def __init__(self):
        self.columns_to_fill_na = []
        self.columns_to_drop_na_data = []
        self.dropped_by_tresholds = []

    def default(self, df):
        return self.make_default_tresholds(df.columns) 
    
    def process(self, df: pd.DataFrame, target, tresholds: dict[t.Any, Treshold], dropped_columns: list) -> pd.DataFrame:
        self.columns_to_fill_na = []
        self.columns_to_drop_na_data = []
        self.dropped_by_tresholds = []
        
        df = df.drop(columns=dropped_columns)
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
                self.columns_to_fill_na.append(column)
            if missing <= fill_na_treshold and df[column].dtype == "object":
                df[column] = df[column].fillna("Not assigned")
                self.columns_to_fill_na.append(column)
            elif missing <= drop_na_treshold:
                df = df.dropna(subset=[column])
                self.columns_to_drop_na_data.append(column)
            else:
                df = df.drop(columns=[column])
                self.dropped_by_tresholds.append(column)

        return df
    
    def process_saved(self, df, target, columns_to_fill_na, columns_to_drop_na_data, dropped_by_tresholds, dropped_columns):
        for column in dropped_columns:
            df = df.drop(columns=[column])

        for column in columns_to_fill_na:
            if df[column].dtype.kind in 'biufc':
                column_empty = df[column].isnull().sum() == len(df[column])

                if column_empty:
                    df[column]=df[column].fillna(0)
                else:
                    df[column]=df[column].fillna(df[column].mean())

            if df[column].dtype == "object":
                df[column] = df[column].fillna("Not assigned")

        for column in columns_to_drop_na_data:
            df = df.dropna(subset=[column])

        for column in dropped_by_tresholds:
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
        