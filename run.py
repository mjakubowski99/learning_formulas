import pandas as pd 

df = pd.read_csv('datasets/dataset5/letter-recognition.csv')

print(df[df.letter.isin(['T', 'I', 'D', 'A', 'C', 'X', 'Y', 'Z'])].reset_index().to_csv('datasets/dataset5/letter-recognition1.csv'))