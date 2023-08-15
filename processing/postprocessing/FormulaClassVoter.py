from processing.models.Formula import Formula

class FormulaClassVoter:

    def class_with_most_votes(self, row: list[bool], formulas: dict[list: Formula]):

        most_votes_class = None
        most_votes_count = 0

        for d_class in formulas:
            satisfied_count = 0
            for formula in formulas[d_class]:
                if self.satisfied(row, formula):
                    satisfied_count+=1

            if satisfied_count > most_votes_count:
                most_votes_class = d_class
                most_votes_count = satisfied_count

        return most_votes_class

    def satisfied(self, row: list[bool], formula: Formula):
        for clause in formula.clauses:
            clause_true = False
            for literal in clause.literals:
                if bool(row[literal.index]) == literal.positive:
                    clause_true = True
                    break 
            
            if clause_true == False:
                return False
        return True

