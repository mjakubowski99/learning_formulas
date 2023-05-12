from preprocessing.Preprocessor import Preprocessor
from models.FormulaCollection import FormulaCollection
import pandas as pd


class FormulaClassifier:

    def __init__(self, formula_collection: FormulaCollection):
        self.formula_collection = formula_collection

    def predict(self, row: list[bool]):
        return self.__vote_for_class(row)

    def __vote_for_class(self, row: list[bool]):
        votes = {}
        for decision_class in self.formula_collection.formulas:
            votes[decision_class] = 0
            for formula in self.formula_collection.formulas[decision_class]:
                if formula.satisfied_by(row):
                    votes[decision_class] += 1

        most_voted_class = -1
        max_votes = -1
        for decision_class in votes:
            if votes[decision_class] > max_votes:
                max_votes = votes[decision_class]
                most_voted_class = decision_class

        if most_voted_class == -1:
            raise Exception("Formulas should have at least one decision class")

        return most_voted_class



                
            
            