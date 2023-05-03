import typing as t
from sklearn.preprocessing import LabelEncoder

default_max_unique = 5

class ObjectTagger:

    def __init__(self, columns, max_unique_counts: dict[t.Any, int]=None):
        if max_unique_counts is None:
            self.max_unique_counts = self.make_default_max_unique(columns)
        else:
            self.max_unique_counts = max_unique_counts
        self.taggers = {}

    def tag_objects(self, df, target):
        self.taggers = {}

        for column in df.columns:
            if df[column].dtype.kind in 'biufc':
                continue

            if df[column].nunique() > self.max_unique_counts[column] and column != target:
                df = df.drop(columns=[column])
                continue

            self.taggers[column] = LabelEncoder() 
            df[column] = self.taggers[column].fit_transform(df[column])

        return df 
        
    def setMaxUniqueCount(self, column, max_unique_count):
        self.max_unique_counts[column] = max_unique_count

    def getMaxUniqueCount(self, column) -> int:
        return self.max_unique_counts[column]

    def make_default_max_unique(self, columns) -> dict[t.Any, int]:
        max_unique_counts = {}
        
        for column in columns:
            max_unique_counts[column] = default_max_unique

        return max_unique_counts