from processing.preprocessing.MissingValuesFiller import MissingValuesFiller
from processing.preprocessing.Treshold import Treshold
from processing.preprocessing.DecimalEncoder import DecimalEncoder
from processing.preprocessing.ObjectTagger import ObjectTagger
from processing.models.Interval import Interval
from processing.preprocessing.Standarizer import Standarizer
from processing.preprocessing.Binarizer import Binarizer
import os.path
import pandas as pd
import numpy as np
import json 

class DataManager:

    def __init__(self, df: pd.DataFrame, config_file: str):
        self.df = df
        self.config_file = config_file

        self.missing_filler = MissingValuesFiller()
        self.decimal_encoder = DecimalEncoder()
        self.object_tagger = ObjectTagger()
        self.value_standarizer = None

        self.make()

    def init_standarizer(self, force_not_init=False):
        intervals = {}
        boundaries = {}
        
        for column in self.df.columns:
            if column == self.target:
                continue

            if self.config['columns'].get(column) is not None and self.config['columns'][column].get('value_ranges') is None and force_not_init:
                continue

            if self.config['columns'].get(column) is not None and self.config['columns'][column].get('value_ranges') is None and not force_not_init:
                self.value_standarizer = Standarizer(self.df, self.target)
                return
            
            data = {}
            for key, value_range in self.config['columns'][column]['value_ranges'].items():
                data[int(key)] = Interval(value_range['begin'], value_range['end'])
            intervals[column] = data
            boundaries[column] = self.config['columns'][column]['boundaries']

        self.value_standarizer = Standarizer(self.df, self.target, intervals, boundaries)

    def columnDropped(self, column):
        return column in self.config['dropped_columns']

    def dropColumn(self, column):
        self.config['dropped_columns'].append(column)
        self.save_config()

    def getTarget(self):
        return self.config.get("target")

    def setTarget(self, target):
        self.target = target

        self.config["target"] = target
        self.config['classes'] = self.df[self.target].fillna('').unique().tolist()
        self.config['classes'].sort()
        self.save_config()

    def getClasses(self):
        return self.config['classes']

    def getFillMissing(self, column):
        return self.config['columns'][column]['missing_values']

    def setFillMissing(self, column, treshold: Treshold):
        self.config['columns'][column]['missing_values'] = {
            'fill_na_treshold': treshold.fill_na_treshold,
            'drop_na_treshold': treshold.drop_na_treshold
        }
        self.save_config()
    
    def getMultipier(self, column):
        return self.config['columns'][column]['float_multiplier']
    
    def setMultipier(self, column, float_multiplier):
        self.config['columns'][column]['float_multiplier'] = float_multiplier
        self.save_config()

    def getMaxUniqueObjects(self, column):
        return self.config['columns'][column]['max_unique_objects']
    
    def setMaxUniqueObjects(self, column, max_unique_count):
        self.config['columns'][column]['max_unique_objects'] = max_unique_count
        self.save_config()

    def getValueRanges(self, column):
        if column == self.target:
            return {} 
        
        if self.config['columns'][column].get('value_ranges') is None:
            self.setValueRanges(self.value_standarizer.intervals)

        data = {}
        for key, value_range in self.config['columns'][column]['value_ranges'].items():
            data[int(key)] = Interval(value_range['begin'], value_range['end'])
        return data
    
    def getBoundaries(self, column):
        return self.config['columns'][column]['boundaries']
    
    def setBoundaries(self, column, boundaries: dict):
        if column == self.target:
            return {} 
        
        self.config['columns'][column]['boundaries'] = {
            'min': int(boundaries['min']),
            'max': int(boundaries['max']),
            'boundary': int(boundaries['boundary']),
        }
        self.value_standarizer.boundaries[column] = self.config['columns'][column]['boundaries']
        self.save_config()

    def setValueRanges(self, column, value_ranges: dict[Interval]):
        data = {}
        for key, value_range in value_ranges.items():
            data[int(key)] = {'begin': int(value_range.begin), 'end': int(value_range.end)}

        self.config['columns'][column]['value_ranges'] = data

        data = {}
        for key, value_range in self.config['columns'][column]['value_ranges'].items():
            data[int(key)] = Interval(value_range['begin'], value_range['end'])
        self.value_standarizer.intervals[column] = data
        self.save_config()

    def setMaxStandarizedValue(self, column, value):
        self.config['columns'][column]['max_standarized_value'] = int(value)
        self.save_config()

    def getMaxStandarizedValue(self, column):
        return self.config['columns'][column]['max_standarized_value']

    def fill_missing(self):
        tresholds = {}
        for column in self.df.columns:
            treshold = self.config['columns'][column]['missing_values']
            tresholds[column] = Treshold(treshold['fill_na_treshold'], treshold['drop_na_treshold'])

        self.df = self.missing_filler.process(self.df, self.target, tresholds, self.config['dropped_columns'])

    def bound_to_only_saved_columns(self):
        for column in self.df.columns:
            if column not in self.config['saved_columns']:
                self.df = self.df.drop(columns=[column])
            else:
                if self.df[column].dtype.kind in 'biufc':
                    self.df[column] = self.df[column].fillna(0.0)
                else:
                    self.df[column] = self.df[column].fillna('Not assigned')

    def encode_floats(self):
        data = {}
        for column in self.df.columns:
            data[column] = self.config['columns'][column]['float_multiplier']
        
        self.df = self.decimal_encoder.process(self.df, self.target, data)

    def encode_objects(self, encode_only=False):
        data = {}
        for column in self.df.columns:
            data[column] = self.config['columns'][column]['max_unique_objects']

        self.df = self.object_tagger.process(self.df, self.target, data, encode_only)

    def standarize(self):
        data = {}
        self.config['saved_columns'] = self.df.columns.tolist()
        self.save_config()

        for column in self.df.columns:
            if column == self.target:
                continue
            
            if self.config['columns'][column].get('value_ranges') is None:
                self.df = self.df.drop(columns=[column])
                continue

            data[column] = self.config['columns'][column]['value_ranges']

        self.df = self.value_standarizer.process(self.df, self.target)

    def process_saved(self):
        self.bound_to_only_saved_columns()
        self.encode_floats()
        self.encode_objects(True)
        self.standarize()

        result = []
        for x in range(0, len(self.df)+2):
            result.append([])

        target = self.config['target']
        
        max_rows = {}
        for column in self.df.columns:
            if column == target:
                continue

            max_rows[column] = self.getMaxStandarizedValue(column)

        result = [[] for i in range(0, len(self.df))]

        for column in self.df.columns:
            if column == target:
                continue

            binarizer = Binarizer()

            values = self.df[column].values.tolist()

            encoded = binarizer.fit_transform(values, max_rows[column])
            i=0
            for value in encoded:
                result[i].extend(value)
                i+=1

        return result


    def getData(self):
        return self.df 

    def make(self):
        if not os.path.isfile(self.config_file):
            self.config = self.build_config()
            self.save_config()
        
        with open(self.config_file) as json_file:
            self.config = json.load(json_file)
            
        self.target = self.config["target"]
           
    def build_config(self):
        config = {}

        self.target = self.df.columns[0]

        config['classes'] = self.df[self.target].unique().tolist()
        config["target"] = self.target
        config['dropped_columns'] = []
        config['columns'] = {}

        missing_filler_settings = self.missing_filler.default(self.df)
        decimal_encoder_settings = self.decimal_encoder.default(self.df)
        object_tagger_settings = self.object_tagger.default(self.df)

        for column in self.df.columns:
            config['columns'][column] = {}
            
            if missing_filler_settings.get(column) is not None:
                config['columns'][column]['missing_values'] = {
                    'fill_na_treshold': missing_filler_settings[column].fill_na_treshold,
                    'drop_na_treshold': missing_filler_settings[column].drop_na_treshold
                }

            if decimal_encoder_settings.get(column) is not None:
                config['columns'][column]['float_multiplier'] = decimal_encoder_settings[column]

            if decimal_encoder_settings.get(column) is not None:
                config['columns'][column]['max_unique_objects'] = object_tagger_settings[column]

        return config
    
    def save_config(self, mode="w"):
        with open(self.config_file, mode) as file:
            json.dump(self.config, file)
            file.write('\n')
    


