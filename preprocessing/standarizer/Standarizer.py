from models.Interval import Interval
from preprocessing.DataTransformer import DataTransformer
import pandas as pd 

def encode_column(x, intervals: dict[int, Interval]):
    for label, interval in intervals.items():
        if x >= interval.begin and x<=interval.end:
            return label
    raise Exception("Failed to encode value")

class Standarizer(DataTransformer):

    def __init__(self, df, target, intervals: dict=None, boundaries: dict=None):
        self.default_boundary = 5

        if boundaries is None:
            self.boundaries = {}
        else:
            self.boundaries = boundaries

        if intervals is None:
            self.intervals = self.init_intervals(df, target)
        else:
            self.intervals = intervals

    def process(self, df: pd.DataFrame, target=None) -> pd.DataFrame:
        for column in df.columns:
            if column == target:
                continue
            if df[column].min() == 0 or df[column].max() in [0,1]:
                continue
            df[column] = df[column].apply(encode_column, intervals=self.intervals[column])
        return df 

    def init_intervals(self, df, target):
        intervals = {}
        for column in df.columns:
            self.boundaries[column] = {
                'min': df[column].min(),
                'max': df[column].max(),
                'boundary': self.default_boundary
            }

            params = self.boundaries[column]
            intervals[column] = self.generate_intervals(params['min'], params['max'], params['boundary'])

        return intervals
    
    def getFullBoundary(self, column):
        return self.boundaries[column]
    
    def getBoundary(self, column):
        return self.boundaries[column]['boundary']
    
    def setBoundary(self, column, boundary: int):
        self.boundaries[column]['boundary'] = boundary
        params = self.boundaries[column]
        self.intervals[column] = self.generate_intervals(params['min'],params['max'],params['boundary'])

    def setIntervals(self, column, intervals):
        self.intervals[column] = intervals

    def getColumnIntervals(self, column):
        return self.intervals[column]

    def getIntervals(self):
        return self.intervals

    def generate_intervals(self, min, max, new_max):
        intervals = {}
        if new_max >= max:
            i=min
            while i<=max:
                intervals[i] = Interval(i,i)
                i+=1
            return intervals

        old_min = min
        if min < 0:
            min = 0
            max = max+abs(old_min)

        new_max += 1
        i = 0

        it_begin = min
        it_end = min

        while i < new_max:
            percents = (i+1) / new_max
            
            it_end = int(((max-min) * percents) + min )
            intervals[i] = Interval(it_begin, it_end)

            it_begin = it_end
            i+=1

        if old_min < 0:
            for label in intervals:
                intervals[label].begin -= abs(old_min)
                intervals[label].end -= abs(old_min)


        return intervals
