from processing.postprocessing.FormulaDecoder import FormulaDecoder
from processing.models.Formula import Formula

class FormulaProcessor:
    
    def __init__(self, file):
        self.decoder = FormulaDecoder()
        self.file = open(file)

    def process(self) -> dict[list[Formula]]:
        formulas = {}
        current_class = 0
        for line in self.file.readlines():
            if formulas.get(current_class) is None:
                formulas[current_class] = []

            if line[0] == "(":
                formulas[current_class].append(self.decoder.cnf_from_string(line))
            else:
                current_class = int(line)

        self.file.close()

        return formulas 
            
