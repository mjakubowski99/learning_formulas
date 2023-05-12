from dataclasses import dataclass
from models.Formula import Formula

@dataclass
class FormulaCollection:
    formulas: dict[int, list[Formula]]

    def item_size(self):
        for decision_class in self.formulas:
            return self.formulas[decision_class][0].literals_count()
        return 0
        

    