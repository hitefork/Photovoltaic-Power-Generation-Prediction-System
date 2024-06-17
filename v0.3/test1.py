import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QDesktopWidget,QWidget,QGridLayout,QComboBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt,QTimer
from functools import partial
import untitled

from untitled import Ui_MainWindow
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.cbook as cbook
import numpy as np
import random

import pandas as pd
import pyqtgraph as pg
import math
import json
import requests
import time
import datetime
import csv
import os
from threading import Thread
from threading import currentThread  # 获取当前线程对象的 对象
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

t1=time.localtime()
df = pd.read_csv('myproject\\test1\\G.csv',engine='python')









def get_G_data():
    G=[]

    my_index=0
    Gurl='https://api.qweather.com/v7/solar-radiation/24h?'

    value = {

    'location':'121.41720733125658,31.070773563325244',
    'key': 'a2ed3984a6da404da499deea1f25f953',

     }

    #Greq = requests.get(Gurl, params=value)

    #Gdatas = Greq.json()



    for i in range(len(df)):
        if df["MO"][i]==t1.tm_mon and df["DY"][i]==t1.tm_mday and df["HR"][i]==t1.tm_hour:
            my_index=i
            break

    for i in range(0,20):
        #print('Time:'+str(Tdatas['hourly'][i]['fxTime'])+'   T='+str(Tdatas['hourly'][i]['temp'])+'   G='+str(df["ALLSKY_SFC_SW_DWN"][index]))
        G.append(df["ALLSKY_SFC_SW_DWN"][my_index])
        my_index=my_index+1
    return G


def get_T_data():
    T=[]
    Turl='https://devapi.qweather.com/v7/weather/24h?'
    my_index=0
    value = {

    'location':'121.41720733125658,31.070773563325244',
    'key': 'a2ed3984a6da404da499deea1f25f953',

     }
    Treq = requests.get(Turl, params=value)
    Tdatas= Treq.json()
    for i in range(0,20):
        #print('Time:'+str(Tdatas['hourly'][i]['fxTime'])+'   T='+str(Tdatas['hourly'][i]['temp'])+'   G='+str(df["ALLSKY_SFC_SW_DWN"][index]))
        T.append(int(Tdatas['hourly'][i]['temp']))
        my_index=my_index+1
    int(Tdatas['hourly'][0]['icon'])
    return T

def get_weather_data():
    weather=[]
    Turl='https://devapi.qweather.com/v7/weather/24h?'
    my_index=0
    value = {

    'location':'121.41720733125658,31.070773563325244',
    'key': 'a2ed3984a6da404da499deea1f25f953',

     }
    Treq = requests.get(Turl, params=value)
    Tdatas= Treq.json()
    weather.append(Tdatas['hourly'][0]['icon'])
    weather.append(Tdatas['hourly'][0]['text'])
    weather.append(Tdatas['hourly'][0]['pop'])
    weather.append(Tdatas['hourly'][0]['pressure'])
    weather.append(Tdatas['hourly'][0]['cloud'])
    weather.append(Tdatas['hourly'][0]['temp'])

    return weather




class Figure_Canvas(FigureCanvas):

    def __init__(self,parent=None,width=3.9,height=2.7,dpi=100):
        self.fig=Figure(figsize=(width,height),dpi=100)
        super(Figure_Canvas,self).__init__(self.fig)
        self.ax=self.fig.add_subplot(111)
    
    def clear(self):
        self.fig.clf()
        self.ax=self.fig.add_subplot(111)

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class myLoadingProgress(QtWidgets.QDialog):
    update_signal = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super(myLoadingProgress, self).__init__(parent)
        self.value = 0
        self.update_signal.connect(self.update_progress)
        vbox = QtWidgets.QVBoxLayout(self)

        self.movie_label = QtWidgets.QLabel()
        self.movie = QtGui.QMovie("myproject\\gif\\loading.gif")
        self.movie_label.setMovie(self.movie)
        self.movie.start()
        self.progress_label = QtWidgets.QLabel()


        vbox.addWidget(self.movie_label)
        vbox.addWidget(self.progress_label)
        self.progress_label.setText("计算中...")
        self.setLayout(vbox)
        self.timer =QtCore.QTimer()
        # 实例化一个定时器

        self.timer.timeout.connect(self.update_progress)
        # 将定时器信号绑定到update_data 函数

        self.timer.start(5000)#五秒更新一次
        self.exec_()
        

    def update_progress(self) :
        self.close()


class ImgDisp(QMainWindow,Ui_MainWindow):
    find_state=0
    true_start_date=1
    true_end_date=31
    true_start_date1=1
    true_end_date1=1
    true_start_date2=1
    true_end_date2=90
    index1=0
    diff_days1=0
    myvector=0
    myflag1=0
    myflag2=0
    myflag3=0
    nowflag=1
    readyornot=[0,0,0,0,0,0,0,0]

    def __init__(self,parent=None):
        super(ImgDisp,self).__init__(parent)
        self.setupUi(self)
        self.Init_Widgets()
        # 解决无法显示中文
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # 解决无法显示负号
        plt.rcParams['axes.unicode_minus'] = False
                # 设置软件图标
        #self.setWindowIcon(QtGui.QIcon("icon.ico"))
        # 设置主界面标题
        self.setWindowTitle("光伏预测")




    def Init_Widgets(self):
        self.PrepareSamples()
        self.PrepareSamples1()
        self.PrepareSamples2()

        self.PrepareSamples5()
        self.PrepareSamples4()
        self.PrepareSamples7()
        self.PrepareSamples8()
        self.PrepareSamples9()
        self.PrepareSamples13()
        self.PrepareSamples14()
        self.PrepareLineCanvas()
        self.PrepareLineCanvas1()
        self.PrepareLineCanvas3()
        self.PrepareLineCanvas4()
        self.PrepareLineCanvas5()
        self.PrepareLineCanvas7()
        self.PrepareLineCanvas8()
        self.PrepareLineCanvas9()
        self.PrepareLineCanvas10()
        self.PrepareLineCanvas11()

        self.PrepareLineCanvas13()
        self.LineFigure14 = Figure_Canvas()
        self.LineFigureLayout14 = QGridLayout(self.LineDisplayGB14)
        self.LineFigureLayout14.addWidget(self.LineFigure14)


    def PrepareSamples(self):        


        if self.myfind_state==0:
            df1 = pd.read_excel('myproject\\pvd4\\展示内容所需数据\\状态监测页\\特征向量展示图.xlsx', sheet_name='normal', header=None)
        elif self.myfind_state==1:
            df1=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\状态监测页\\特征向量展示图.xlsx',sheet_name='LL',header=None)
        elif self.myfind_state==2:
            df1=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\状态监测页\\特征向量展示图.xlsx',sheet_name='OC',header=None)
        elif self.myfind_state==3:
            df1=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\状态监测页\\特征向量展示图.xlsx',sheet_name='PS1',header=None)
        elif self.myfind_state==4:
            df1=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\状态监测页\\特征向量展示图.xlsx',sheet_name='PS2',header=None)
        elif self.myfind_state==5:
            df1=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\状态监测页\\特征向量展示图.xlsx',sheet_name='PS3',header=None)
        elif self.myfind_state==6:
            df1=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\状态监测页\\特征向量展示图.xlsx',sheet_name='PS4',header=None)
        elif self.myfind_state==7:
            df1=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\状态监测页\\特征向量展示图.xlsx',sheet_name='PS5',header=None)

        weather=[]
        self.G=df1.iloc[1:, 6].values
        self.G=self.G.astype('float')
        self.T=df1.iloc[1:, 7].values
        self.T=self.T.astype('float')
        weather=get_weather_data() #当前天气
        icons='myproject\\icons\\'+weather[0]+'.svg'
        self.weather_information3.setText('天气      '+weather[1])
        self.weather_information_label.load(icons)
        self.weather_information4.setText('温度      '+str(self.T[0]))
        self.weather_information5.setText('辐照度    '+str(self.G[0]))


        self.v=df1.iloc[1:, 0].values
        self.v = self.v.astype('float')
        self.i=df1.iloc[1:, 1].values
        self.i = self.i.astype('float')
        self.p=df1.iloc[1:, 2].values
        self.p = self.p.astype('float')
        self.DATA=self.v[0:20]#只取二十个数据展示
        self.DATA1=self.i[0:20]#只取二十个数据展示
        self.DATA2=self.p[0:20]#只取二十个数据展示

        self.vstc=df1.iloc[1:, 3].values
        self.vstc = self.vstc.astype('float')
        self.istc=df1.iloc[1:, 4].values
        self.istc=self.istc.astype('float')
        self.pstc=df1.iloc[1:, 5].values
        self.pstc=self.pstc.astype('float')
        
        
        self.DATA_1=[]
        self.DATA1_1=[]
        self.DATA2_1=[]
        self.DATA_1=self.vstc[0:20]#只取二十个数据展示
        self.DATA1_1=self.istc[0:20]#只取二十个数据展示
        self.DATA2_1=self.pstc[0:20]#只取二十个数据展示
        


        

    
    
    



        
        self.index=0



    def PrepareSamples1(self):
        df4=pd.read_excel('myproject\\pvd4_1\\traindata.xlsx',sheet_name='Sheet1',header=None)
        self.setup1=df4.iloc[self.true_start_date1*40+1+self.true_start_date1:(1+self.true_end_date1)*40+self.true_end_date1+1, 0].values
        self.setuplabel1=df4.iloc[self.true_start_date1*40+1+self.true_start_date1:(1+self.true_end_date1)*40+self.true_end_date1+1, 1].values

    def PrepareSamples2(self):
        self.random_data1=[]
        for i in range(0,self.diff_days1):

            self.random_data1.append(random.uniform(0.9, 1.0))
   


    def PrepareSamples4(self):
        self.myvector=int(4*self.myflag1+2*self.myflag2+self.myflag3)
        df3 = pd.read_excel('myproject\\pvd4\\comparison.xlsx', sheet_name=str(self.myvector), header=None)
        # 提取第一列数据到单独的数组
        self.comparsion1_label = df3.iloc[1:, 0].values
        # 提取第二到第六列数据到四个单独的数组
        self.comparsion1_normal = df3.iloc[1, 1:6].values
        self.comparsion1_LL= df3.iloc[2, 1:6].values
        self.comparsion1_OC = df3.iloc[3, 1:6].values
        self.comparsion1_PS = df3.iloc[4, 1:6].values



    def PrepareSamples5(self):

        df2 = pd.read_excel('myproject\\pvd4\\comparison.xlsx', sheet_name='7', header=None)
        # 提取第一列数据到单独的数组
        self.comparsion0_label = df2.iloc[1:, 0].values
        # 提取第二到第六列数据到四个单独的数组
        self.comparsion0_normal = df2.iloc[1, 1:6].values
        self.comparsion0_LL= df2.iloc[2, 1:6].values
        self.comparsion0_OC = df2.iloc[3, 1:6].values
        self.comparsion0_PS = df2.iloc[4, 1:6].values
        
    def PrepareSamples7(self):

        df7=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\设置页\\辐照度图.xlsx',sheet_name='测试数据',header=None)
        self.setup3yshow=df7.iloc[1+self.true_start_date*290:self.true_end_date*290, 1].values
            
    def PrepareSamples8(self):
        if self.myfind_state==0:
            df8=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\状态监测页\\概率.xlsx',sheet_name='normal',header=None)
            self.y_P_normal=df8.iloc[1:, 0].values
            self.y_p_LL=df8.iloc[1:, 1].values
            self.y_p_OC=df8.iloc[1:, 2].values
            self.y_p_PS=df8.iloc[1:, 3].values

        elif self.myfind_state==1:
            df8=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\状态监测页\\概率.xlsx',sheet_name='LL',header=None)
            self.y_P_normal=df8.iloc[1:, 0].values
            self.y_p_LL=df8.iloc[1:, 1].values
            self.y_p_OC=df8.iloc[1:, 2].values
            self.y_p_PS=df8.iloc[1:, 3].values

        elif self.myfind_state==2:
            df8=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\状态监测页\\概率.xlsx',sheet_name='OC',header=None)
            self.y_P_normal=df8.iloc[1:, 0].values
            self.y_p_LL=df8.iloc[1:, 1].values
            self.y_p_OC=df8.iloc[1:, 2].values
            self.y_p_PS=df8.iloc[1:, 3].values

        elif self.myfind_state==3:
            df8=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\状态监测页\\概率.xlsx',sheet_name='PS1',header=None)
            self.y_P_normal=df8.iloc[1:, 0].values
            self.y_p_LL=df8.iloc[1:, 1].values
            self.y_p_OC=df8.iloc[1:, 2].values
            self.y_p_PS=df8.iloc[1:, 3].values

        elif self.myfind_state==4:
            df8=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\状态监测页\\概率.xlsx',sheet_name='PS2',header=None)
            self.y_P_normal=df8.iloc[1:, 0].values
            self.y_p_LL=df8.iloc[1:, 1].values
            self.y_p_OC=df8.iloc[1:, 2].values
            self.y_p_PS=df8.iloc[1:, 3].values
        elif self.myfind_state==5:
            df8=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\状态监测页\\概率.xlsx',sheet_name='PS3',header=None)
            self.y_P_normal=df8.iloc[1:, 0].values
            self.y_p_LL=df8.iloc[1:, 1].values
            self.y_p_OC=df8.iloc[1:, 2].values
            self.y_p_PS=df8.iloc[1:, 3].values
        elif self.myfind_state==6:
            df8=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\状态监测页\\概率.xlsx',sheet_name='PS4',header=None)
            self.y_P_normal=df8.iloc[1:, 0].values
            self.y_p_LL=df8.iloc[1:, 1].values
            self.y_p_OC=df8.iloc[1:, 2].values
            self.y_p_PS=df8.iloc[1:, 3].values
        elif self.myfind_state==7:
            df8=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\状态监测页\\概率.xlsx',sheet_name='PS5',header=None)
            self.y_P_normal=df8.iloc[1:, 0].values
            self.y_p_LL=df8.iloc[1:, 1].values
            self.y_p_OC=df8.iloc[1:, 2].values
            self.y_p_PS=df8.iloc[1:, 3].values
        
        self.y_P_normal_show=self.y_P_normal[0]
        self.y_P_LL_show=self.y_p_LL[0]
        self.y_P_OC_show=self.y_p_OC[0]
        self.y_P_PS_show=self.y_p_PS[0]
        
    def PrepareSamples9(self):
        if self.myfind_state==0:
            df9=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\状态统计页\\发电状态监测结果_画图.xlsx',sheet_name='normal',header=None)
            self.y_true=df9.iloc[1:, 1].values
            self.y_pred=df9.iloc[1:, 2].values
 
        elif self.myfind_state==1:
            df9=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\状态统计页\\发电状态监测结果_画图.xlsx',sheet_name='LL',header=None)
            self.y_true=df9.iloc[1:, 1].values
            self.y_pred=df9.iloc[1:, 2].values

        elif self.myfind_state==2:
            df9=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\状态统计页\\发电状态监测结果_画图.xlsx',sheet_name='OC',header=None)
            self.y_true=df9.iloc[1:, 1].values
            self.y_pred=df9.iloc[1:, 2].values

        elif self.myfind_state==3:
            df9=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\状态统计页\\发电状态监测结果_画图.xlsx',sheet_name='PS1',header=None)
            self.y_true=df9.iloc[1:, 1].values
            self.y_pred=df9.iloc[1:, 2].values

        elif self.myfind_state==4:
            df9=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\状态统计页\\发电状态监测结果_画图.xlsx',sheet_name='PS2',header=None)
            self.y_true=df9.iloc[1:, 1].values
            self.y_pred=df9.iloc[1:, 2].values
        elif self.myfind_state==5:
            df9=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\状态统计页\\发电状态监测结果_画图.xlsx',sheet_name='PS3',header=None)
            self.y_true=df9.iloc[1:, 1].values
            self.y_pred=df9.iloc[1:, 2].values
        elif self.myfind_state==6:
            df9=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\状态统计页\\发电状态监测结果_画图.xlsx',sheet_name='PS4',header=None)
            self.y_true=df9.iloc[1:, 1].values
            self.y_pred=df9.iloc[1:, 2].values
        elif self.myfind_state==7:
            df9=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\状态统计页\\发电状态监测结果_画图.xlsx',sheet_name='PS5',header=None)
            self.y_true=df9.iloc[1:, 1].values
            self.y_pred=df9.iloc[1:, 2].values
        

    def PrepareSamples13(self):


        df13=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\设置页\\辐照度图.xlsx',sheet_name='训练数据',header=None)
        self.setupyshow=df13.iloc[1+self.true_start_date2*290:self.true_end_date2*290, 1].values


    def PrepareSamples14(self):
        if self.find_state==0:
            df14=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\设置页\\光伏出力图.xlsx',sheet_name='normal',header=None)
            self.setupyshow1=df14.iloc[1:, 1].values
            self.setupyshow1label=df14.iloc[1:, 2].values
        elif self.find_state==1:
            df14=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\设置页\\光伏出力图.xlsx',sheet_name='LL',header=None)
            self.setupyshow1=df14.iloc[1:, 1].values
            self.setupyshow1label=df14.iloc[1:, 2].values
        elif self.find_state==2:
            df14=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\设置页\\光伏出力图.xlsx',sheet_name='OC',header=None)
            self.setupyshow1=df14.iloc[1:, 1].values
            self.setupyshow1label=df14.iloc[1:, 2].values
        elif self.find_state==3:
            df14=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\设置页\\光伏出力图.xlsx',sheet_name='PS1',header=None)
            self.setupyshow1=df14.iloc[1:, 1].values
            self.setupyshow1label=df14.iloc[1:, 2].values
        elif self.find_state==4:
            df14=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\设置页\\光伏出力图.xlsx',sheet_name='PS2',header=None)
            self.setupyshow1=df14.iloc[1:, 1].values
            self.setupyshow1label=df14.iloc[1:, 2].values   
        elif self.find_state==5:
            df14=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\设置页\\光伏出力图.xlsx',sheet_name='PS3',header=None)
            self.setupyshow1=df14.iloc[1:, 1].values
            self.setupyshow1label=df14.iloc[1:, 2].values
        elif self.find_state==6:
            df14=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\设置页\\光伏出力图.xlsx',sheet_name='PS4',header=None)
            self.setupyshow1=df14.iloc[1:, 1].values
            self.setupyshow1label=df14.iloc[1:, 2].values   
        elif self.find_state==7:
            df14=pd.read_excel('myproject\\pvd4\\展示内容所需数据\\设置页\\光伏出力图.xlsx',sheet_name='PS5',header=None)
            self.setupyshow1=df14.iloc[1:, 1].values
            self.setupyshow1label=df14.iloc[1:, 2].values


        
    def PrepareLineCanvas(self):


        # 自定义时间轴标签
        ticks = []
        hour = 8
        minute = 0
        for i in range(21):
            ticks.append((5*i, f'{hour:02d}:{minute:02d}'))
            minute += 30
            if minute >= 60:
                hour += 1
                minute = 0
            if hour >= 12:
                hour = 8


        self.LineFigureLayout = QGridLayout(self.LineDisplayGB)
        self.echart=pg.PlotWidget()
        self.echart1=pg.PlotWidget()
        self.echart2=pg.PlotWidget()
        self.echart.setYRange(min(self.v),max(self.v))
        self.echart1.setYRange(min(self.i),max(self.i))
        self.echart2.setYRange(min(self.p),max(self.p))
        self.echart.setBackground('white')
        self.echart1.setBackground('white')
        self.echart2.setBackground('white')





        self.LineFigureLayout.addWidget(self.echart)
        self.LineFigureLayout.addWidget(self.echart1)
        self.LineFigureLayout.addWidget(self.echart2)

        self.curve1=self.echart.plot(self.DATA,pen='b',name="电压")
        self.curve2=self.echart1.plot(self.DATA1,pen='b',name="电流")
        self.curve3=self.echart2.plot(self.DATA2,pen='b',name="功率")
        self.echart.setLabel('left', '电压', units='V')
        self.echart.setLabel('bottom', '时间')
        self.echart1.setLabel('left', '电流', units='A')
        self.echart1.setLabel('bottom', '时间')
        self.echart2.setLabel('left', '功率', units='W')
        self.echart2.setLabel('bottom', '时间')



        self.LineFigureLayout4 = QGridLayout(self.LineDisplayGB2)
        self.echart3=pg.PlotWidget()
        self.echart4=pg.PlotWidget()
        self.echart5=pg.PlotWidget()
        self.echart3.setBackground('white')
        self.echart4.setBackground('white')
        self.echart5.setBackground('white')

        self.echart3.setXRange(0,20,padding=0)
        self.echart4.setXRange(0,20,padding=0)
        self.echart5.setXRange(0,20,padding=0)
    

        self.LineFigureLayout4.addWidget(self.echart3)
        self.LineFigureLayout4.addWidget(self.echart4)
        self.LineFigureLayout4.addWidget(self.echart5)

        self.curve4=self.echart3.plot(self.DATA_1,pen='b',name="电压")
        self.curve5=self.echart4.plot(self.DATA1_1,pen='b',name="电流")
        self.curve6=self.echart5.plot(self.DATA2_1,pen='b',name="功率")
        self.echart3.setLabel('left', '电压', units='V')
        self.echart3.setLabel('bottom', '时间')
        self.echart4.setLabel('left', '电流', units='A')
        self.echart4.setLabel('bottom', '时间')
        self.echart5.setLabel('left', '功率', units='W')
        self.echart5.setLabel('bottom', '时间')


        self.X_ptr1 = 0
        #用于记录X轴的位置
        self.curve1.setPos(self.X_ptr1,0)
        self.curve2.setPos(self.X_ptr1,0)
        self.curve3.setPos(self.X_ptr1,0)

        self.curve4.setPos(self.X_ptr1,0)
        self.curve5.setPos(self.X_ptr1,0)
        self.curve6.setPos(self.X_ptr1,0)
        
        # 将时间轴添加到 echart3、echart4 和 echart5 对象中
        self.echart.showAxis('bottom')
        self.echart.getAxis('bottom').setStyle(tickTextOffset=15)
        self.echart.getAxis('bottom').setTicks([ticks])
        self.echart1.showAxis('bottom')
        self.echart1.getAxis('bottom').setStyle(tickTextOffset=15)
        self.echart1.getAxis('bottom').setTicks([ticks])
        self.echart2.showAxis('bottom')
        self.echart2.getAxis('bottom').setStyle(tickTextOffset=15)
        self.echart2.getAxis('bottom').setTicks([ticks])        
        
        
        # 将时间轴添加到 echart3、echart4 和 echart5 对象中
        self.echart3.showAxis('bottom')
        self.echart3.getAxis('bottom').setStyle(tickTextOffset=15)
        self.echart3.getAxis('bottom').setTicks([ticks])
        self.echart4.showAxis('bottom')
        self.echart4.getAxis('bottom').setStyle(tickTextOffset=15)
        self.echart4.getAxis('bottom').setTicks([ticks])
        self.echart5.showAxis('bottom')
        self.echart5.getAxis('bottom').setStyle(tickTextOffset=15)
        self.echart5.getAxis('bottom').setTicks([ticks])
   

        self.timer =QtCore.QTimer()
        # 实例化一个定时器

        self.timer.timeout.connect(self.update_data)
        # 将定时器信号绑定到update_data 函数

        self.timer.start(1000)#三秒更新一次
    def update_data(self):#数据更新函数
        
        
        self.X_ptr1 += 1
        if self.X_ptr1==len(self.v):
            self.X_ptr1=0
        self.weather_information4.setText('温度  ' + str(round(self.T[self.X_ptr1 % self.T.size], 2)))
        self.weather_information5.setText('辐照度 ' + str(round(self.G[self.X_ptr1 % self.G.size], 2)))
        self.curve1.setPos(self.X_ptr1,0)
        self.curve2.setPos(self.X_ptr1,0)
        self.curve3.setPos(self.X_ptr1,0)

        self.curve4.setPos(self.X_ptr1,0)
        self.curve5.setPos(self.X_ptr1,0)
        self.curve6.setPos(self.X_ptr1,0)
        

                
        if(self.myfind_state==0):
            self.echart.setYRange(70,72.3)
            self.echart1.setYRange(5,15.5)
            self.echart2.setYRange(480,1100)
            self.echart3.setYRange(70,72)
            self.echart4.setYRange(13,13.5)
            self.echart5.setYRange(920,960)
        elif self.myfind_state==1:
            self.echart.setYRange(54,71)
            self.echart1.setYRange(5,15.2)
            self.echart2.setYRange(400,1000)
            self.echart3.setYRange(55,72)
            self.echart4.setYRange(12.5,13.5)
            self.echart5.setYRange(740,960)
        elif self.myfind_state==2:
            self.echart.setYRange(70.8,72.5)
            self.echart1.setYRange(6.5,13.2)
            self.echart2.setYRange(400,1000)
            self.echart3.setYRange(60,75)
            self.echart4.setYRange(8.4,13.8)
            self.echart5.setYRange(600,980)
        elif self.myfind_state>=3:
            self.echart.setYRange(min(self.v),max(self.v))
            self.echart1.setYRange(min(self.i),max(self.i))
            self.echart2.setYRange(min(self.p),max(self.p))
            self.echart3.setYRange(min(self.vstc),max(self.vstc))
            self.echart4.setYRange(min(self.istc),max(self.istc))
            self.echart5.setYRange(min(self.pstc),max(self.pstc))
        
        
        
        self.echart.setXRange(self.X_ptr1,self.X_ptr1+20,padding=0)
        self.echart1.setXRange(self.X_ptr1,self.X_ptr1+20,padding=0)
        self.echart2.setXRange(self.X_ptr1,self.X_ptr1+20,padding=0)
        self.echart3.setXRange(self.X_ptr1,self.X_ptr1+20,padding=0)
        self.echart4.setXRange(self.X_ptr1,self.X_ptr1+20,padding=0)
        self.echart5.setXRange(self.X_ptr1,self.X_ptr1+20,padding=0)
        
        self.DATA[:-1] = self.DATA[1:]#将列表中的数左移一位
        self.DATA1[:-1] = self.DATA1[1:]#将列表中的数左移一位
        self.DATA2[:-1] = self.DATA2[1:]#将列表中的数左移一位

      
        self.DATA[-1]=self.v[self.index]
        self.DATA1[-1]=self.i[self.index]
        self.DATA2[-1] = self.p[self.index]
        
        
        self.DATA_1[:-1] = self.DATA_1[1:]#将列表中的数左移一位
        self.DATA1_1[:-1] = self.DATA1_1[1:]#将列表中的数左移一位
        self.DATA2_1[:-1] = self.DATA2_1[1:]#将列表中的数左移一位

      
        self.DATA_1[-1]=self.vstc[self.index]
        self.DATA1_1[-1]=self.istc[self.index]
        self.DATA2_1[-1] = self.pstc[self.index]        
        
        
        self.index = (self.index + 1) % len(self.v) 

        self.curve1.setData(self.DATA,)
        self.curve2.setData(self.DATA1,)
        self.curve3.setData(self.DATA2,)
        
        self.curve4.setData(self.DATA_1,)
        self.curve5.setData(self.DATA1_1,)
        self.curve6.setData(self.DATA2_1,)
        

        
        
        self.index1=(self.index1+1)%len(self.y_P_normal)
        self.y_P_normal_show=self.y_P_normal[self.index1]
        self.y_P_LL_show=self.y_p_LL[self.index1]
        self.y_P_OC_show=self.y_p_OC[self.index1]
        self.y_P_PS_show=self.y_p_PS[self.index1]
        self.LineCanvas8_update()
        self.LineCanvas9_update()
        self.LineCanvas10_update()
        self.LineCanvas11_update()
        
        
        
        






    def PrepareLineCanvas1(self):#状态统计那里的曲线图
        self.LineFigure1 = Figure_Canvas()
        self.LineFigureLayout1 = QGridLayout(self.LineDisplayGB1)
        self.LineFigureLayout1.addWidget(self.LineFigure1)
        ax1 = self.LineFigure1.ax

        ax1.set_xlabel('时间点', fontsize=16)
        # 名词列表，对应不同的 y 轴刻度值
        y_labels = ['正常', '短路', '开路', '阴影']
        y_values = [1, 2, 3, 4]  # 对应的 y 轴数值
        ax1.set_ylim(0, 5)  # 设置 y 轴范围
        ax1.set_xticks([0,5,10,15,20,25])  # 设置 x 轴刻度
        ax1.set_xticklabels(['09:45','10:00','10:15','10:30','10:45','11:00'])  # 设置 x 轴刻度
        ax1.set_yticks(y_values)  # 设置 y 轴刻度
        ax1.set_yticklabels(y_labels)  # 设置 y 轴刻度标签
        x=[]
        for i in range(0,len(self.y_pred)):
            x.append(i)
            
        
        ax1.plot(x, self.y_true, label='真实结果',marker='v')  # 绘制折线图
        ax1.plot(x, self.y_pred, label='预测结果',marker='^')  # 绘制折线图
        ax1.legend()  # 显示图例
        self.LineFigure1.draw()
        
        
        

    def PrepareLineCanvas3(self): #设置那里的图
        self.LineFigure3 = Figure_Canvas()
        self.LineFigureLayout3 = QGridLayout(self.LineDisplayGB3)
        self.LineFigureLayout3.addWidget(self.LineFigure3)
        ax3 = self.LineFigure3.ax
        labels = ['带标签数据', '无标签数据']
        first = [50, 20]
        second = [50, 20]
        third = [50, 20]
        fourth = [50, 20]
        fifth = [0, 120]
        x = np.arange(len(labels))  # x轴刻度标签位置
        width = 0.1  # 柱子的宽度
        # 计算每个柱子在x轴上的位置，保证x轴刻度标签居中
        # x - width/2，x + width/2即每组数据在x轴上的位置
        rects1 = ax3.bar(x - width*2-0.04, first, width, label='正常',color='g')
        rects2 = ax3.bar(x - width-0.02, second, width, label='短路',color='r')
        rects3 = ax3.bar(x, third, width, label='开路',color='b')
        rects4 = ax3.bar(x + width+0.02, fourth, width, label='阴影',color='y')
        rects5 = ax3.bar(x + width*2+0.04, fifth, width, label='其他阴影',color='#FF7FFF')

        ax3.set_ylabel('样本数量')

        # x轴刻度标签位置不进行计算
        ax3.set_xticks(x, labels=labels)
        ax3.legend()

        # 在柱状图上方显示数值
        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax3.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')
        autolabel(rects1)
        autolabel(rects2)
        autolabel(rects3)
        autolabel(rects4)
        autolabel(rects5)

        self.LineFigure3.draw()

        
    def PrepareLineCanvas7(self): #设置那里的图


        self.LineFigure7 = Figure_Canvas()
        self.LineFigureLayout7 = QGridLayout(self.LineDisplayGB7)
        self.LineFigureLayout7.addWidget(self.LineFigure7)
        ax7 = self.LineFigure7.ax
        ax7.plot(range(0,len(self.setup3yshow)),self.setup3yshow)
        # 设置主刻度的位置
        ax7.set_ylim(min(self.setup3yshow),max(self.setup3yshow))
        # 设置主刻度的位置
        ax7.set_xticks([290*10*i for i in range(0, int(self.true_end_date/10)-int(self.true_start_date/10))])
        
        # 设置主刻度的标签，带入主刻度旋转角度和字体大小参数
        ax7.set_xticklabels([QDate(2021, 10, 1).addDays(i*10).toString("yyyy-M-d") for i in range(int(self.true_start_date/10), int(self.true_end_date/10))],fontsize=8)
        ax7.set_ylabel('辐照度(W/(m*m))',fontsize=7)
        self.LineFigure7.draw()


    
    def PrepareLineCanvas4(self):  #饼状图
        self.DATA4=[0.25,0.25,0.25,0.25]
        self.myDATA4=[0.26,0.252,0.248,0.24]
        self.LineFigure4 = Figure_Canvas()
        self.myLineFigure4 = Figure_Canvas()
        self.LineFigureLayout4 = QGridLayout(self.LineDisplayGB4)
        self.LineFigureLayout4.addWidget(self.LineFigure4,0, 0, Qt.AlignLeft)
        self.LineFigureLayout4.addWidget(self.myLineFigure4,0, 1, Qt.AlignRight)
        ax4 = self.LineFigure4.ax

        recipe = ["正常\n"+str(self.DATA4[0]*100)+"%",
          "短路\n"+str(self.DATA4[1]*100)+"%",
          "开路\n"+str(self.DATA4[2]*100)+"%",
          "阴影\n"+str(self.DATA4[3]*100)+"%"]
        ax4.pie(self.DATA4, labels=recipe, colors=['g','r','b','y'],wedgeprops={'width': 0.5})
        ax4.axis('off')  # 去掉坐标轴
        ax4.set_title('真实结果')
        myax4=self.myLineFigure4.ax
        myrecipe = ["正常\n26%",
          "短路\n25.2%",
          "开路\n24.8%",
          "阴影\n26%"]
        myax4.pie(self.myDATA4, labels=myrecipe, colors=['g','r','b','y'],wedgeprops={'width': 0.5})
        myax4.axis('off')  # 去掉坐标轴
        myax4.set_title('预测结果')
        self.LineFigure4.draw()     
    '''
    def PrepareLineCanvas5(self):  #最后的一张图
        self.LineFigure5 = Figure_Canvas()
        self.LineFigureLayout5 = QGridLayout(self.LineDisplayGB5)
        self.LineFigureLayout5.addWidget(self.LineFigure5)
        ax5 = self.LineFigure5.ax
        colors = ['g','r','b','y']
        # 绘制折线
        x=[]
        y = df4.iloc[:, 0].values
        for i in range(0,len(self.comparsion0_label)):
            x.append(i)
        for i in range(len(self.comparsion0_label)-1):
            ax5.plot([x[i], x[i+1]], [y[i], y[i+1]], 
                    color=colors[self.comparsion0_label[i]-1], linewidth=2)
        ax5.set_ylim(min(y)-5,max(y)+5)
        self.LineFigure5.draw()
    '''
    
    def PrepareLineCanvas5(self):  #最后的一张图
        self.LineFigure5 = Figure_Canvas()
        self.LineFigureLayout5 = QGridLayout(self.LineDisplayGB5)
        self.LineFigureLayout5.addWidget(self.LineFigure5)
        ax5 = self.LineFigure5.ax
        
        labels = ['正常', '短路', '开路', '阴影']
        self.myx1=[int(self.comparsion0_normal[1]*100),int(self.comparsion0_LL[1]*100),int(self.comparsion0_OC[1]*100),int(self.comparsion0_PS[1]*100)]
        self.myx2=[int(self.comparsion1_normal[1]*100),int(self.comparsion1_LL[1]*100),int(self.comparsion1_OC[1]*100),int(self.comparsion1_PS[1]*100)]
        x = np.arange(len(labels))  # x轴刻度标签位置
        width = 0.25  # 柱子的宽度
        # 计算每个柱子在x轴上的位置，保证x轴刻度标签居中
        # x - width/2，x + width/2即每组数据在x轴上的位置
        ax5.bar(x - width/2, self.myx1, width, label='所提方法',color='blue')
        ax5.bar(x + width/2, self.myx2, width, label='对比方法',color='red')
        ax5.legend()
        ax5.set_ylabel('百分比')
        ax5.set_xticks(x,labels=labels)
        self.LineFigure5.draw()   
        self.comparsion15clicked()

        


    def PrepareLineCanvas8(self):  #饼状图

        self.LineFigure8 = Figure_Canvas()
        self.LineFigureLayout8 = QGridLayout(self.LineDisplayGB8)
        self.LineFigureLayout8.addWidget(self.LineFigure8)
        ax8 = self.LineFigure8.ax
        colors = ['mediumblue', 'slategray']
        mydata=[self.y_P_normal_show,1-self.y_P_normal_show]
        ax8.pie(mydata,colors=colors, wedgeprops={'width': 0.5})
        ax8.text(0, 0, str(int(mydata[0]*100))+'%' , ha='center', va='center', fontsize=16)
        ax8.axis('off')  # 去掉坐标轴


        self.LineFigure8.draw()   
        
    def PrepareLineCanvas9(self):  #饼状图

        self.LineFigure9 = Figure_Canvas()
        self.LineFigureLayout9 = QGridLayout(self.LineDisplayGB9)
        self.LineFigureLayout9.addWidget(self.LineFigure9)
        ax9 = self.LineFigure9.ax
        colors = ['mediumblue', 'slategray']
        mydata=[self.y_P_LL_show,1-self.y_P_LL_show]
        ax9.pie(mydata,colors=colors, wedgeprops={'width': 0.5})
        ax9.axis('off')  # 去掉坐标轴
        ax9.text(0, 0, str(int(mydata[0]*100))+'%' , ha='center', va='center', fontsize=16)

        self.LineFigure9.draw()   
        
    def PrepareLineCanvas10(self):  #饼状图

        self.LineFigure10 = Figure_Canvas()
        self.LineFigureLayout10 = QGridLayout(self.LineDisplayGB10)
        self.LineFigureLayout10.addWidget(self.LineFigure10)
        ax10 = self.LineFigure10.ax
        colors = ['mediumblue', 'slategray']
        mydata=[self.y_P_OC_show,1-self.y_P_OC_show]
        ax10.pie(mydata,colors=colors, wedgeprops={'width': 0.5})
        ax10.axis('off')  # 去掉坐标轴
        ax10.text(0, 0, str(int(mydata[0]*100))+'%' , ha='center', va='center', fontsize=16)

        self.LineFigure10.draw()   
        
    def PrepareLineCanvas11(self):  #饼状图

        self.LineFigure11 = Figure_Canvas()
        self.LineFigureLayout11 = QGridLayout(self.LineDisplayGB11)
        self.LineFigureLayout11.addWidget(self.LineFigure11)
        ax11 = self.LineFigure11.ax
        colors = ['mediumblue', 'slategray']
        mydata=[self.y_P_PS_show,1-self.y_P_PS_show]
        ax11.pie(mydata,colors=colors, wedgeprops={'width': 0.5})
        ax11.axis('off')  # 去掉坐标轴
        ax11.text(0, 0, str(int(mydata[0]*100))+'%' , ha='center', va='center', fontsize=16)

        self.LineFigure11.draw()   
    
    def PrepareLineCanvas13(self):  #设置那里的图
        self.LineFigure13 = Figure_Canvas()
        self.LineFigureLayout13 = QGridLayout(self.LineDisplayGB13)
        self.LineFigureLayout13.addWidget(self.LineFigure13)
        ax13 = self.LineFigure13.ax
        ax13.plot(range(0,len(self.setupyshow)),self.setupyshow)
        # 设置主刻度的位置
        ax13.set_ylim(min(self.setupyshow),max(self.setupyshow))
        # 设置主刻度的位置
        ax13.set_xticks([290*30*i for i in range(0, int(self.true_end_date2/30)-int(self.true_start_date2/30))])
        
        # 设置主刻度的标签，带入主刻度旋转角度和字体大小参数
        ax13.set_xticklabels([QDate(2021, 3, 1).addMonths(i).toString("yyyy-M-d") for i in range(int(self.true_start_date2/30), int(self.true_end_date2/30))],  fontsize=8)
        ax13.set_ylabel('辐照度(W/(m*m))',fontsize=7)
        self.LineFigure13.draw()
    
    def PrepareLineCanvas14(self): #设置那里的图

        ax14 = self.LineFigure14.ax
        colors = ['g','r','b','y']
        # 绘制折线
        x=[]
        for i in range(0,len(self.setup1)):
            x.append(i)
        for i in range(0,len(self.setup1)-1):
            ax14.plot([x[i], x[i+1]], [self.setupyshow1[i], self.setupyshow1[i+1]], 
                    color=colors[self.setupyshow1label[i]-1], linewidth=2)
        ax14.set_ylim(min(self.setup1)-5,max(self.setup1)+5)
        ax14.set_xticks([0, 10, 20, 30, 40])
        # 设置主刻度的标签， 带入主刻度旋转角度和字体大小参数
        ax14.set_xticklabels(['8:20', '9:10', '9:30','10:20', '11:40'], rotation=30, fontsize=12)
        ax14.set_ylabel('光伏出力(W)')

        self.LineFigure14.draw()
    
    
    
    
    def LineCanvas1_update(self):

        self.LineFigure1.clear()
        self.LineFigure1.fig.canvas.draw()  # 这里注意是画布重绘，self.figs.canvas
        self.LineFigure1.fig.canvas.flush_events()  # 画布刷新self.figs.canvas
        ax1 = self.LineFigure1.ax

        ax1.set_xlabel('时间点', fontsize=16)
        # 名词列表，对应不同的 y 轴刻度值
        y_labels = ['正常', '短路', '开路', '阴影']
        y_values = [1, 2, 3, 4]  # 对应的 y 轴数值
        ax1.set_ylim(0, 5)  # 设置 y 轴范围

        ax1.set_yticks(y_values)  # 设置 y 轴刻度
        ax1.set_yticklabels(y_labels)  # 设置 y 轴刻度标签
        x=[]
        for i in range(0,len(self.y_pred)):
            x.append(i)
            
        
        ax1.plot(x, self.y_true, label='真实结果',marker='v')  # 绘制折线图
        ax1.plot(x, self.y_pred, label='预测结果',marker='^')  # 绘制折线图
        ax1.legend()  # 显示图例
        self.LineFigure1.draw()
    
    
    
    def LineCanvas3_update(self):
        self.LineFigure3.clear()
        self.LineFigure3.fig.canvas.draw()  # 这里注意是画布重绘，self.figs.canvas
        self.LineFigure3.fig.canvas.flush_events()  # 画布刷新self.figs.canvas
        ax3 = self.LineFigure3.ax
        colors = ['g','r','b','y']
        # 绘制折线
        x=[]
        for i in range(0,len(self.setup)):
            x.append(i)
        for i in range(0,len(self.setup)-1):
            ax3.plot([x[i], x[i+1]], [self.setup[i], self.setup[i+1]], 
                    color=colors[self.setuplabel[i]-1], linewidth=2)
        ax3.set_ylim(min(self.setup)-5,max(self.setup)+5)
        ax3.set_xlabel('光伏出力(W)')
        ax3.set_ylabel('时间点')
        self.LineFigure3.draw()
        
    def LineCanvas12_update(self):
        self.LineFigure12.clear()
        self.LineFigure12.fig.canvas.draw()  # 这里注意是画布重绘，self.figs.canvas
        self.LineFigure12.fig.canvas.flush_events()  # 画布刷新self.figs.canvas
        ax12 = self.LineFigure12.ax
        colors = ['g','r','b','y']
        # 绘制折线
        x=[]
        for i in range(0,len(self.setup1)):
            x.append(i)
        for i in range(0,len(self.setup1)-1):
            ax12.plot([x[i], x[i+1]], [self.setup1[i], self.setup1[i+1]], 
                    color=colors[self.setuplabel1[i]-1], linewidth=2)
        ax12.set_ylim(min(self.setup1)-5,max(self.setup1)+5)
        ax12.set_xlabel('光伏出力(W)')
        ax12.set_ylabel('时间点')
        self.LineFigure12.draw()

        
    def LineCanvas4_update(self):
        self.LineFigure1.clear()
        self.LineFigure1.fig.canvas.draw()  # 这里注意是画布重绘，self.figs.canvas
        self.LineFigure1.fig.canvas.flush_events()  # 画布刷新self.figs.canvas
        ax1 = self.LineFigure1.ax
        x=[]
        for i in range(0,self.diff_days1):
            x.append(i)
            
        ax1.plot(x, self.random_data1, color=(0, 100/255, 0),label="原始曲线")  # 绘制折线图
        ax1.legend()
        self.LineFigure1.draw()
        
    def LineCanvas5_update(self):
        self.LineFigure5.clear()
        self.LineFigure5.fig.canvas.draw()  # 这里注意是画布重绘，self.figs.canvas
        self.LineFigure5.fig.canvas.flush_events()  # 画布刷新self.figs.canvas
        ax5 = self.LineFigure5.ax
        labels = ['正常', '短路', '开路', '阴影']

        x = np.arange(len(labels))  # x轴刻度标签位置
        width = 0.25  # 柱子的宽度
        # 计算每个柱子在x轴上的位置，保证x轴刻度标签居中
        # x - width/2，x + width/2即每组数据在x轴上的位置
        ax5.bar(x - width/2, self.myx1, width, label='所提方法',color='#003D8F')
        ax5.bar(x + width/2, self.myx2, width, label='对比方法',color='#C00000')
        ax5.legend()
        ax5.set_ylabel('百分比')
        ax5.set_xticks(x,labels=labels)
        self.LineFigure5.draw()   
        



    def LineCanvas6_update(self):
        self.LineFigure4.clear()
        self.LineFigure4.fig.canvas.draw()  # 这里注意是画布重绘，self.figs.canvas
        self.LineFigure4.fig.canvas.flush_events()  # 画布刷新self.figs.canvas
        ax4 = self.LineFigure4.ax
        recipe = ["正常\n"+str(self.DATA4[0]*100)+"%",
          "短路\n"+str(self.DATA4[1]*100)+"%",
          "开路\n"+str(self.DATA4[2]*100)+"%",
          "阴影\n"+str(self.DATA4[3]*100)+"%"]
        ax4.pie(self.DATA4, labels=recipe, wedgeprops={'width': 0.5})
        ax4.axis('off')  # 去掉坐标轴
        self.LineFigure4.draw()  

    def LineCanvas7_update(self):
        self.LineFigure7.clear()
        self.LineFigure7.fig.canvas.draw()  # 这里注意是画布重绘，self.figs.canvas
        self.LineFigure7.fig.canvas.flush_events()  # 画布刷新self.figs.canvas
        ax7 = self.LineFigure7.ax
        ax7.plot(range(0,len(self.setup3yshow)),self.setup3yshow)
        # 设置主刻度的位置
        ax7.set_ylim(min(self.setup3yshow),max(self.setup3yshow))
        # 设置主刻度的位置
        ax7.set_xticks([290*10*i for i in range(0, int(self.true_end_date/10)-int(self.true_start_date/10))])
        
        # 设置主刻度的标签，带入主刻度旋转角度和字体大小参数
        ax7.set_xticklabels([QDate(2021, 10, 1).addDays(i*10).toString("yyyy-M-d") for i in range(int(self.true_start_date/10), int(self.true_end_date/10))],  fontsize=8)
        ax7.set_ylabel('辐照度(W/(m*m))',fontsize=7)
        self.LineFigure7.draw()



    def LineCanvas8_update(self):  #饼状图

        self.LineFigure8.clear()
        self.LineFigure8.fig.canvas.draw()  # 这里注意是画布重绘，self.figs.canvas
        self.LineFigure8.fig.canvas.flush_events()  # 画布刷新self.figs.canvas
        ax8 = self.LineFigure8.ax
        colors = ['mediumblue', 'slategray']
        mydata=[self.y_P_normal_show,1-self.y_P_normal_show]
        ax8.axis('off')  # 去掉坐标轴
        ax8.pie(mydata,colors=colors, wedgeprops={'width': 0.5})
        ax8.text(0, 0, str(int(mydata[0]*100))+'%' , ha='center', va='center', fontsize=16)

        self.LineFigure8.draw()   
    
    def LineCanvas9_update(self):  #饼状图
        self.LineFigure9.clear()
        self.LineFigure9.fig.canvas.draw()  # 这里注意是画布重绘，self.figs.canvas
        self.LineFigure9.fig.canvas.flush_events()  # 画布刷新self.figs.canvas
        ax9 = self.LineFigure9.ax
        colors = ['mediumblue', 'slategray']
        mydata=[self.y_P_LL_show,1-self.y_P_LL_show]
        ax9.axis('off')  # 去掉坐标轴
        ax9.pie(mydata,colors=colors, wedgeprops={'width': 0.5})
        ax9.text(0, 0, str(int(mydata[0]*100))+'%' , ha='center', va='center', fontsize=16)

        self.LineFigure9.draw()   
    
    def LineCanvas10_update(self):  #饼状图
        self.LineFigure10.clear()
        self.LineFigure10.fig.canvas.draw()  # 这里注意是画布重绘，self.figs.canvas
        self.LineFigure10.fig.canvas.flush_events()  # 画布刷新self.figs.canvas
        ax10 = self.LineFigure10.ax
        colors = ['mediumblue', 'slategray']
        mydata=[self.y_P_OC_show,1-self.y_P_OC_show]
        ax10.axis('off')  # 去掉坐标轴
        ax10.pie(mydata,colors=colors, wedgeprops={'width': 0.5})
        ax10.text(0, 0, str(int(mydata[0]*100))+'%' , ha='center', va='center', fontsize=16)

        self.LineFigure10.draw()
    def LineCanvas11_update(self):  #饼状图
        self.LineFigure11.clear()
        self.LineFigure11.fig.canvas.draw()  # 这里注意是画布重绘，self.figs.canvas
        self.LineFigure11.fig.canvas.flush_events()  # 画布刷新self.figs.canvas
        ax11 = self.LineFigure11.ax
        colors = ['mediumblue', 'slategray']
        mydata=[self.y_P_PS_show,1-self.y_P_PS_show]
        ax11.axis('off')  # 去掉坐标轴
        ax11.pie(mydata,colors=colors, wedgeprops={'width': 0.5})
        ax11.text(0, 0, str(int(mydata[0]*100))+'%' , ha='center', va='center', fontsize=16)

        self.LineFigure11.draw()

    def LineCanvas13_update(self):
        self.LineFigure13.clear()
        self.LineFigure13.fig.canvas.draw()  # 这里注意是画布重绘，self.figs.canvas
        self.LineFigure13.fig.canvas.flush_events()  # 画布刷新self.figs.canvas
        ax13 = self.LineFigure13.ax

        ax13.plot(range(0,len(self.setupyshow)),self.setupyshow)
        
        ax13.set_ylim(min(self.setupyshow),max(self.setupyshow))
        
        # 设置主刻度的位置
        ax13.set_xticks([290*30*i for i in range(0, int(self.true_end_date2/30)-int(self.true_start_date2/30))])
        
        # 设置主刻度的标签，带入主刻度旋转角度和字体大小参数
        ax13.set_xticklabels([QDate(2021, 3, 1).addMonths(i).toString("yyyy-M-d") for i in range(int(self.true_start_date2/30), int(self.true_end_date2/30))],  fontsize=8)
        ax13.set_ylabel('辐照度(W/(m*m))',fontsize=7)
        self.LineFigure13.draw()
        

    def LineCanvas14_update(self):
        self.LineFigure14.clear()
        self.LineFigure14.fig.canvas.draw()  # 这里注意是画布重绘，self.figs.canvas
        self.LineFigure14.fig.canvas.flush_events()  # 画布刷新self.figs.canvas
        ax14 = self.LineFigure14.ax
        colors = ['g','r','b','y']
        # 绘制折线
        x=[]
        for i in range(0,len(self.setup1)):
            x.append(i)
        for i in range(0,len(self.setup1)-1):
            ax14.plot([x[i], x[i+1]], [self.setupyshow1[i], self.setupyshow1[i+1]], 
                    color=colors[self.setupyshow1label[i]-1], linewidth=2)
        ax14.set_ylim(min(self.setup1)-5,max(self.setup1)+5)
        ax14.set_xticks([0, 10, 20, 30, 40])
        # 设置主刻度的标签， 带入主刻度旋转角度和字体大小参数
        ax14.set_xticklabels(['8:20', '9:10', '9:30','10:20', '11:40'], rotation=30, fontsize=12)
        ax14.set_ylabel('光伏出力(W)')

        self.LineFigure14.draw()
        
    def calculateDays(self):#设置那里的图更新
        self.start_date = self.station_id2_datebox_2.date()
        self.end_date= self.station_id2_datebox1_2.date()
        self.true_start_date = -self.start_date.daysTo(QDate(2021, 10, 1))
        self.true_end_date = -self.end_date.daysTo(QDate(2021, 10, 1))
        self.PrepareSamples7()
        self.LineCanvas7_update()   
        
   
    def tempcalculateDays(self):#设置那里的图更新
        self.start_date2 = self.station_id2_dateboxtemp.date()
        self.end_date2= self.station_id2_dateboxtemp1.date()
        self.true_start_date2 = -self.start_date2.daysTo(QDate(2021, 3, 1))
        self.true_end_date2 = -self.end_date2.daysTo(QDate(2021, 3, 1))

        self.PrepareSamples13()
        self.LineCanvas13_update()    
        
    def fuckyou_clicked(self):#设置那里的图更新
        self.setWindowModality(Qt.ApplicationModal)	# 设置主窗口不可操作
        self.fuckme=myLoadingProgress(self)
        self.readyornot[self.find_state]=1
        self.setWindowModality(Qt.NonModal)	# 恢复正常模式
        self.PrepareLineCanvas14()
        







 
        
 

      
    def on_button_clicked5(self):
 
        if self.comparsion5_button.checked==True:
                self.myflag1=float(1)
        else:
            self.myflag1=float(0)
        self.PrepareSamples4()
        self.comparsion19_text_0.setText(str(int(self.comparsion0_normal[1]*100))+"%")
        self.comparsion19_text_2.setText(str(int(self.comparsion1_normal[1]*100))+"%")
        self.comparsion20_text_0.setText(str(int(self.comparsion0_LL[1]*100))+"%")
        self.comparsion20_text_2.setText(str(int(self.comparsion1_LL[1]*100))+"%")
        self.comparsion21_text_0.setText(str(int(self.comparsion0_OC[1]*100))+"%")
        self.comparsion21_text_2.setText(str(int(self.comparsion1_OC[1]*100))+"%")
        self.comparsion22_text_0.setText(str(int(self.comparsion0_PS[1]*100))+"%")
        self.comparsion22_text_2.setText(str(int(self.comparsion1_PS[1]*100))+"%")
        self.myx1=[int(self.comparsion0_normal[self.nowflag]*100),int(self.comparsion0_LL[self.nowflag]*100),int(self.comparsion0_OC[self.nowflag]*100),int(self.comparsion0_PS[self.nowflag]*100)]
        self.myx2=[int(self.comparsion1_normal[self.nowflag]*100),int(self.comparsion1_LL[self.nowflag]*100),int(self.comparsion1_OC[self.nowflag]*100),int(self.comparsion1_PS[self.nowflag]*100)] 
        self.LineCanvas5_update()
        

    def on_button_clicked6(self):

        if self.comparsion6_button.checked==True:
            self.myflag2=float(1)
        else:
            self.myflag2=float(0)
        self.PrepareSamples4()      
        self.comparsion19_text_0.setText(str(int(self.comparsion0_normal[1]*100))+"%")
        self.comparsion19_text_2.setText(str(int(self.comparsion1_normal[1]*100))+"%")
        self.comparsion20_text_0.setText(str(int(self.comparsion0_LL[1]*100))+"%")
        self.comparsion20_text_2.setText(str(int(self.comparsion1_LL[1]*100))+"%")
        self.comparsion21_text_0.setText(str(int(self.comparsion0_OC[1]*100))+"%")
        self.comparsion21_text_2.setText(str(int(self.comparsion1_OC[1]*100))+"%")
        self.comparsion22_text_0.setText(str(int(self.comparsion0_PS[1]*100))+"%")
        self.comparsion22_text_2.setText(str(int(self.comparsion1_PS[1]*100))+"%")
        self.myx1=[int(self.comparsion0_normal[self.nowflag]*100),int(self.comparsion0_LL[self.nowflag]*100),int(self.comparsion0_OC[self.nowflag]*100),int(self.comparsion0_PS[self.nowflag]*100)]
        self.myx2=[int(self.comparsion1_normal[self.nowflag]*100),int(self.comparsion1_LL[self.nowflag]*100),int(self.comparsion1_OC[self.nowflag]*100),int(self.comparsion1_PS[self.nowflag]*100)] 
        self.LineCanvas5_update()

    def on_button_clicked7(self):

        if self.comparsion7_button.checked==True:
            self.myflag3=float(1)
        else:
            self.myflag3=float(0)
        self.PrepareSamples4()
        self.comparsion19_text_0.setText(str(int(self.comparsion0_normal[1]*100))+"%")
        self.comparsion19_text_2.setText(str(int(self.comparsion1_normal[1]*100))+"%")
        self.comparsion20_text_0.setText(str(int(self.comparsion0_LL[1]*100))+"%")
        self.comparsion20_text_2.setText(str(int(self.comparsion1_LL[1]*100))+"%")
        self.comparsion21_text_0.setText(str(int(self.comparsion0_OC[1]*100))+"%")
        self.comparsion21_text_2.setText(str(int(self.comparsion1_OC[1]*100))+"%")
        self.comparsion22_text_0.setText(str(int(self.comparsion0_PS[1]*100))+"%")
        self.comparsion22_text_2.setText(str(int(self.comparsion1_PS[1]*100))+"%")
        self.myx1=[int(self.comparsion0_normal[self.nowflag]*100),int(self.comparsion0_LL[self.nowflag]*100),int(self.comparsion0_OC[self.nowflag]*100),int(self.comparsion0_PS[self.nowflag]*100)]
        self.myx2=[int(self.comparsion1_normal[self.nowflag]*100),int(self.comparsion1_LL[self.nowflag]*100),int(self.comparsion1_OC[self.nowflag]*100),int(self.comparsion1_PS[self.nowflag]*100)] 
        self.LineCanvas5_update()


    def comparsion15clicked(self):
        self.comparsion19_text_0.setText(str(int(self.comparsion0_normal[1]*100))+"%")
        self.comparsion19_text_2.setText(str(int(self.comparsion1_normal[1]*100))+"%")
        self.comparsion20_text_0.setText(str(int(self.comparsion0_LL[1]*100))+"%")
        self.comparsion20_text_2.setText(str(int(self.comparsion1_LL[1]*100))+"%")
        self.comparsion21_text_0.setText(str(int(self.comparsion0_OC[1]*100))+"%")
        self.comparsion21_text_2.setText(str(int(self.comparsion1_OC[1]*100))+"%")
        self.comparsion22_text_0.setText(str(int(self.comparsion0_PS[1]*100))+"%")
        self.comparsion22_text_2.setText(str(int(self.comparsion1_PS[1]*100))+"%")
        self.myx1=[int(self.comparsion0_normal[1]*100),int(self.comparsion0_LL[1]*100),int(self.comparsion0_OC[1]*100),int(self.comparsion0_PS[1]*100)]
        self.myx2=[int(self.comparsion1_normal[1]*100),int(self.comparsion1_LL[1]*100),int(self.comparsion1_OC[1]*100),int(self.comparsion1_PS[1]*100)] 
        self.nowflag=1
        self.LineCanvas5_update()
    def comparsion16clicked(self):
        self.comparsion19_text_0.setText(str(int(self.comparsion0_normal[2]*100))+"%")
        self.comparsion19_text_2.setText(str(int(self.comparsion1_normal[2]*100))+"%")
        self.comparsion20_text_0.setText(str(int(self.comparsion0_LL[2]*100))+"%")
        self.comparsion20_text_2.setText(str(int(self.comparsion1_LL[2]*100))+"%")
        self.comparsion21_text_0.setText(str(int(self.comparsion0_OC[2]*100))+"%")
        self.comparsion21_text_2.setText(str(int(self.comparsion1_OC[2]*100))+"%")
        self.comparsion22_text_0.setText(str(int(self.comparsion0_PS[2]*100))+"%")
        self.comparsion22_text_2.setText(str(int(self.comparsion1_PS[2]*100))+"%")
        self.myx1=[int(self.comparsion0_normal[2]*100),int(self.comparsion0_LL[2]*100),int(self.comparsion0_OC[2]*100),int(self.comparsion0_PS[2]*100)]
        self.myx2=[int(self.comparsion1_normal[2]*100),int(self.comparsion1_LL[2]*100),int(self.comparsion1_OC[2]*100),int(self.comparsion1_PS[2]*100)] 
        self.nowflag=2
        self.LineCanvas5_update()   
    def comparsion17clicked(self):
        self.comparsion19_text_0.setText(str(int(self.comparsion0_normal[3]*100))+"%")
        self.comparsion19_text_2.setText(str(int(self.comparsion1_normal[3]*100))+"%")
        self.comparsion20_text_0.setText(str(int(self.comparsion0_LL[3]*100))+"%")
        self.comparsion20_text_2.setText(str(int(self.comparsion1_LL[3]*100))+"%")
        self.comparsion21_text_0.setText(str(int(self.comparsion0_OC[3]*100))+"%")
        self.comparsion21_text_2.setText(str(int(self.comparsion1_OC[3]*100))+"%")
        self.comparsion22_text_0.setText(str(int(self.comparsion0_PS[3]*100))+"%")
        self.comparsion22_text_2.setText(str(int(self.comparsion1_PS[3]*100))+"%")
        self.myx1=[int(self.comparsion0_normal[3]*100),int(self.comparsion0_LL[3]*100),int(self.comparsion0_OC[3]*100),int(self.comparsion0_PS[3]*100)]
        self.myx2=[int(self.comparsion1_normal[3]*100),int(self.comparsion1_LL[3]*100),int(self.comparsion1_OC[3]*100),int(self.comparsion1_PS[3]*100)] 
        self.nowflag=3
        self.LineCanvas5_update()    
    def comparsion18clicked(self):
        self.comparsion19_text_0.setText(str(int(self.comparsion0_normal[4]*100))+"%")
        self.comparsion19_text_2.setText(str(int(self.comparsion1_normal[4]*100))+"%")
        self.comparsion20_text_0.setText(str(int(self.comparsion0_LL[4]*100))+"%")
        self.comparsion20_text_2.setText(str(int(self.comparsion1_LL[4]*100))+"%")
        self.comparsion21_text_0.setText(str(int(self.comparsion0_OC[4]*100))+"%")
        self.comparsion21_text_2.setText(str(int(self.comparsion1_OC[4]*100))+"%")
        self.comparsion22_text_0.setText(str(int(self.comparsion0_PS[4]*100))+"%")
        self.comparsion22_text_2.setText(str(int(self.comparsion1_PS[4]*100))+"%")
        self.myx1=[int(self.comparsion0_normal[4]*100),int(self.comparsion0_LL[4]*100),int(self.comparsion0_OC[4]*100),int(self.comparsion0_PS[4]*100)]
        self.myx2=[int(self.comparsion1_normal[4]*100),int(self.comparsion1_LL[4]*100),int(self.comparsion1_OC[4]*100),int(self.comparsion1_PS[4]*100)] 
        self.nowflag=4   
        self.LineCanvas5_update()

def auto_resize(QMainWindow):
        # 获取窗口原来大小
        window_width = QMainWindow.width()
        window_height = QMainWindow.height()
        # 获取屏幕大小
        screen = QDesktopWidget().screenGeometry()
        screen_width = screen.width()
        screen_height = screen.height()
        # 自定义新窗口大小
        new_window_width = int(screen_width * 0.7)
        resize_rate = new_window_width / window_width  # 确定放大比例
        new_window_height = int(window_height * resize_rate)  # 确定新窗口高度
        # 重新调整窗口大小并移动到屏幕中心
        QMainWindow.resize(new_window_width, new_window_height)
        QMainWindow.move((screen_width - new_window_width) // 2, (screen_height - new_window_height) // 3)
        # 重新调整子控件位置大小
        for widget in QMainWindow.findChildren(QWidget):
            rect = widget.geometry()
            widget.setGeometry(QtCore.QRect(
                int(rect.x() * resize_rate),
                int(rect.y() * resize_rate),
                int(rect.width() * resize_rate),
                int(rect.height() * resize_rate),
            ))




if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui=ImgDisp()
    auto_resize(ui)
    ui.show()
    sys.exit(app.exec_())
'''
    ui = untitled.Ui_MainWindow()
    ui.setupUi(MainWindow)
    auto_resize(MainWindow)
    MainWindow.show()
'''



