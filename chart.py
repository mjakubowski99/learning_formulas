import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('core/result/report.csv')

df.groupby('populations_count', as_index=False).mean().plot.line(x='populations_count', y='result')

plt.show()