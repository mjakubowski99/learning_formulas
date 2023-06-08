from postprocessing.FormulaProcessor import FormulaProcessor
from models.FormulaCollection import FormulaCollection
from postprocessing.FormulaPredictor import FormulaPredictor
import pandas as pd 

processor = FormulaProcessor("core/result/1685481741.txt")
formulas = processor.process()

predictor = FormulaPredictor(formulas)
df = pd.read_csv('datasets/wine.csv')

print( predictor.predict(df, 'datasets/config.json'))




