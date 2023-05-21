from preprocessing.missing_values.MissingValuesFiller import MissingValuesFiller
from preprocessing.missing_values.Treshold import Treshold
from preprocessing.decimal_encoding.DecimalEncoder import DecimalEncoder
from preprocessing.object_tagging.ObjectTagger import ObjectTagger
import os.path
import pandas as pd
import json 

class DataManager:

    def __init__(self, df: pd.DataFrame, config_file: str):
        self.df = df
        self.config_file = config_file

        self.missing_filler = MissingValuesFiller()
        #self.decimal_encoder = DecimalEncoder()
        #self.object_tagger = ObjectTagger()

        self.make()
        self.df = self.df.drop(columns=self.config['dropped_columns'])

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

    def fill_missing(self):
        tresholds = {}
        for column in self.df.columns:
            treshold = self.config[column]['missing_values']
            tresholds[column] = Treshold(treshold['fill_na_treshold'], treshold['drop_na_treshold'])

        self.df = self.missing_filler.process(self.df, self.target, tresholds)

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
        #decimal_encoder_settings = self.decimal_encoder.default(df)
        #object_tagger_settings = self.object_tagger.default(df)

        for column in self.df.columns:
            config[column] = {}
            
            if missing_filler_settings.get(column) is not None:
                config[column]['missing_values'] = {
                    'fill_na_treshold': missing_filler_settings[column].fill_na_treshold,
                    'drop_na_treshold': missing_filler_settings[column].drop_na_treshold
                }

            """
            if decimal_encoder_settings.get(column) is not None:
                config[column]['multiplier'] = decimal_encoder_settings[column]

            if object_tagger_settings.get(column) is not None:
                config[column]['max_unique_objects'] = object_tagger_settings[column]

            """

        return config
    
    def save_config(self, mode="w"):
        with open(self.config_file, mode) as file:
            json.dump(self.config, file)
            file.write('\n')
    


