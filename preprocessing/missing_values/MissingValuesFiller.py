from preprocessing.missing_values.Treshold import Treshold
import pandas as pd 
import typing as t 

fill_na_default_treshold = 0.1
drop_na_default_treshold = 0.4

class MissingValuesFiller:

    def __init__(self, columns, tresholds: dict[t.Any, Treshold]=None):
        if tresholds is None:
            self.__tresholds = self.make_default_tresholds(columns)
        else:
            self.__tresholds = tresholds
    
    def fill_missing(self, df: pd.DataFrame, target):
        rows_count = len(df)

        for column in df.columns:
            print("Filling missing for column: "+column)

            missing = df[column].isnull().sum()/rows_count
            if missing == 0:
                continue

            fill_na_treshold = self.__tresholds[column].fill_na_treshold
            drop_na_treshold = self.__tresholds[column].drop_na_treshold 

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
    
    def getTresholds(self) -> dict[t.Any, Treshold]:
        return self.__tresholds
    
    def setTreshold(self, column, fill_na_treshold, drop_na_treshold):
        self.__tresholds[column].fill_na_treshold = fill_na_treshold
        self.__tresholds[column].drop_na_treshold = drop_na_treshold
         
    def make_default_tresholds(self, columns) -> dict[t.Any, Treshold]:
        tresholds = {}
        for column in columns:
            tresholds[column] = Treshold(
                fill_na_treshold=fill_na_default_treshold, 
                drop_na_treshold=drop_na_default_treshold
            )
        return tresholds
        