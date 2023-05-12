from postprocessing.FormulaProcessor import FormulaProcessor
from models.FormulaCollection import FormulaCollection
from classifier.FormulaClassifier import FormulaClassifier

processor = FormulaProcessor("core/result/1682165454.txt")
formulas = FormulaCollection(processor.process())

clf = FormulaClassifier(formulas)

print(clf.predict([x%2==0 for x in range(0,300)]))



