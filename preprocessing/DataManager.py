from preprocessing.missing_values.MissingValuesFiller import MissingValuesFiller
from preprocessing.missing_values.Treshold import Treshold
from preprocessing.decimal_encoding.DecimalEncoder import DecimalEncoder
from preprocessing.object_tagging.ObjectTagger import ObjectTagger
from models.Interval import Interval
from preprocessing.standarizer.Standarizer import Standarizer
import os.path
import pandas as pd
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
        self.df = self.df.drop(columns=self.config['dropped_columns'])

    def init_standarizer(self):
        intervals = {}
        for column in self.df.columns:
            if self.config[column].get('value_ranges') is None:
                self.value_standarizer = Standarizer(self.df, self.target)
                return
            
            data = {}
            for key, value_range in self.config[column]['value_ranges'].items():
                data[int(key)] = Interval(value_range['begin'], value_range['end'])
            intervals[column] = data

        self.value_standarizer = Standarizer(self.df, self.target, data)

    def dropColumn(self, column):
        self.df = self.df.drop(columns=[column])
        self.config['dropped_columns'].append(column)

    def getTarget(self):
        return self.config["target"]

    def setTarget(self, target):
        self.config["target"] = target
        self.save_config()

    def getFillMissing(self, column):
        return self.config[column]['missing_values']

    def setFillMissing(self, column, treshold: Treshold):
        self.config[column]['missing_values'] = {
            'fill_na_treshold': treshold.fill_na_treshold,
            'drop_na_treshold': treshold.drop_na_treshold
        }
        self.save_config()
    
    def getMultipier(self, column):
        return self.config[column]['float_multiplier']
    
    def setMultipier(self, column, float_multiplier):
        self.config[column]['float_multiplier'] = float_multiplier
        self.save_config()

    def getMaxUniqueObjects(self, column):
        return self.config[column]['max_unique_objects']
    
    def setMaxUniqueObjects(self, column, max_unique_count):
        self.config[column]['max_unique_objects'] = max_unique_count
        self.save_config()

    def getValueRanges(self, column):
        if self.config[column].get('value_ranges') is None:
            self.setValueRanges(self.value_standarizer.intervals)

        data = {}
        for key, value_range in self.config[column]['value_ranges'].items():
            data[int(key)] = Interval(value_range['begin'], value_range['end'])
        return data

    def setValueRanges(self, column, value_ranges: dict[Interval]):
        data = {}
        for key, value_range in value_ranges.items():
            data[int(key)] = {'begin': int(value_range.begin), 'end': int(value_range.end)}

        self.config[column]['value_ranges'] = data
        self.save_config()

    def fill_missing(self):
        tresholds = {}
        for column in self.df.columns:
            treshold = self.config[column]['missing_values']
            tresholds[column] = Treshold(treshold['fill_na_treshold'], treshold['drop_na_treshold'])

        self.df = self.missing_filler.process(self.df, self.target, tresholds)

    def encode_floats(self):
        data = {}
        for column in self.df.columns:
            data[column] = self.config[column]['float_multiplier']
        
        self.df = self.decimal_encoder.process(self.df, self.target, data)

    def encode_objects(self):
        data = {}
        for column in self.df.columns:
            data[column] = self.config[column]['max_unique_objects']

        self.df = self.object_tagger.process(self.df, self.target, data)

    def standarize(self):
        data = {}
        for column in self.df.columns:
            data[column] = self.config[column]['value_ranges']

        self.df = self.value_standarizer.process(self.df, self.target)

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
        config["target"] = self.target
        config['dropped_columns'] = []

        missing_filler_settings = self.missing_filler.default(self.df)
        decimal_encoder_settings = self.decimal_encoder.default(self.df)
        object_tagger_settings = self.object_tagger.default(self.df)

        for column in self.df.columns:
            config[column] = {}
            
            if missing_filler_settings.get(column) is not None:
                config[column]['missing_values'] = {
                    'fill_na_treshold': missing_filler_settings[column].fill_na_treshold,
                    'drop_na_treshold': missing_filler_settings[column].drop_na_treshold
                }

            if decimal_encoder_settings.get(column) is not None:
                config[column]['float_multiplier'] = decimal_encoder_settings[column]

            if decimal_encoder_settings.get(column) is not None:
                config[column]['max_unique_objects'] = object_tagger_settings[column]

        return config
    
    def save_config(self, mode="w"):
        with open(self.config_file, mode) as file:
            json.dump(self.config, file)
            file.write('\n')
    


