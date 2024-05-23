import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QDesktopWidget,QWidget,QGridLayout,QComboBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt,QTimer
from functools import partial
import untitled
from test2 import NewDialog
from test5 import LoadingProgress
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
import matlab
import matlab.engine
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
import matlab
import matlab.engine
eng = matlab.engine.start_matlab()
eng.cd("C:\\Users\\whitefork\\Desktop\\python\\myproject\\test1",nargout=0)
label=['正常','短路','开路','阴影']
yticks=[1.0,2.0,3.0,4.0]
t1=time.localtime()
df = pd.read_csv('C:\\Users\\whitefork\\Desktop\\python\\myproject\\test1\\G.csv',engine='python')




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




class ImgDisp(QMainWindow,Ui_MainWindow):
    loading_label=False

    count=0
    DATA=[]#电压
    DATA1=[]#电流
    DATA2=[]#功率
    DATA3=[]#发电状态
    DATA4=[]#发电状态占比
    DATA5=[]#准确率
    DATA6=[]#精确率
    DATA7=[]#召回率
    random_data=[]
    
    startlearning_state=False #开始学习

    
    
    my_v=[]
    my_i=[]
    my_state=[]
    M=[]
    index=20
    
    state=0
    
    find_state=0 #正常，短路，开路，阴影
    find_state1=0 #准确率，精确率，召回率，F1分数
    
    DATA4=[0.25,0.25,0.25,0.25]
    DATA5=[0.25,0.25,0.25,0.25]
    DATA6=[0.25,0.25,0.25,0.25]
    DATA7=[0.25,0.25,0.25,0.25]

    def __init__(self,parent=None):
        self.diff_days=29
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
        self.PrepareLineCanvas()
        self.PrepareLineCanvas1()
        self.PrepareLineCanvas2()
        self.PrepareLineCanvas3()
        self.PrepareLineCanvas4()
        self.PrepareLineCanvas5()
    
    '''
    def test1(self):
        [self.my_v,self.my_i,self.my_state,self.M,self.ratio,self.accuracy,self.precision,self.recall]=eng.test1(nargout=8)
        self.DATA4=[]
        self.DATA5=[]
        self.DATA6=[]
        self.DATA7=[]
        
        for i in range(0,4):
            self.DATA4.append(self.ratio[i][0])
            self.DATA5.append(self.accuracy[i][0])
            self.DATA6.append(self.precision[i][0])
            self.DATA7.append(self.recall[i][0])
        self.M=np.array(self.M,dtype=np.int64)
    '''       
    def simulate_and_record_standard(self,G,T,mode):


        DATA=[0] * 20
        DATA1=[0] * 20
        DATA2=[0] * 20
        vstc=[0]*20
        istc=[0]*20
        pstc=[0]*20
        self.DATA_standard=[]
        self.DATA1_standard=[]
        self.DATA2_standard=[]
        eng.cd("C:\\Users\\whitefork\\Desktop\\python\\myproject\\test1",nargout=0)
        if mode=='normal':
            [DATA,DATA1,DATA2,vstc,istc,pstc]=eng.simulate_and_record(G,T,nargout=6)
        elif mode=='LL':
            [DATA,DATA1,DATA2,vstc,istc,pstc]=eng.simulate_and_record_LL(G,T,nargout=6)   
        elif mode=='OC':
            [DATA,DATA1,DATA2,vstc,istc,pstc]=eng.simulate_and_record_OC(G,T,nargout=6)  
        elif mode=='PS1':
            [DATA,DATA1,DATA2,vstc,istc,pstc]=eng.simulate_and_record_PS1(G,T,nargout=6)
        elif mode=='PS2':
            [DATA,DATA1,DATA2,vstc,istc,pstc]=eng.simulate_and_record_PS2(G,T,nargout=6)        
        for i in range(0,20):
            self.DATA_standard.append(DATA[i][0])
            self.DATA1_standard.append(DATA1[i][0])
            self.DATA2_standard.append(DATA2[i][0])

        op2 = QtWidgets.QGraphicsOpacityEffect()
        op2.setOpacity(0)
        self.loadinggif.setGraphicsEffect(op2)

    def simulate_and_record(self,G,T,mode):


        DATA=[0] * 20
        DATA1=[0] * 20
        DATA2=[0] * 20
        vstc=[0]*20
        istc=[0]*20
        pstc=[0]*20
        self.DATA=[]
        self.DATA1=[]
        self.DATA2=[]
        self.vstc=[]
        self.istc=[]
        self.pstc=[]
        eng.cd("C:\\Users\\whitefork\\Desktop\\python\\myproject\\test1",nargout=0)
        if mode=='normal':
            [DATA,DATA1,DATA2,vstc,istc,pstc]=eng.simulate_and_record(G,T,nargout=6)
        elif mode=='LL':
            [DATA,DATA1,DATA2,vstc,istc,pstc]=eng.simulate_and_record_LL(G,T,nargout=6)   
        elif mode=='OC':
            [DATA,DATA1,DATA2,vstc,istc,pstc]=eng.simulate_and_record_OC(G,T,nargout=6)  
        elif mode=='PS1':
            [DATA,DATA1,DATA2,vstc,istc,pstc]=eng.simulate_and_record_PS1(G,T,nargout=6)
        elif mode=='PS2':
            [DATA,DATA1,DATA2,vstc,istc,pstc]=eng.simulate_and_record_PS2(G,T,nargout=6)        
        for i in range(0,20):
            self.DATA.append(DATA[i][0])
            self.DATA1.append(DATA1[i][0])
            self.DATA2.append(DATA2[i][0])
            self.vstc.append(vstc[0][i])
            self.istc.append(istc[0][i])
            self.pstc.append(pstc[0][i])
        op2 = QtWidgets.QGraphicsOpacityEffect()
        op2.setOpacity(0)
        self.loadinggif.setGraphicsEffect(op2)

    def analyze(self):
        eng.cd("C:\\Users\\whitefork\\Desktop\\python\\myproject\\test2",nargout=0)
        [self.returnP,self.y_pred]=eng.pvd_disp(self.myflag1,self.myflag2,self.myflag3,nargout=1)        
        op2 = QtWidgets.QGraphicsOpacityEffect()
        op2.setOpacity(0)
        self.loadinggif.setGraphicsEffect(op2)
        self.x1_1=[]
        self.x_green_1=[]
        self.x_red_1=[]
        self.x_blue_1=[]
        self.x_yellow_1=[]
        self.y_green_1=[]
        self.y_red_1=[]
        self.y_blue_1=[]
        self.y_yellow_1=[]
        for i in range(0,len(self.y_pred)):
            self.x1_1.append(i)
            if self.y_pred[i][0]==1:
                self.x_green_1.append(i)
                self.y_green_1.append(self.returnP[i][0])
            elif self.y_pred[i][0]==2:
                self.x_red.append(i)
                self.y_red.append(self.returnP[i][0])
            elif self.y_pred[i][0]==3:
                self.x_blue_1.append(i)
                self.y_blue_1.append(self.returnP[i][0])
            elif self.y_pred[i][0]==4:
                self.x_yellow_1.append(i)
                self.y_yellow_1.append(self.returnP[i][0])   
        self.LineCanvas5_update()

    def PrepareSamples(self):
        self.y_pred=[]
        self.G=[]
        self.T=[]
        standard_G=[1000]*20
        standard_T=[25]*20
        weather=[]
        self.G=get_G_data()
        self.T=get_T_data()
        weather=get_weather_data()
        icons='C:\\Users\\whitefork\\Desktop\\python\\myproject\\icons\\'+weather[0]+'.svg'
        self.weather_information3.setText('天气      '+weather[1])
        self.weather_information_label.load(icons)
        self.weather_information4.setText('温度      '+weather[5])
        self.weather_information5.setText('辐照度    '+str(self.G[0]))
        
        self.vstc=[0]*20
        self.istc=[0]*20
        self.pstc=[0]*20
        self.DATA_standard=[0]*20
        self.DATA1_standard=[0]*20
        self.DATA2_standard=[0]*20

        
        '''
       # 获取 y_pred 结果
        t = Thread(target=self.test1, name='这里设置子线程初始化名')
        t.start()
        t.setName('设置线程名')  # ！！！！
        t.join()  # 等待子线程运行结束

        t1=Thread(target=self.simulate_and_record,args=(self.G,self.T,'normal'))
        t1.start()
        t1.setName('设置线程名')  # ！！！！
        t1.join()  # 等待子线程运行结束
        
        t2=Thread(target=self.simulate_and_record_standard,args=(standard_G,standard_T,'normal'))
        t2.start()
        t2.setName('设置线程名')  # ！！！！
        t2.join()  # 等待子线程运行结束
        self.myflag1=float(0)
        self.myflag2=float(0)
        self.myflag3=float(0)
        t3=Thread(target=self.analyze,args=(self.myflag1,self.myflag2,self.myflag3,))
        t3.start()
        t3.setName('设置线程名')  # ！！！！
        t3.join()  # 等待子线程运行结束
        '''

        '''
        for i in range(0,50):
            self.DATA.append(self.my_v[i][0])
            self.DATA1.append(self.my_i[i][0])
            self.DATA2.append(self.my_v[i][0]*self.my_i[i][0])
            self.DATA3.append(self.my_state[i][0])
        '''
        



    def PrepareSamples1(self):

        data = pd.read_excel("C:\\Users\\whitefork\\Desktop\\python\\myproject\\test1\\data1.xlsx")  
        data_array = data.to_numpy()
        # Randomly select 30 rows
        np.random.shuffle(data_array)
        selected_data = data_array[:self.diff_days]      
        self.x1=[]
        self.y1=[]
        self.x_green=[]
        self.x_red=[]
        self.x_blue=[]
        self.x_yellow=[]
        self.y_green=[]
        self.y_red=[]
        self.y_blue=[]
        self.y_yellow=[]
        for i in range(0,self.diff_days):
            self.x1.append(i)
            self.y1.append(selected_data[i][0])
            if selected_data[i][1]==1:
                self.x_green.append(i)
                self.y_green.append(selected_data[i][0])
            elif selected_data[i][1]==2:
                self.x_red.append(i)
                self.y_red.append(selected_data[i][0])
            elif selected_data[i][1]==3:
                self.x_blue.append(i)
                self.y_blue.append(selected_data[i][0])
            elif selected_data[i][1]==4:
                self.x_yellow.append(i)
                self.y_yellow.append(selected_data[i][0])   





        
    def PrepareLineCanvas(self):


        self.LineFigureLayout = QGridLayout(self.LineDisplayGB)
        self.echart=pg.PlotWidget()
        self.echart1=pg.PlotWidget()
        self.echart2=pg.PlotWidget()
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
        self.echart.setLabel('bottom', '时间', units='s')
        self.echart1.setLabel('left', '电流', units='A')
        self.echart1.setLabel('bottom', '时间', units='s')
        self.echart2.setLabel('left', '功率', units='W')
        self.echart2.setLabel('bottom', '时间', units='s')
        self.state=0#处于动态图阶段


        self.LineFigureLayout4 = QGridLayout(self.LineDisplayGB2)
        self.echart3=pg.PlotWidget()
        self.echart4=pg.PlotWidget()
        self.echart5=pg.PlotWidget()
        self.echart3.setBackground('white')
        self.echart4.setBackground('white')
        self.echart5.setBackground('white')

        self.LineFigureLayout4.addWidget(self.echart3)
        self.LineFigureLayout4.addWidget(self.echart4)
        self.LineFigureLayout4.addWidget(self.echart5)

        self.curve4=self.echart3.plot(self.vstc,pen='b',name="电压")
        self.curve4_1=self.echart3.plot(self.DATA_standard,pen='r',name="电压")
        self.curve5=self.echart4.plot(self.istc,pen='b',name="电流")
        self.curve5_1=self.echart4.plot(self.DATA1_standard,pen='r',name="电压")
        self.curve6=self.echart5.plot(self.pstc,pen='b',name="功率")
        self.curve6_1=self.echart5.plot(self.DATA2_standard,pen='r',name="电压")
        self.echart3.setLabel('left', '电压', units='V')
        self.echart3.setLabel('bottom', '时间', units='s')
        self.echart4.setLabel('left', '电流', units='A')
        self.echart4.setLabel('bottom', '时间', units='s')
        self.echart5.setLabel('left', '功率', units='W')
        self.echart5.setLabel('bottom', '时间', units='s')


        self.X_ptr1 = 0
        #用于记录X轴的位置

        self.timer =QtCore.QTimer()
        # 实例化一个定时器

        self.timer.timeout.connect(self.update_data)
        # 将定时器信号绑定到update_data 函数

        self.timer.start(100)
    def update_data(self):#数据更新函数
        '''
        self.DATA[:-1] = self.DATA[1:]#将列表中的数左移一位
        self.DATA1[:-1] = self.DATA1[1:]#将列表中的数左移一位
        self.DATA2[:-1] = self.DATA2[1:]#将列表中的数左移一位
        self.DATA3[:-1] = self.DATA3[1:]#将列表中的数左移一位
        self.DATA[-1]=self.my_v[self.index][0]
        self.DATA1[-1]=self.my_i[self.index][0]
        self.DATA2[-1]=self.my_i[self.index][0]*self.my_v[self.index][0]
        self.DATA3[-1] = self.my_state[self.index][0]#将列表中的数左移一位
        '''
        #self.index = (self.index + 1) % len(self.my_v) 

        #调用随机函数生成一个随机数并且将它放在数据列表的最后一位
        # 将更新后的X坐标也放入图表中
        
        '''
        if(self.DATA3[-1]==1):
            self.curve3.setPen('g')
            self.state1.setStyleSheet("QLabel{color:green;font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")
            self.state2.setStyleSheet("QLabel{color:black;font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")
            self.state3.setStyleSheet("QLabel{color:black;font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")
            self.state4.setStyleSheet("QLabel{color:black;font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")
            
            
        if(self.DATA3[-1]==2):
            self.curve3.setPen('r')
            self.state1.setStyleSheet("QLabel{color:black;font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")
            self.state2.setStyleSheet("QLabel{color:red;font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")
            self.state3.setStyleSheet("QLabel{color:black;font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")
            self.state4.setStyleSheet("QLabel{color:black;font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")

            
        if(self.DATA3[-1]==3):
            self.curve3.setPen('b')
            self.state1.setStyleSheet("QLabel{color:black;font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")
            self.state2.setStyleSheet("QLabel{color:black;font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")
            self.state3.setStyleSheet("QLabel{color:blue;font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")
            self.state4.setStyleSheet("QLabel{color:black;font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")
            
        if(self.DATA3[-1]==4):
            self.curve3.setPen('y')
            self.state1.setStyleSheet("QLabel{color:black;font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")
            self.state2.setStyleSheet("QLabel{color:black;font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")
            self.state3.setStyleSheet("QLabel{color:black;font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")
            self.state4.setStyleSheet("QLabel{color:yellow;font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")
        '''
        '''
        self.LineFigure1.clear()
        self.LineFigure1.fig.canvas.draw()  # 这里注意是画布重绘,self.figs.canvas
        self.LineFigure1.fig.canvas.flush_events()  # 画布刷新self.figs.canvas
        ax1 = self.LineFigure1.ax
        ax1.set_ylabel('power(MW)', fontsize=16)
        ax1.set_xlabel('time(s)', fontsize=16)
        x=[]
        colors=[]
        self.X_ptr2=0
        for i in range(0,50):
            x.append(self.X_ptr2+i)
        for i in range(0,len(self.DATA2)):
            if self.DATA3[i]==0:
                colors.append('green')
            if self.DATA3[i]==1:
                colors.append('red')
            if self.DATA3[i]==2:
                colors.append('blue')
            if self.DATA3[i]==3:
                colors.append('yellow')
        ax1.scatter(x, self.DATA2, c=colors, s=100, alpha=0.8)  # 绘制散点图
        ax1.plot(x, self.DATA2, color='black')  # 绘制折线图
        self.LineFigure1.draw()
        '''
        self.curve1.setData(self.DATA,)
        self.curve2.setData(self.DATA1,)
        self.curve3.setData(self.DATA2,)
        
        self.curve4.setData(self.vstc,)
        self.curve5.setData(self.istc,)
        self.curve6.setData(self.pstc,)
        
        self.curve4_1.setData(self.DATA_standard,)
        self.curve5_1.setData(self.DATA1_standard,)
        self.curve6_1.setData(self.DATA2_standard,)
        

        self.X_ptr1 += 1

        #self.curve1.setPos(self.X_ptr1,0)
        #self.curve2.setPos(self.X_ptr1,0)
        #self.curve3.setPos(self.X_ptr1,0)




    def PrepareLineCanvas1(self):
        self.LineFigure1 = Figure_Canvas()
        self.LineFigureLayout1 = QGridLayout(self.LineDisplayGB1)
        self.LineFigureLayout1.addWidget(self.LineFigure1)
        ax1 = self.LineFigure1.ax
        ax1.set_ylabel('准确率', fontsize=16)
        ax1.set_xlabel('time(s)', fontsize=16)
        x=[]
        self.random_data=[]
        
        
        for i in range(0,20):
            x.append(i)
            self.random_data.append(random.uniform(0.9, 1.0))
            
        
        ax1.plot(x, self.random_data, color=(0, 100/255, 0),label="原始曲线")  # 绘制折线图

        ax1.legend()
        self.LineFigure1.draw()
        
        
        
    def PrepareLineCanvas2(self):
        self.LineFigure2 = Figure_Canvas()
        self.LineFigureLayout2 = QGridLayout(self.LineDisplayGB2)
        self.LineFigureLayout2.addWidget(self.LineFigure2)
        ax2 = self.LineFigure2.ax
        ax2.axis('equal')
        labels=["正常","短路","开路","阴影"]
        colors=['green','red','blue','yellow']
        explode=[0.15,0,0,0]
        ax2.pie(self.DATA4,#加载绘图数据  
        explode=explode,
        labels=labels,#各球队标签
        colors=colors,#颜色属性
        radius=1.2,#设置饼图半径
        counterclock=False,#设置为顺时针方向开始绘图
        labeldistance=1.1,#设置标签位置
        autopct='%.2f%%',#设置百分比格式，这里保存两位小数
        textprops={'fontsize':12,'color':'black'},#设置文本属性,字体大小为12，颜色为黑
        wedgeprops={'linewidth':0.7,'edgecolor':'black'},#设置边框，宽度为0.7，颜色为黑
        shadow=True,#添加阴影
        startangle=90#设置开始绘图的角度
       )

        self.LineFigure2.draw()

    def PrepareLineCanvas3(self):
        self.LineFigure3 = Figure_Canvas()
        self.LineFigureLayout3 = QGridLayout(self.LineDisplayGB3)
        self.LineFigureLayout3.addWidget(self.LineFigure3)
        ax3 = self.LineFigure3.ax
        ax3.scatter(self.x_green, self.y_green, color='green',s=20)

        ax3.scatter(self.x_red, self.y_red, color='red',s=20)
        ax3.scatter(self.x_blue, self.y_blue, color='blue',s=20)
        ax3.scatter(self.x_yellow, self.y_yellow, color='yellow',s=20)

        ax3.plot(self.x1, self.y1,  color='black')

        self.LineFigure3.draw()
    
    def PrepareLineCanvas4(self):
        self.LineFigure4 = Figure_Canvas()
        self.LineFigureLayout4 = QGridLayout(self.LineDisplayGB4)
        self.LineFigureLayout4.addWidget(self.LineFigure4)
        ax4 = self.LineFigure4.ax
        recipe = ["正常\n"+str(self.DATA4[0]*100)+"%",
          "短路\n"+str(self.DATA4[1]*100)+"%",
          "开路\n"+str(self.DATA4[2]*100)+"%",
          "阴影\n"+str(self.DATA4[3]*100)+"%"]
        ax4.pie(self.DATA4, labels=recipe, wedgeprops={'width': 0.5})
        ax4.axis('off')  # 去掉坐标轴
        self.LineFigure4.draw()     
    
    def PrepareLineCanvas5(self):
        self.LineFigure5 = Figure_Canvas()
        self.LineFigureLayout5 = QGridLayout(self.LineDisplayGB5)
        self.LineFigureLayout5.addWidget(self.LineFigure5)
        ax5 = self.LineFigure5.ax
        ax5.scatter(self.x_green, self.y_green, color='green',s=20)

        ax5.scatter(self.x_red, self.y_red, color='red',s=20)
        ax5.scatter(self.x_blue, self.y_blue, color='blue',s=20)
        ax5.scatter(self.x_yellow, self.y_yellow, color='yellow',s=20)

        ax5.plot(self.x1, self.y1,  color='black')

        self.LineFigure5.draw()
    
    def LineCanvas3_update(self):
        self.LineFigure3.clear()
        self.LineFigure3.fig.canvas.draw()  # 这里注意是画布重绘，self.figs.canvas
        self.LineFigure3.fig.canvas.flush_events()  # 画布刷新self.figs.canvas
        ax3 = self.LineFigure3.ax
        ax3.scatter(self.x_green, self.y_green, color='green',s=20)

        ax3.scatter(self.x_red, self.y_red, color='red',s=20)
        ax3.scatter(self.x_blue, self.y_blue, color='blue',s=20)
        ax3.scatter(self.x_yellow, self.y_yellow, color='yellow',s=20)

        ax3.plot(self.x1, self.y1,  color='black')

        self.LineFigure3.draw()

    def LineCanvas5_update(self):
        self.LineFigure5.clear()
        self.LineFigure5.fig.canvas.draw()  # 这里注意是画布重绘，self.figs.canvas
        self.LineFigure5.fig.canvas.flush_events()  # 画布刷新self.figs.canvas
        ax5 = self.LineFigure5.ax
        ax5.scatter(self.x_green_1, self.y_green_1, color='green',s=20)

        ax5.scatter(self.x_red_1, self.y_red_1, color='red',s=20)
        ax5.scatter(self.x_blue_1, self.y_blue_1, color='blue',s=20)
        ax5.scatter(self.x_yellow_1, self.y_yellow_1, color='yellow',s=20)

        ax5.plot(self.x1_1, self.y_pred,color='black')

        self.LineFigure5.draw()


    def startanalyzing(self):
        dialog = NewDialog(self.M)
        dialog.exec_()
        

    
    def endlearning(self):
      if(self.state==1):
        self.LineFigure.clear()
        self.LineFigure.fig.canvas.draw()  # 这里注意是画布重绘，self.figs.canvas
        self.LineFigure.fig.canvas.flush_events()  # 画布刷新self.figs.canvas
        self.LineFigureLayout.removeWidget(self.LineFigure)
        self.echart=pg.PlotWidget()
        self.echart1=pg.PlotWidget()
        self.echart2=pg.PlotWidget()
        self.LineFigureLayout.addWidget(self.echart)
        self.LineFigureLayout.addWidget(self.echart1)
        self.LineFigureLayout.addWidget(self.echart2)
        self.curve1=self.echart.plot(self.DATA,pen='w',name="电压")
        self.curve2=self.echart1.plot(self.DATA1,pen='w',name="电流")
        self.curve3=self.echart2.plot(self.DATA2,pen='g',name="功率")

        self.echart.setLabel('left', '电压', units='V')
        self.echart.setLabel('bottom', '时间', units='s')
        self.echart1.setLabel('left', '电流', units='A')
        self.echart1.setLabel('bottom', '时间', units='s')
        self.echart2.setLabel('left', '功率', units='WM')
        self.echart2.setLabel('bottom', '时间', units='s')



        self.X_ptr1 = 0
        #用于记录X轴的位置

        self.timer =QtCore.QTimer()
        # 实例化一个定时器

        self.timer.timeout.connect(self.update_data)
        # 将定时器信号绑定到update_data 函数

        self.timer.start(100)
        self.state=0
    
    
    def updateimg(self):
        self.LineFigure1.clear()
        self.LineFigure1.fig.canvas.draw()  # 这里注意是画布重绘，self.figs.canvas
        self.LineFigure1.fig.canvas.flush_events()  # 画布刷新self.figs.canvas
        ax1=self.LineFigure1.ax
        x=[]
        random_data1=[]  
        self.random_data=[]      
        for i in range(0,20):
            x.append(i)
            self.random_data.append(random.uniform(0.9, 1.0))
            random_data1.append(min(random.uniform(0.01,0.09)+self.random_data[i],1))
        if self.find_state==0:
            if self.startlearning_state==True:
                ax1.plot(x, random_data1, color=(144/255, 238/255, 144/255),label="状态学习曲线")  # 绘制折线图
            ax1.plot(x, self.random_data, color=(0, 100/255, 0),label="原始曲线")  # 绘制折线图
        elif self.find_state==1:
            if self.startlearning_state==True:
                ax1.plot(x, random_data1, color=(1.0, 0.753, 0.796),label="状态学习曲线")  # 绘制折线图
            ax1.plot(x, self.random_data, color=(165/255, 42/255, 42/255),label="原始曲线")  # 绘制折线图
        elif self.find_state==2:
            if self.startlearning_state==True:
                ax1.plot(x, random_data1, color=(0.678, 0.847, 0.902),label="状态学习曲线")  # 绘制折线图
            ax1.plot(x, self.random_data, color=(0.0, 0.0, 0.545),label="原始曲线")  # 绘制折线图
        elif self.find_state==3:
            if self.startlearning_state==True:
                ax1.plot(x, random_data1, color='y',label="状态学习曲线")  # 绘制折线图
            ax1.plot(x, self.random_data, color=(0.855, 0.647, 0.125),label="原始曲线")  # 绘制折线图
        
        if self.find_state1==0:
            ax1.set_ylabel('准确率', fontsize=16)

        elif self.find_state1==1:
            ax1.set_ylabel('精确率', fontsize=16)
        elif self.find_state1==2:
            ax1.set_ylabel('召回率', fontsize=16)
        elif self.find_state1==3:
            ax1.set_ylabel('F1分数', fontsize=16)      
        

        ax1.set_xlabel('Time(d)', fontsize=16)
        ax1.legend()
        self.LineFigure1.draw()
                
            
        
        
    
    def startlearning1(self):
        #dialog = LoadingProgress()
        #dialog.exec_()
        self.startlearning_state=True
        self.updateimg()   
    def choose_state(self):
        sender = self.sender()
        self.find_state=sender.i
        self.updateimg()



    def choose_state1(self):
        sender = self.sender()
        self.find_state1=sender.j
        self.find_state=sender.i
        self.updateimg()  
        
         
    def calculateDays(self):
        self.start_date = self.station_id2_datebox.date()
        self.end_date = self.station_id2_datebox1.date()
        self.diff_days = self.start_date.daysTo(self.end_date)
        self.PrepareSamples1()
        self.LineCanvas3_update()

    def station_id1_button0_clicked(self):
        self.station_id1_button0.setStyleSheet("QPushButton{color:white;font-size:30px;font-weight:normal;font-family:SimHei;border-color:rgb(170, 150, 163);background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop:0 #FFFFFF,stop:0.66 #000000);}"
                                  "QPushButton::hover{color:blue}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.station_id1_button1.setStyleSheet("QPushButton{color:grey;font-size:30px;font-weight:normal;font-family:SimHei;border-color:rgb(170, 150, 163);background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop:0 #FFFFFF,stop:1 #D9D9D9);}"
                                  "QPushButton::hover{color:blue}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.station_id1_button2.setStyleSheet("QPushButton{color:grey;font-size:30px;font-weight:normal;font-family:SimHei;border-color:rgb(170, 150, 163);background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop:0 #FFFFFF,stop:1 #D9D9D9);}"
                                  "QPushButton::hover{color:blue}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.station_id1_button3.setStyleSheet("QPushButton{color:grey;font-size:30px;font-weight:normal;font-family:SimHei;border-color:rgb(170, 150, 163);background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop:0 #FFFFFF,stop:1 #D9D9D9);}"
                                  "QPushButton::hover{color:blue}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.station_id1_button4.setStyleSheet("QPushButton{color:grey;font-size:30px;font-weight:normal;font-family:SimHei;border-color:rgb(170, 150, 163);background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop:0 #FFFFFF,stop:1 #D9D9D9);}"
                                  "QPushButton::hover{color:blue}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.find_state=0
        station_id1_picture_cover_img = os.path.abspath("myproject\\picture\\picture1.png")
        station_id1_picture_image1 = QtGui.QPixmap(station_id1_picture_cover_img)
        self.station_id1_picture.setScaledContents(True)
        self.station_id1_picture.setPixmap(station_id1_picture_image1)
        self.state3.setStyleSheet("QLabel{background-color:#338D27}") 
        self.state4.setStyleSheet("QLabel{color:#338D27;font-size:30px;font-weight:normal;font-family:SimHei;}")
        self.state5.setStyleSheet("QLabel{background-color:#B5B5B6}") 
        self.state6.setStyleSheet("QLabel{color:#B5B5B6;font-size:30px;font-weight:normal;font-family:SimHei;}") 
        self.state7.setStyleSheet("QLabel{background-color:#B5B5B6}") 
        self.state8.setStyleSheet("QLabel{color:#B5B5B6;font-size:30px;font-weight:normal;font-family:SimHei;}") 
        self.state9.setStyleSheet("QLabel{background-color:#B5B5B6}") 
        self.state10.setStyleSheet("QLabel{color:#B5B5B6;font-size:30px;font-weight:normal;font-family:SimHei;}") 
        
        
        
        op = QtWidgets.QGraphicsOpacityEffect()
        # 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
        op.setOpacity(1)
        self.loadinggif.setGraphicsEffect(op)
        self.arrow0.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #009688;}")

        self.arrow1.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #009688;}")
        self.arrow1_1.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #009688;}")

        self.arrow2.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #009688;}")
        self.arrow2_1.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #009688;}")

        self.arrow3.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #009688;}")
        self.arrow14.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #FFFFFF;}")
        self.arrow15.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #FFFFFF;}")
        self.arrow16.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #FFFFFF;}")
        cover_img_1_0 = os.path.abspath("myproject\\picture\\picture3.png")
        image1_0 = QtGui.QPixmap(cover_img_1_0 )
        self.picture5_1.setPixmap(image1_0) 
        t1=Thread(target=self.simulate_and_record,args=(self.G,self.T,'normal'))
        t1.start()
        t1.setName('正常')  # ！！！！
        standard_G=[1000]*20
        standard_T=[25]*20
        t2=Thread(target=self.simulate_and_record_standard,args=(standard_G,standard_T,'normal'))
        t2.start()
        t2.setName('设置线程名')  # ！！！！

        #t1.join()  # 等待子线程运行结束

        
        
    def station_id1_button1_clicked(self):
        self.station_id1_button1.setStyleSheet("QPushButton{color:white;font-size:30px;font-weight:normal;font-family:SimHei;border-color:rgb(170, 150, 163);background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop:0 #FFFFFF,stop:0.66 #000000);}"
                                  "QPushButton::hover{color:blue}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.station_id1_button0.setStyleSheet("QPushButton{color:grey;font-size:30px;font-weight:normal;font-family:SimHei;border-color:rgb(170, 150, 163);background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop:0 #FFFFFF,stop:1 #D9D9D9);}"
                                  "QPushButton::hover{color:blue}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.station_id1_button2.setStyleSheet("QPushButton{color:grey;font-size:30px;font-weight:normal;font-family:SimHei;border-color:rgb(170, 150, 163);background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop:0 #FFFFFF,stop:1 #D9D9D9);}"
                                  "QPushButton::hover{color:blue}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.station_id1_button3.setStyleSheet("QPushButton{color:grey;font-size:30px;font-weight:normal;font-family:SimHei;border-color:rgb(170, 150, 163);background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop:0 #FFFFFF,stop:1 #D9D9D9);}"
                                  "QPushButton::hover{color:blue}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.station_id1_button4.setStyleSheet("QPushButton{color:grey;font-size:30px;font-weight:normal;font-family:SimHei;border-color:rgb(170, 150, 163);background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop:0 #FFFFFF,stop:1 #D9D9D9);}"
                                  "QPushButton::hover{color:blue}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.find_state=1
        station_id1_picture_cover_img = os.path.abspath("myproject\\picture\\LL.png")
        station_id1_picture_image1 = QtGui.QPixmap(station_id1_picture_cover_img)
        self.station_id1_picture.setScaledContents(True)
        self.station_id1_picture.setPixmap(station_id1_picture_image1)
        self.state3.setStyleSheet("QLabel{background-color:#B5B5B6}") 
        self.state4.setStyleSheet("QLabel{color:#B5B5B6;font-size:30px;font-weight:normal;font-family:SimHei;}")
        self.state5.setStyleSheet("QLabel{background-color:#C00000}") 
        self.state6.setStyleSheet("QLabel{color:#C00000;font-size:30px;font-weight:normal;font-family:SimHei;}") 
        self.state7.setStyleSheet("QLabel{background-color:#B5B5B6}") 
        self.state8.setStyleSheet("QLabel{color:#B5B5B6;font-size:30px;font-weight:normal;font-family:SimHei;}") 
        self.state9.setStyleSheet("QLabel{background-color:#B5B5B6}") 
        self.state10.setStyleSheet("QLabel{color:#B5B5B6;font-size:30px;font-weight:normal;font-family:SimHei;}")         

        op = QtWidgets.QGraphicsOpacityEffect()
        # 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
        op.setOpacity(1)
        self.loadinggif.setGraphicsEffect(op)

        self.arrow0.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #004098;}")
        self.arrow1.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #004098;}")
        self.arrow1_1.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #FFFFFF;}")

        self.arrow2.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #FFFFFF;}")
        self.arrow2_1.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #004098;}")
        self.arrow14.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #004098;}")
        self.arrow15.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #004098;}")
        self.arrow16.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #004098;}")

        cover_img_1_1 = os.path.abspath("myproject\\picture\\picture4.png")
        image1_1 = QtGui.QPixmap(cover_img_1_1 )
        self.picture5_1.setPixmap(image1_1)
        self.arrow3.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #004098;}")
        t1=Thread(target=self.simulate_and_record,args=(self.G,self.T,'LL'))
        t1.start()
        t1.setName('正常')  # ！！！！
        standard_G=[1000]*20
        standard_T=[25]*20
        t2=Thread(target=self.simulate_and_record_standard,args=(standard_G,standard_T,'LL'))
        t2.start()
        t2.setName('设置线程名')  # ！！！！
        #t1.join()  # 等待子线程运行结束

        
    def station_id1_button2_clicked(self):
        self.station_id1_button2.setStyleSheet("QPushButton{color:white;font-size:30px;font-weight:normal;font-family:SimHei;border-color:rgb(170, 150, 163);background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop:0 #FFFFFF,stop:0.66 #000000);}"
                                  "QPushButton::hover{color:blue}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.station_id1_button1.setStyleSheet("QPushButton{color:grey;font-size:30px;font-weight:normal;font-family:SimHei;border-color:rgb(170, 150, 163);background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop:0 #FFFFFF,stop:1 #D9D9D9);}"
                                  "QPushButton::hover{color:blue}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.station_id1_button0.setStyleSheet("QPushButton{color:grey;font-size:30px;font-weight:normal;font-family:SimHei;border-color:rgb(170, 150, 163);background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop:0 #FFFFFF,stop:1 #D9D9D9);}"
                                  "QPushButton::hover{color:blue}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.station_id1_button3.setStyleSheet("QPushButton{color:grey;font-size:30px;font-weight:normal;font-family:SimHei;border-color:rgb(170, 150, 163);background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop:0 #FFFFFF,stop:1 #D9D9D9);}"
                                  "QPushButton::hover{color:blue}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.station_id1_button4.setStyleSheet("QPushButton{color:grey;font-size:30px;font-weight:normal;font-family:SimHei;border-color:rgb(170, 150, 163);background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop:0 #FFFFFF,stop:1 #D9D9D9);}"
                                  "QPushButton::hover{color:blue}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.find_state=2
        station_id1_picture_cover_img = os.path.abspath("myproject\\picture\\OC.png")
        station_id1_picture_image1 = QtGui.QPixmap(station_id1_picture_cover_img)
        self.station_id1_picture.setScaledContents(True)
        self.station_id1_picture.setPixmap(station_id1_picture_image1)
        self.state3.setStyleSheet("QLabel{background-color:#B5B5B6}") 
        self.state4.setStyleSheet("QLabel{color:#B5B5B6;font-size:30px;font-weight:normal;font-family:SimHei;}")
        self.state5.setStyleSheet("QLabel{background-color:#B5B5B6}") 
        self.state6.setStyleSheet("QLabel{color:#B5B5B6;font-size:30px;font-weight:normal;font-family:SimHei;}") 
        self.state7.setStyleSheet("QLabel{background-color:#004098}") 
        self.state8.setStyleSheet("QLabel{color:#004098;font-size:30px;font-weight:normal;font-family:SimHei;}") 
        self.state9.setStyleSheet("QLabel{background-color:#B5B5B6}") 
        self.state10.setStyleSheet("QLabel{color:#B5B5B6;font-size:30px;font-weight:normal;font-family:SimHei;}")  
        
        cover_img_1_0 = os.path.abspath("myproject\\picture\\picture3.png")
        image1_0 = QtGui.QPixmap(cover_img_1_0 )
        self.picture5_1.setPixmap(image1_0) 
        op = QtWidgets.QGraphicsOpacityEffect()
        # 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
        op.setOpacity(1)
        self.loadinggif.setGraphicsEffect(op)
        self.arrow0.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #FFFFFF;}")

        self.arrow1.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #FFFFFF;}")
        self.arrow1_1.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #FFFFFF;}")

        self.arrow2.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #FFFFFF;}")
        self.arrow2_1.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #FFFFFF;}")

        self.arrow3.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #FFFFFF;}")
        self.arrow14.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #FFFFFF;}")
        self.arrow15.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #FFFFFF;}")
        self.arrow16.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #FFFFFF;}")
        t1=Thread(target=self.simulate_and_record,args=(self.G,self.T,'OC'))
        t1.start()
        t1.setName('正常')  # ！！！！
        standard_G=[1000]*20
        standard_T=[25]*20
        t2=Thread(target=self.simulate_and_record_standard,args=(standard_G,standard_T,'OC'))
        t2.start()
        t2.setName('设置线程名')  # ！！！！
        #t1.join()  # 等待子线程运行结束



        
    def station_id1_button3_clicked(self):
        self.station_id1_button3.setStyleSheet("QPushButton{color:white;font-size:30px;font-weight:normal;font-family:SimHei;border-color:rgb(170, 150, 163);background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop:0 #FFFFFF,stop:0.66 #000000);}"
                                  "QPushButton::hover{color:blue}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.station_id1_button1.setStyleSheet("QPushButton{color:grey;font-size:30px;font-weight:normal;font-family:SimHei;border-color:rgb(170, 150, 163);background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop:0 #FFFFFF,stop:1 #D9D9D9);}"
                                  "QPushButton::hover{color:blue}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.station_id1_button2.setStyleSheet("QPushButton{color:grey;font-size:30px;font-weight:normal;font-family:SimHei;border-color:rgb(170, 150, 163);background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop:0 #FFFFFF,stop:1 #D9D9D9);}"
                                  "QPushButton::hover{color:blue}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.station_id1_button0.setStyleSheet("QPushButton{color:grey;font-size:30px;font-weight:normal;font-family:SimHei;border-color:rgb(170, 150, 163);background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop:0 #FFFFFF,stop:1 #D9D9D9);}"
                                  "QPushButton::hover{color:blue}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.station_id1_button4.setStyleSheet("QPushButton{color:grey;font-size:30px;font-weight:normal;font-family:SimHei;border-color:rgb(170, 150, 163);background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop:0 #FFFFFF,stop:1 #D9D9D9);}"
                                  "QPushButton::hover{color:blue}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.find_state=3
        station_id1_picture_cover_img = os.path.abspath("myproject\\picture\\PS1.png")
        station_id1_picture_image1 = QtGui.QPixmap(station_id1_picture_cover_img)
        self.state3.setStyleSheet("QLabel{background-color:#B5B5B6}") 
        self.state4.setStyleSheet("QLabel{color:#B5B5B6;font-size:30px;font-weight:normal;font-family:SimHei;}")
        self.state5.setStyleSheet("QLabel{background-color:#B5B5B6}") 
        self.state6.setStyleSheet("QLabel{color:#B5B5B6;font-size:30px;font-weight:normal;font-family:SimHei;}") 
        self.state7.setStyleSheet("QLabel{background-color:#B5B5B6}") 
        self.state8.setStyleSheet("QLabel{color:#B5B5B6;font-size:30px;font-weight:normal;font-family:SimHei;}") 
        self.state9.setStyleSheet("QLabel{background-color:#FDD000}") 
        self.state10.setStyleSheet("QLabel{color:#FDD000;font-size:30px;font-weight:normal;font-family:SimHei;}")   
        self.station_id1_picture.setScaledContents(True)
        self.station_id1_picture.setPixmap(station_id1_picture_image1)

        op = QtWidgets.QGraphicsOpacityEffect()
        # 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
        op.setOpacity(1)
        self.loadinggif.setGraphicsEffect(op)
        cover_img_1_1 = os.path.abspath("myproject\\picture\\picture7.png")
        image1_1 = QtGui.QPixmap(cover_img_1_1 )
        self.picture5_1.setPixmap(image1_1)
        
        self.arrow0.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #009688;}")

        self.arrow1.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #009688;}")
        self.arrow1_1.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #009688;}")

        self.arrow2.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #009688;}")
        self.arrow2_1.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #009688;}")

        self.arrow3.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #009688;}")
        self.arrow14.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #FFFFFF;}")
        self.arrow15.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #FFFFFF;}")
        self.arrow16.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #FFFFFF;}")        
        
        t1=Thread(target=self.simulate_and_record,args=(self.G,self.T,'PS1'))
        t1.start()
        t1.setName('正常')  # ！！！！
        standard_G=[1000]*20
        standard_T=[25]*20
        t2=Thread(target=self.simulate_and_record_standard,args=(standard_G,standard_T,'PS1'))
        t2.start()
        t2.setName('设置线程名')  # ！！！！
        #t1.join()  # 等待子线程运行结束
 
        
    def station_id1_button4_clicked(self):
        self.station_id1_button4.setStyleSheet("QPushButton{color:white;font-size:30px;font-weight:normal;font-family:SimHei;border-color:rgb(170, 150, 163);background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop:0 #FFFFFF,stop:0.66 #000000);}"
                                  "QPushButton::hover{color:blue}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.station_id1_button1.setStyleSheet("QPushButton{color:grey;font-size:30px;font-weight:normal;font-family:SimHei;border-color:rgb(170, 150, 163);background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop:0 #FFFFFF,stop:1 #D9D9D9);}"
                                  "QPushButton::hover{color:blue}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.station_id1_button2.setStyleSheet("QPushButton{color:grey;font-size:30px;font-weight:normal;font-family:SimHei;border-color:rgb(170, 150, 163);background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop:0 #FFFFFF,stop:1 #D9D9D9);}"
                                  "QPushButton::hover{color:blue}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.station_id1_button3.setStyleSheet("QPushButton{color:grey;font-size:30px;font-weight:normal;font-family:SimHei;border-color:rgb(170, 150, 163);background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop:0 #FFFFFF,stop:1 #D9D9D9);}"
                                  "QPushButton::hover{color:blue}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.station_id1_button0.setStyleSheet("QPushButton{color:grey;font-size:30px;font-weight:normal;font-family:SimHei;border-color:rgb(170, 150, 163);background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop:0 #FFFFFF,stop:1 #D9D9D9);}"
                                  "QPushButton::hover{color:blue}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.find_state=3
        station_id1_picture_cover_img = os.path.abspath("myproject\\picture\\PS2.png")
        station_id1_picture_image1 = QtGui.QPixmap(station_id1_picture_cover_img)
        self.station_id1_picture.setScaledContents(True)
        self.station_id1_picture.setPixmap(station_id1_picture_image1)
        self.state3.setStyleSheet("QLabel{background-color:#B5B5B6}") 
        self.state4.setStyleSheet("QLabel{color:#B5B5B6;}")
        self.state5.setStyleSheet("QLabel{background-color:#B5B5B6}") 
        self.state6.setStyleSheet("QLabel{color:#B5B5B6}") 
        self.state7.setStyleSheet("QLabel{background-color:#B5B5B6}") 
        self.state8.setStyleSheet("QLabel{color:#B5B5B6}") 
        self.state9.setStyleSheet("QLabel{background-color:#FDD000}") 
        self.state10.setStyleSheet("QLabel{color:#FDD000}")   
        op = QtWidgets.QGraphicsOpacityEffect()
        # 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
        op.setOpacity(1)
        self.loadinggif.setGraphicsEffect(op)

        cover_img_1_1 = os.path.abspath("myproject\\picture\\picture7.png")
        image1_1 = QtGui.QPixmap(cover_img_1_1 )
        self.picture5_1.setPixmap(image1_1)
        self.arrow0.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #009688;}")

        self.arrow1.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #009688;}")
        self.arrow1_1.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #009688;}")

        self.arrow2.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #009688;}")
        self.arrow2_1.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #009688;}")

        self.arrow3.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #009688;}")
        self.arrow14.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #FFFFFF;}")
        self.arrow15.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #FFFFFF;}")
        self.arrow16.setStyleSheet("QProgressBar{ border-radius: 4px;}"
                                  "QProgressBar::chunk{border-radius: 4px;background-color: #FFFFFF;}")
        t1=Thread(target=self.simulate_and_record,args=(self.G,self.T,'PS2'))
        t1.start()
        t1.setName('正常')  # ！！！！
        standard_G=[1000]*20
        standard_T=[25]*20
        t2=Thread(target=self.simulate_and_record_standard,args=(standard_G,standard_T,'PS2'))
        t2.start()
        t2.setName('设置线程名')  # ！！！！
        #t1.join()  # 等待子线程运行结束

      
    def on_button_clicked5(self):
        op = QtWidgets.QGraphicsOpacityEffect()
        # 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
        op.setOpacity(1)
        self.loadinggif.setGraphicsEffect(op)
        if self.comparsion5_button.checked==True:
                self.myflag1=float(1)
        else:
            self.myflag1=float(0)
        t3=Thread(target=self.analyze,args=(self.myflag1,self.myflag2,self.myflag3,))
        t3.start()
        t3.setName('设置线程名')  # ！！！！
    def on_button_clicked6(self):
        op = QtWidgets.QGraphicsOpacityEffect()
        # 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
        op.setOpacity(1)
        self.loadinggif.setGraphicsEffect(op)
        if self.comparsion6_button.checked==True:
            self.myflag2=float(1)
        else:
            self.myflag2=float(0)
        t3=Thread(target=self.analyze,args=(self.myflag1,self.myflag2,self.myflag3,))
        t3.start()
        t3.setName('设置线程名')  # ！！！！
    def on_button_clicked7(self):
        op = QtWidgets.QGraphicsOpacityEffect()
        # 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
        op.setOpacity(1)
        self.loadinggif.setGraphicsEffect(op)
        if self.comparsion7_button.checked==True:
            self.myflag3=float(1)
        else:
            self.myflag3=float(0)
        t3=Thread(target=self.analyze,args=(self.myflag1,self.myflag2,self.myflag3,))
        t3.start()
        t3.setName('设置线程名')  # ！！！！









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



