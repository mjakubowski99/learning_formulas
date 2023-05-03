from postprocessing.FormulaDecoder import FormulaDecoder

class FormulaProcessor:
    
    def __init__(self, file):
        self.decoder = FormulaDecoder()
        self.file = file

    def process(self):
        formulas = {}
        current_class = 0
        for line in self.file.readlines():
            if line[0] == "(":
                formulas[current_class].append(self.decoder.cnf_from_string(line))
            else:
                current_class = int(line)

            
