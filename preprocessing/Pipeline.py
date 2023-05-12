from preprocessing.DataTransformer import DataTransformer
import pandas as pd 

class Pipeline:
    
    def __init__(self, steps: list[DataTransformer] = []):
        self.steps = steps

    def add(self, step: DataTransformer):
        self.steps.append(step)

    def process(self, df: pd.DataFrame, target=None):
        for step in self.steps:
            df = step.procees(df, target)
        return df 