import csv
import pandas as pd
import time
import datetime
# 获取当前时间
# 指定要读取的 CSV 文件路径

t1=time.localtime()
df = pd.read_csv('C:\\Users\\whitefork\\Desktop\\python\\myproject\\test1\\G.csv',engine='python')
# 按行读取保存到字典里，假设每行有三个字段，item_id,info,title
index=0
for i in range(len(df)):
    if df["MO"][i]==t1.tm_mon and df["DY"][i]==t1.tm_mday and df["HR"][i]==t1.tm_hour:
        index=i
        break


for i in range(index,index+24):
    print(df["ALLSKY_SFC_SW_DWN"][i])
    
