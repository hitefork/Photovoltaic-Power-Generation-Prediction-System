import pandas as pd
import matplotlib.pyplot as plt
# 读取Excel文件
df = pd.read_excel('myproject\\pvd4\\comparison.xlsx', sheet_name='Sheet1_stc', header=None)

# 将数据存储到二维数组中
data_array = df.values

# 读取Excel文件
df1 = pd.read_excel('myproject\\pvd4\\comparison.xlsx', sheet_name='0', header=None)
df2 = pd.read_excel('myproject\\pvd4\\sample_test.xlsx', sheet_name='normal', header=None)

# 提取第一列数据到单独的数组
column1_array = df1.iloc[1:, 0].values

# 提取第二到第六列数据到四个单独的数组
column2_array = df1.iloc[1, 1:6].values
column3_array = df1.iloc[2, 1:6].values
column4_array = df1.iloc[3, 1:6].values
column5_array = df1.iloc[4, 1:6].values

# 打印第一列数据数组
print("第一列数据数组:")
print(column1_array)
print(type(column1_array[0]))
# 打印第二到第六列数据数组
print("第二列数据数组:")
print(column2_array)
print("第三列数据数组:")
print(column3_array)
print("第四列数据数组:")
print(column4_array)
print("第五列数据数组:")
print(column5_array)


u=df2.iloc[1:, 3].values
print("u:")
print(u)


# 坐标轴数据
label =column1_array

x = [i for i in range(0, 40)]
y = df.iloc[:, 0].values
colors = ['g','r','b','y']

# 绘制折线
for i in range(len(x)-1):
    plt.plot([x[i], x[i+1]], [y[i], y[i+1]], 
             color=colors[label[i]-1], linewidth=2)

# 展示
plt.show()
y=df.iloc[:, :].values
print("y:")
print(y.shape)