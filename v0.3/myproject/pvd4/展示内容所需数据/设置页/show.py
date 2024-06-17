import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np

# 读取Excel文件
df = pd.read_excel('C:\\Users\\whitefork\\Desktop\\python\\myproject\\pvd4\\展示内容所需数据\\设置页\\辐照度图.xlsx', sheet_name='训练数据')

x=df.iloc[1:,1]


plt.plot(range(0, len(x)), x)
plt.show()