from models.Literal import Literal
from models.Clause import Clause
from models.Formula import Formula

class FormulaDecoder:

    def cnf_from_string(self, line: str):
        clauses = []
        for clause in line.split('^'):
            literals = []
            for literal in clause[1:-1].split('v'):
                if literal[-1] == ')':
                    literal = literal[:-1]
                literals.append(self.literal_from_string(literal))
            clauses.append(Clause(literals))

        return Formula(clauses)

    def literal_from_string(self, literal: str):
        if literal[0:2] == '~X':
            positive = False
        elif literal[0:1] == "X":
            positive = True 
        else:
            raise Exception("Unkown literal format. Expected format is for e.g X123 or ~X12")
        
        index = int(literal.split("X")[1])

        return Literal(index, positive)


        

        

        



