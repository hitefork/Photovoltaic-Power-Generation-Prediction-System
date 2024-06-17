# coding=utf-8
import json
import requests
import time
import datetime
import csv
import pandas as pd

# 获取当前时间
current_time = datetime.datetime.now()

# 减去8小时
new_time = current_time - datetime.timedelta(hours=7)

# 格式化为指定格式
t = new_time.strftime('%Y-%m-%dT%H:00+00:00')

t1=time.localtime()
df = pd.read_csv('C:\\Users\\whitefork\\Desktop\\python\\myproject\\test1\\G.csv',engine='python')
# 按行读取保存到字典里，假设每行有三个字段，item_id,info,title
index=0

Gurl='https://api.qweather.com/v7/solar-radiation/24h?'
Turl='https://devapi.qweather.com/v7/weather/24h?'
value = {

    'location':'121.41720733125658,31.070773563325244',
    'key': 'a2ed3984a6da404da499deea1f25f953',

}

#Greq = requests.get(Gurl, params=value)
Treq = requests.get(Turl, params=value)
#Gdatas = Greq.json()
Tdatas= Treq.json()


for i in range(len(df)):
    if df["MO"][i]==t1.tm_mon and df["DY"][i]==t1.tm_mday and df["HR"][i]==t1.tm_hour:
        index=i
        break
'''
for i in range(0,24):
    print('Time:'+str(Tdatas['hourly'][i]['fxTime'])+'   T='+str(Tdatas['hourly'][i]['temp'])+'   G='+str(df["ALLSKY_SFC_SW_DWN"][index]))
    index=index+1
'''

print(Tdatas['hourly'])











