import pandas as pd 

class DataTransformer:
    def process(self, df: pd.DataFrame, target=None) -> pd.DataFrame:
        raise Exception("process method must be implemented")