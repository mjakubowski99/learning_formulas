from dataclasses import dataclass
from models.Clause import Clause
import pandas as pd 

@dataclass
class Formula:
    clauses: list[Clause]

    def literals_count(self):
        length = 0
        for clause in self.clauses:
            length += len(clause.literals)
        return length


    def satisfied_by(self, row: list[bool]):
        for clause in self.clauses:
            positive = False 
            for literal in clause.literals:
                positive = positive or (bool(row[literal.index]) == literal.positive)

            if not positive:
                return False
        return True
                
