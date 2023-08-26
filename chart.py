import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('core/result/report.csv')

#df.groupby('populaton_size', as_index=False).mean().plot.line(x='result', y='result')

x = []
y = []

i=0
for row in df['result']:
    x.append(i)
    y.append(row)
    i+=1

print(df['result'].mean())

plt.plot(x,y)
plt.show()

