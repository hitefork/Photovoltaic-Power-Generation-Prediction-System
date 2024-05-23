import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data from the Excel file
data = pd.read_excel("C:\\Users\\whitefork\\Desktop\\python\\myproject\\test1\\data1.xlsx")

# Convert the DataFrame to a numpy array
data_array = data.to_numpy()

# Randomly select 30 rows
np.random.shuffle(data_array)
selected_data = data_array[:30]

x=[]
y=[]
x_green=[]
x_red=[]
x_blue=[]
x_yellow=[]
y_green=[]
y_red=[]
y_blue=[]
y_yellow=[]
for i in range(0,30):
    x.append(i)
    y.append(selected_data[i][0])
    if selected_data[i][1]==1:
        x_green.append(i)
        y_green.append(selected_data[i][0])
    elif selected_data[i][1]==2:
        x_red.append(i)
        y_red.append(selected_data[i][0])
    elif selected_data[i][1]==3:
        x_blue.append(i)
        y_blue.append(selected_data[i][0])
    elif selected_data[i][1]==4:
        x_yellow.append(i)
        y_yellow.append(selected_data[i][0])

        
plt.figure()
# Plot red points
plt.scatter(x_green, y_green, color='green',s=100)

plt.scatter(x_red, y_red, color='red',s=100)
plt.scatter(x_blue, y_blue, color='blue',s=100)
# Plot blue points
plt.scatter(x_yellow, y_yellow, color='yellow',s=100)

# Connect points with black dashed line
plt.plot(x, y, linestyle='dashed', color='black')

plt.show()
