from postprocessing.FormulaProcessor import FormulaProcessor
from postprocessing.FormulaDecoder import FormulaDecoder
from models.FormulaCollection import FormulaCollection
from postprocessing.FormulaPredictor import FormulaPredictor
import pandas as pd

def accuracy(arr, value):
    summ = 0
    for x in arr:
        if x == value:
            summ+=1
    return summ

def from_string(string):
    arr = []
    for x in string.split(" "):
        if x == "0":
            arr.append(0.0)
        else:
            arr.append(1.0)
    return arr 

negative = """0 0 0 0 0 1 1 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 1 1 0 1 0 0 0 0 0 0 1 1 0 1 0 0 1 1 0 0 0 0 0 1 0
0 0 0 0 0 1 1 0 1 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 1 0 0 1 0 0 0 0 0 1 0 1 1 0 0 1 1 0 0 0 0 0 1 0
0 0 0 0 0 1 0 1 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 1 1 0 0 1 0 0 0 0 0 1 1 0 1 0 0 1 1 0 0 0 0 0 0 1
0 0 0 0 0 1 0 1 0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 1 1 0 0 1 0 0 0 0 0 1 1 0 1 0 0 1 1 0 0 0 0 0 1 0
0 0 0 0 0 1 0 1 1 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 1 0 0 1 0 0 0 0 0 1 1 0 1 0 0 1 1 0 0 0 0 0 1 0"""

negative_data = [from_string(x) for x in negative.split('\n')]

processor = FormulaProcessor("core/result/result.txt")

formulas = processor.process()

predictor = FormulaPredictor(formulas)

pred_a = predictor.predict_raw(negative_data)

print(pred_a)
