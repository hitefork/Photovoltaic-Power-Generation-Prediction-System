import pandas as pd
import matplotlib.pyplot as plt

df4 = pd.read_excel('myproject\\pvd4_1\\traindata.xlsx',  header=None)

print(len(df4.iloc[1:41, 1].values))
