from models.Formula import Formula
from postprocessing.FormulaClassVoter import FormulaClassVoter
from preprocessing.DataManager import DataManager
import pandas as pd
import numpy as np

class FormulaPredictor:

    def __init__(self, formulas: dict[Formula]):
        self.formulas = formulas
        self.formula_class_voter = FormulaClassVoter()

    def predict(self, df: pd.DataFrame, config):
        data_manager = DataManager(df, config)
        data_manager.init_standarizer(True)

        cloned_df = df.copy()
        cloned_data_manager = DataManager(cloned_df, config)

        cloned_data_manager.bound_to_only_saved_columns()
        cloned_data_manager.encode_objects(True)
        cloned_df = cloned_data_manager.getData()
        
        processed_df = data_manager.process_saved()
        classes = data_manager.getClasses()

        class_indexes = self.predict_raw(processed_df)

        result = []
        i=0
        score = 0

        if cloned_df.get(data_manager.getTarget()) is None:
            for class_index in class_indexes:
                if class_index is not None:
                    predicted = classes[class_index]
                else:
                    predicted = -1

                result.append(predicted)

            self.score = None 
            return result

        for row in cloned_df[data_manager.getTarget()]:
            
            if class_indexes[i] is not None:
                predicted = classes[class_indexes[i]]
            else:
                predicted = -1

            if predicted == row:
                score+=1
            result.append(predicted)
            i+=1

        self.score = score/len(df)

        return result

    def predict_raw(self, data: list[list[bool]]):
        predictions = []

        for row in data:
            predictions.append(
                self.formula_class_voter.class_with_most_votes(row, self.formulas)
            )

        return predictions
