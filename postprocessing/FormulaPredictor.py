from models.Formula import Formula
from postprocessing.FormulaClassVoter import FormulaClassVoter
from preprocessing.DataManager import DataManager
import pandas as pd 

class FormulaPredictor:

    def __init__(self, formulas: dict[Formula]):
        self.formulas = formulas
        self.formula_class_voter = FormulaClassVoter()

    def predict(self, df: pd.DataFrame, config):
        data_manager = DataManager(df, config)
        data_manager.init_standarizer()
        
        df = data_manager.process_all_at_once()

        return self.predict_raw(df)

    def predict_raw(self, data: list[list[bool]]):
        predictions = []

        for row in data:
            predictions.append(
                self.formula_class_voter.class_with_most_votes(row, self.formulas)
            )

        return predictions
