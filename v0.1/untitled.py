# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import random
import os
from test2 import SecondWindow
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QDesktopWidget,QWidget,QHeaderView,QAbstractItemView,QComboBox,QCheckBox,QBoxLayout,QVBoxLayout
from PyQt5.QtCore import QTimer, QCoreApplication
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
import matplotlib
import matplotlib.cbook as cbook
import pandas
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import matlab
import matlab.engine
#eng = matlab.engine.start_matlab()
#eng.cd("C:\\Users\\whitefork\\Desktop\\python\\myproject",nargout=0)

class MyButton(QPushButton):

    def __init__(self, parent=None):
        super().__init__( parent)
        self.s= SecondWindow()
        self.clicked.connect(self.slot)
    def set_i(self,i):

        self.s.setWindowTitle(str(i)+"号机")
        self.clicked.connect(self.slot)
        
    def slot(self):
      self.s.show()
      

class MyCustomWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen()
        pen.setColor(QColor(0, 0, 255))  # 设置线条颜色为蓝色
        pen.setWidth(4)  # 设置线宽为2像素
        pen.setStyle(Qt.SolidLine)  # 设置线条样式为虚线
        painter.setPen(pen)

        x1, y1 = 10, 10  # 起点坐标
        x2, y2 = self.width(), 10  # 终点坐标（与窗口右边对齐）
        painter.drawLine(x1, y1, x2, y2)

class MyCustomWidget1(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen()
        pen.setColor(QColor(0, 0, 255))  # 设置线条颜色为蓝色
        pen.setWidth(4)  # 设置线宽为2像素
        pen.setStyle(Qt.SolidLine)  # 设置线条样式为虚线
        painter.setPen(pen)

        x1, y1 = 10, 10  # 起点坐标
        x2, y2 = 10, self.width()  # 终点坐标（与窗口右边对齐）
        painter.drawLine(x1, y1, x2, y2)



    
    
class Ui_MainWindow(object):
    num=5
    a=[]
    data=[]
    id=0
    def __init__(self):
        super().__init__()


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        
        

        
        self.widget_menu = QtWidgets.QWidget(self)  # 注意，传入参数代表一个从属关系，表示创建的QWidget属于self，也就是MainWindow自身
        self.widget_menu.setObjectName("widget_menu")
        # 设置窗口的左上角x,y,窗口的width和height
        self.widget_menu.setGeometry(QtCore.QRect(0, 90, 1280, 20))
        self.widget_menu.setStyleSheet("QWidget{background-color:rgb(123,223,223);border:2px solid balck;}")


        self.widget_menu1 = QtWidgets.QWidget(self)  # 注意，传入参数代表一个从属关系，表示创建的QWidget属于self，也就是MainWindow自身
        self.widget_menu1.setObjectName("widget_menu1")
        # 设置窗口的左上角x,y,窗口的width和height
        self.widget_menu1.setGeometry(QtCore.QRect(400, 10, 400, 100))

        # 1.2 创建一个水平布局
        self.menuLayout1 = QHBoxLayout(self.widget_menu1)
        # 1.3 设置水平布局的属性
        self.menuLayout1.setSpacing(10)  # 设置间距
        self.menuLayout1.setDirection(0)  # 自左向右的布局
        self.menuLayout1.addSpacing(0)  # 最左端增加30像素的间距
        # 1.4 为菜单栏设置按钮组
        self.menuButtonGroup1 = QButtonGroup()      
        menuStr1 = []
        menuStr1.append("光伏电站1")
        menuStr1.append("光伏电站2")
        menuStr1.append("光伏电站3")
        self.font = QFont()  # 设置字样式
        self.font.setFamily("黑体")  # 设置字体
        self.font.setBold(1)  # 设置为粗体
        self.font.setPixelSize(40)  # 字体大小
        # 1.5 添加按钮至按钮组
        count1 = 0  # 设置按钮在按钮组内的序号
        for menu_str1 in menuStr1:
            menuBtn1 = QPushButton()  # 创建按钮
            menuBtn1.setStyleSheet("QPushButton{color:rgb(0,0,0);border-color:rgb(170, 150, 163);background-color: rgb(170, 150, 163);}"
                                  "QPushButton::hover{color:rgb(58,164,98)}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
            menuBtn1.setFont(self.font)  # 加载字体
            menuBtn1.setText(menu_str1)  # 加载文字
            menuBtn1.setParent(self.widget_menu1)  # 属于一级菜单栏的窗口
            menuBtn1.setMaximumSize(200, 50)
             

            self.menuLayout1.addWidget(menuBtn1)  # 一级菜单栏的水平布局中添加该按钮

            self.menuButtonGroup1.addButton(menuBtn1, count1)  # 把按钮添加到按钮组中
            self.menuButtonGroup1.buttonClicked[int].connect(self.slot)

            count1 += 1




        self.widget_menu2 = QtWidgets.QWidget(self)  # 注意，传入参数代表一个从属关系，表示创建的QWidget属于self，也就是MainWindow自身
        self.widget_menu2.setObjectName("widget_menu2")
        # 设置窗口的左上角x,y,窗口的width和height
        self.widget_menu2.setGeometry(QtCore.QRect(0, 100, 200, 150))

        # 1.2 创建一个水平布局
        self.menuLayout2 = QVBoxLayout(self.widget_menu2)
        # 1.3 设置水平布局的属性
        self.menuLayout2.setSpacing(0)  # 设置间距

        # 1.4 为菜单栏设置按钮组
        self.menuButtonGroup2 = QButtonGroup()      
        menuStr2 = []
        menuStr2.append("电站信息")
        menuStr2.append("发电状态")
        menuStr2.append("状态统计")
        self.font = QFont()  # 设置字样式
        self.font.setFamily("黑体")  # 设置字体
        self.font.setBold(1)  # 设置为粗体
        self.font.setPixelSize(40)  # 字体大小
        # 1.5 添加按钮至按钮组
        count2 = 0  # 设置按钮在按钮组内的序号
        for menu_str2 in menuStr2:

              
            menuBtn2 = QPushButton()  # 创建按钮
            menuBtn2.setStyleSheet("QPushButton{color:rgb(0,0,0);border-color:rgb(170, 150, 163);background-color: rgb(170, 150, 163);}"
                                  "QPushButton::hover{color:rgb(58,164,98)}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
            menuBtn2.setFont(self.font)  # 加载字体
            menuBtn2.setText(menu_str2)  # 加载文字
            menuBtn2.setParent(self.widget_menu2)  # 属于一级菜单栏的窗口
            menuBtn2.setMaximumSize(180, 50)
            
            if count2==0:
              menuBtn2.clicked.connect(self.gotoanother0)
            if count2==1:
              menuBtn2.clicked.connect(self.gotoanother1)
            if count2==2:
              menuBtn2.clicked.connect(self.gotoanother2)


            self.menuLayout2.addWidget(menuBtn2)  # 一级菜单栏的水平布局中添加该按钮
            self.menuButtonGroup2.addButton(menuBtn2, count2)  # 把按钮添加到按钮组中
            count2 += 1
            



        
        
        
        
        
        
        
        
        
        
        









        
       #重新生成数据的按钮
       
       
        # self.pushButton = QtWidgets.QPushButton("重新生成数据",self.centralwidget)
        # self.pushButton.setGeometry(QtCore.QRect(300, 200, 150, 50))
        # self.pushButton.setObjectName("pushButton")

        
        # self.pushButton1 = QtWidgets.QPushButton("开始分析",self.centralwidget)
        # self.pushButton1.setGeometry(QtCore.QRect(300, 260, 150, 50))
        # self.pushButton1.setObjectName("pushButton1")
        

        # self.pushButton2 = QtWidgets.QPushButton("运行状态分析",self.centralwidget)
        # self.pushButton2.setGeometry(QtCore.QRect(770, 120, 150, 50))
        # self.pushButton2.setObjectName("pushButton2")
        # self.label4 = QtWidgets.QLabel("运行状况:正常 ", self.centralwidget)
        # # 显示位置与大小：(x, y, w, h)
        # self.label4.setGeometry(650, 160, 200, 80)
        # self.label4.setStyleSheet("QLabel{font-size:30px;font-weight:normal;font-family:Arial;}")       
        
        
        # self.label5 = QtWidgets.QLabel("故障情况:短路 ", self.centralwidget)
        # # 显示位置与大小：(x, y, w, h)
        # self.label5.setGeometry(650, 200, 200, 80)
        # self.label5.setStyleSheet("QLabel{font-size:30px;font-weight:normal;font-family:Arial;}")       
        
        
        #控制生成数据的数量


        #生成标题
        
        # 创建label，创建之初指定父亲
        self.label = QtWidgets.QLabel("分布式光伏发电在线监测系统 ", self.centralwidget)
        # 显示位置与大小：(x, y, w, h)
        self.label.setGeometry(370, 0, 450, 40)
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        # 设置阴影 据说只有加了这步才能设置边框颜色。///可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
        self.label.setFrameShadow(QtWidgets.QFrame.Raised)
        # 设置背景颜色，包括边框颜色
        # self.label.setStyleSheet()
        self.label.setFrameShape(QFrame.Box)
        self.label.setAlignment(Qt.AlignCenter) 
        self.label.setStyleSheet("QLabel{font-size:50px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;background-color: rgb(100, 149, 237);}")

        

        # # 创建label，创建之初指定父亲
        # self.label1 = QtWidgets.QLabel("展示方式: ", self.centralwidget)
        # # 显示位置与大小：(x, y, w, h)
        # self.label1.setGeometry(50, 280, 100, 30)
        # self.label1.setStyleSheet("QLabel{font-size:30px;font-weight:normal;font-family:Arial;}")       
        # #生成小菜单
        # self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        # self.comboBox.setGeometry(QtCore.QRect(50, 310, 200, 30))
        # #添加一个下拉选项
        # self.comboBox.addItem("折线图")
        # #从列表中添加下拉选项
        # self.comboBox.addItems(["柱状图", "3D", "热力图"])



        # # 创建label，创建之初指定父亲
        # self.label2 = QtWidgets.QLabel("展示内容: ", self.centralwidget)
        # # 显示位置与大小：(x, y, w, h)
        # self.label2.setGeometry(50, 220, 90, 30)
        # self.label2.setStyleSheet("QLabel{font-size:30px;font-weight:normal;font-family:Arial;}")       
        # #生成小菜单
        # self.comboBox2 = QtWidgets.QComboBox(self.centralwidget)
        # self.comboBox2.setGeometry(QtCore.QRect(50, 250, 200, 30))
        # #添加一个下拉选项
        # self.comboBox2.addItem("电流")
        # #从列表中添加下拉选项
        # self.comboBox2.addItems(["电压", "功率"])
        
        # # 创建label，创建之初指定父亲
        # self.label3 = QtWidgets.QLabel("设备: ", self.centralwidget)
        # # 显示位置与大小：(x, y, w, h)
        # self.label3.setGeometry(50, 160, 90, 30)
        # self.label3.setStyleSheet("QLabel{font-size:30px;font-weight:normal;font-family:Arial;}")       
        # #生成小菜单
        # self.comboBox3 = QtWidgets.QComboBox(self.centralwidget)
        # self.comboBox3.setGeometry(QtCore.QRect(50, 190, 200, 30))
        # #添加一个下拉选项
        # self.comboBox3.addItem("0号")
        # #从列表中添加下拉选项
        # self.comboBox3.addItems(["1号", "2号", "3号"])




        # self.custom_widget = MyCustomWidget(self.centralwidget)  # 创建自定义Widget
        # self.custom_widget.setGeometry(QtCore.QRect(600, 280, 800, 30))
        # self.custom_widget1 = MyCustomWidget1(self.centralwidget)  # 创建自定义Widget
        # self.custom_widget1.setGeometry(QtCore.QRect(600, 90, 500, 195))
        # self.custom_widget2 = MyCustomWidget(self.centralwidget)  # 创建自定义Widget
        # self.custom_widget2.setGeometry(QtCore.QRect(590, 290, 820, 30))
        # self.custom_widget3 = MyCustomWidget1(self.centralwidget)  # 创建自定义Widget
        # self.custom_widget3.setGeometry(QtCore.QRect(590, 90, 500, 205))





        #生成表格

        self.form1= QtWidgets.QWidget(self)
        self.form1.setObjectName("form1")
        self.form2= QtWidgets.QWidget(self)
        self.form2.setObjectName("form2")
        self.form3= QtWidgets.QWidget(self)
        self.form3.setObjectName("form3")
        



        self.window0 = QtWidgets.QLabel( self.form1)
        self.window0.setText("电站名称：列克星敦号发电站\n容量:100000kw\n在线监测状态:正常")
        self.window0.setWordWrap(True)
        # 显示位置与大小：(x, y, w, h)
        self.window0.setGeometry(300, 130, 500, 100)
        self.window0.setFrameShape(QtWidgets.QFrame.Box)
        # 设置阴影 据说只有加了这步才能设置边框颜色。///可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
        self.window0.setFrameShadow(QtWidgets.QFrame.Raised)
        # 设置背景颜色，包括边框颜色
        # self.label.setStyleSheet()
        self.window0.setAlignment(Qt.AlignCenter)
        self.window0.setLineWidth(2)

        self.window0.setFont(self.font)
        #self.window0.setStyleSheet("QLabel{color:white;font-size:50px;font-weight:normal;font-family:Arial;border-width: 1px;color:rgb(0,0,0);border-color:rgb(170, 150, 163);background-color: rgb(170, 150, 163);}")

        self.picture1 = QtWidgets.QLabel(self.form1)
        self.picture1.setText("")
        self.picture1.setObjectName("picture1")
        cover_img = os.path.abspath("myproject\\picture\\picture1.png")
        image1 = QtGui.QPixmap(cover_img)
        self.picture1.setScaledContents(True)
        self.picture1.setPixmap(image1)
        self.picture1.setGeometry(QtCore.QRect(100, 250, 250, 200))

        self.window1 = QtWidgets.QLabel( self.form1)
        self.window1.setText("光伏组件型号:\n参数:")
        self.window1.setWordWrap(True)
        # 显示位置与大小：(x, y, w, h)
        self.window1.setGeometry(100, 460, 250, 100)
        self.window1.setFrameShape(QtWidgets.QFrame.Box)
        # 设置阴影 据说只有加了这步才能设置边框颜色。///可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
        self.window1.setFrameShadow(QtWidgets.QFrame.Raised)
        # 设置背景颜色，包括边框颜色
        # self.label.setStyleSheet()
        self.window1.setAlignment(Qt.AlignCenter)
        self.window1.setLineWidth(2)
        self.window1.setFont(self.font)



        self.picture2 = QtWidgets.QLabel(self.form1)
        self.picture2.setText("")
        self.picture2.setObjectName("picture2")
        cover_img = os.path.abspath("myproject\\picture\\picture2.png")
        image1 = QtGui.QPixmap(cover_img)
        self.picture2.setScaledContents(True)
        self.picture2.setPixmap(image1)
        self.picture2.setGeometry(QtCore.QRect(400, 250, 250, 200))

        self.window2 = QtWidgets.QLabel( self.form1)
        self.window2.setText("逆变器型号:\n参数:")
        self.window2.setWordWrap(True)
        # 显示位置与大小：(x, y, w, h)
        self.window2.setGeometry(400, 460, 250, 100)
        self.window2.setFrameShape(QtWidgets.QFrame.Box)
        # 设置阴影 据说只有加了这步才能设置边框颜色。///可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
        self.window2.setFrameShadow(QtWidgets.QFrame.Raised)
        # 设置背景颜色，包括边框颜色
        # self.label.setStyleSheet()
        self.window2.setAlignment(Qt.AlignCenter)
        self.window2.setLineWidth(2)
        self.window2.setFont(self.font)
        
        self.window3 = QtWidgets.QLabel( self.form1)
        self.window3.setText("传感器型号:\n参数:")
        self.window3.setWordWrap(True)
        # 显示位置与大小：(x, y, w, h)
        self.window3.setGeometry(700, 460, 250, 100)
        self.window3.setFrameShape(QtWidgets.QFrame.Box)
        # 设置阴影 据说只有加了这步才能设置边框颜色。///可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
        self.window3.setFrameShadow(QtWidgets.QFrame.Raised)
        # 设置背景颜色，包括边框颜色
        # self.label.setStyleSheet()
        self.window3.setAlignment(Qt.AlignCenter)
        self.window3.setLineWidth(2)
        self.window3.setFont(self.font)

        #日期框
        self.yearbox = QtWidgets.QComboBox(self.form2)

        self.yearbox.addItem("2024")
        self.yearbox.addItems(["2023", "2022", "2021"])
        self.yearlabel=QtWidgets.QLabel("年",self.form2)
        self.yearbox.setGeometry(200, 130, 60, 30)
        self.yearlabel.setGeometry(260, 130, 20, 30)
        self.monthbox = QtWidgets.QComboBox(self.form2)
        self.monthbox.addItem("2")
        self.monthbox.addItems(["1", "3", "4","5","6","7","8","9"])
        self.monthlabel=QtWidgets.QLabel("月",self.form2)
        self.monthbox.setGeometry(280, 130, 60, 30)
        self.monthlabel.setGeometry(340, 130, 20, 30)
        self.datebox = QtWidgets.QComboBox(self.form2)
        self.datebox.addItem("2")
        self.datebox.addItems(["1", "3", "4","5","6","7","8","9"])
        self.datelabel=QtWidgets.QLabel("日",self.form2)
        self.datebox.setGeometry(360, 130, 60, 30)
        self.datelabel.setGeometry(420, 130, 20, 30)
        
        #画图
        self.LineDisplayGB = QtWidgets.QWidget(self.form2)
        self.LineDisplayGB.setObjectName("LineDisplayGB")
        self.LineDisplayGB.setGeometry(QtCore.QRect(200, 180, 600, 400))
        
        #退出键
        self.exitbutton=QtWidgets.QPushButton("退出",self.form2)
        self.exitbutton.setGeometry(800,130,60,30)
        self.exitbutton.setStyleSheet("QPushButton{color:rgb(0,0,0);border-color:rgb(170, 150, 163);background-color: rgb(170, 150, 163);}"
                                  "QPushButton::hover{color:rgb(58,164,98)}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.exitbutton.setFont(self.font)
        
        
        self.state0 = QtWidgets.QLabel("发电状态", self.form2)
        # 显示位置与大小：(x, y, w, h)
        self.state0.setGeometry(850, 200, 100, 40)
        self.state0.setFrameShape(QtWidgets.QFrame.Box)
        # 设置阴影 据说只有加了这步才能设置边框颜色。///可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
        self.state0.setFrameShadow(QtWidgets.QFrame.Raised)
        # 设置背景颜色，包括边框颜色
        # self.label.setStyleSheet()
        self.state0.setFrameShape(QFrame.Box)
        self.state0.setAlignment(Qt.AlignCenter) 
        self.state0.setStyleSheet("QLabel{font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")
        
        self.state1 = QtWidgets.QLabel("正常", self.form2)
        # 显示位置与大小：(x, y, w, h)
        self.state1.setGeometry(850, 260, 70, 40)
        self.state1.setFrameShape(QtWidgets.QFrame.Box)
        # 设置阴影 据说只有加了这步才能设置边框颜色。///可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
        self.state1.setFrameShadow(QtWidgets.QFrame.Raised)
        # 设置背景颜色，包括边框颜色
        # self.label.setStyleSheet()
        self.state1.setFrameShape(QFrame.Box)
        self.state1.setAlignment(Qt.AlignCenter) 
        self.state1.setStyleSheet("QLabel{font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")  
        
        self.state2 = QtWidgets.QLabel("短路", self.form2)
        # 显示位置与大小：(x, y, w, h)
        self.state2.setGeometry(850, 320, 70, 40)
        self.state2.setFrameShape(QtWidgets.QFrame.Box)
        # 设置阴影 据说只有加了这步才能设置边框颜色。///可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
        self.state2.setFrameShadow(QtWidgets.QFrame.Raised)
        # 设置背景颜色，包括边框颜色
        # self.label.setStyleSheet()
        self.state2.setFrameShape(QFrame.Box)
        self.state2.setAlignment(Qt.AlignCenter) 
        self.state2.setStyleSheet("QLabel{font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")        
        
        self.state3 = QtWidgets.QLabel("开路", self.form2)
        # 显示位置与大小：(x, y, w, h)
        self.state3.setGeometry(850, 380, 70, 40)
        self.state3.setFrameShape(QtWidgets.QFrame.Box)
        # 设置阴影 据说只有加了这步才能设置边框颜色。///可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
        self.state3.setFrameShadow(QtWidgets.QFrame.Raised)
        # 设置背景颜色，包括边框颜色
        # self.label.setStyleSheet()
        self.state3.setFrameShape(QFrame.Box)
        self.state3.setAlignment(Qt.AlignCenter) 
        self.state3.setStyleSheet("QLabel{font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")  

        self.state4 = QtWidgets.QLabel("阴影", self.form2)
        # 显示位置与大小：(x, y, w, h)
        self.state4.setGeometry(850, 440, 70, 40)
        self.state4.setFrameShape(QtWidgets.QFrame.Box)
        # 设置阴影 据说只有加了这步才能设置边框颜色。///可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
        self.state4.setFrameShadow(QtWidgets.QFrame.Raised)
        # 设置背景颜色，包括边框颜色
        # self.label.setStyleSheet()
        self.state4.setFrameShape(QFrame.Box)
        self.state4.setAlignment(Qt.AlignCenter) 
        self.state4.setStyleSheet("QLabel{font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")  

        self.startbutton=QtWidgets.QPushButton(self.form2)
        self.startbutton.setGeometry(1000, 230, 70, 200)
        self.startbutton.setText("状\n态\n在\n线\n学\n习")
        self.startbutton.setStyleSheet("QPushButton{color:rgb(0,0,0);border-color:rgb(170, 150, 163);background-color: rgb(170, 150, 163);}"
                                  "QPushButton::hover{color:rgb(58,164,98)}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.startbutton.setFont(self.font)
        
        
        
        
        self.LineDisplayGB1= QtWidgets.QWidget(self.form3)
        self.LineDisplayGB1.setObjectName("LineDisplayGB1")
        self.LineDisplayGB1.setGeometry(QtCore.QRect(160, 180, 500, 400))
        
        #日期框
        self.yearbox1 = QtWidgets.QComboBox(self.form3)

        self.yearbox1.addItem("2024")
        self.yearbox1.addItems(["2023", "2022", "2021"])
        self.yearlabel1=QtWidgets.QLabel("年",self.form3)
        self.yearbox1.setGeometry(200, 130, 60, 30)
        self.yearlabel1.setGeometry(260, 130, 20, 30)
        self.monthbox1 = QtWidgets.QComboBox(self.form3)
        self.monthbox1.addItem("2")
        self.monthbox1.addItems(["1", "3", "4","5","6","7","8","9"])
        self.monthlabel1=QtWidgets.QLabel("月",self.form3)
        self.monthbox1.setGeometry(280, 130, 60, 30)
        self.monthlabel1.setGeometry(340, 130, 20, 30)
        self.datebox1 = QtWidgets.QComboBox(self.form3)
        self.datebox1.addItem("2")
        self.datebox1.addItems(["1", "3", "4","5","6","7","8","9"])
        self.datelabel1=QtWidgets.QLabel("日",self.form3)
        self.datebox1.setGeometry(360, 130, 60, 30)
        self.datelabel1.setGeometry(420, 130, 20, 30)
        
        #退出键
        self.exitbutton1=QtWidgets.QPushButton("退出",self.form3)
        self.exitbutton1.setGeometry(800,130,60,30)
        self.exitbutton1.setStyleSheet("QPushButton{color:rgb(0,0,0);border-color:rgb(170, 150, 163);background-color: rgb(170, 150, 163);}"
                                  "QPushButton::hover{color:rgb(58,164,98)}"
                                  "QPushButton:pressed{color:rgb(0,0,0);border:none;}"
                                    )
        self.exitbutton1.setFont(self.font)
        
        self.state_0 = QtWidgets.QLabel("状态检测结果分析", self.form3)
        # 显示位置与大小：(x, y, w, h)
        self.state_0.setGeometry(690, 200, 200, 40)
        self.state_0.setFrameShape(QtWidgets.QFrame.Box)
        # 设置阴影 据说只有加了这步才能设置边框颜色。///可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
        self.state_0.setFrameShadow(QtWidgets.QFrame.Raised)
        # 设置背景颜色，包括边框颜色
        # self.label.setStyleSheet()
        self.state_0.setFrameShape(QFrame.Box)
        self.state_0.setAlignment(Qt.AlignCenter) 
        self.state_0.setStyleSheet("QLabel{font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")
        
        self.gridmenu=QtWidgets.QWidget(self.form3)
        self.gridmenu.setObjectName("gridmenu")
        # 设置窗口的左上角x,y,窗口的width和height
        self.gridmenu.setGeometry(QtCore.QRect(690,250,400,300))
        self.grid=QtWidgets.QGridLayout(self.gridmenu)
        self.grid.setSpacing(10)  

        self.state_1 = QtWidgets.QLabel("正常")
        self.grid.addWidget(self.state_1,0,0)
        # 显示位置与大小：(x, y, w, h)
        self.state_1.setFrameShape(QtWidgets.QFrame.Box)
        # 设置阴影 据说只有加了这步才能设置边框颜色。///可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
        self.state_1.setFrameShadow(QtWidgets.QFrame.Raised)
        # 设置背景颜色，包括边框颜色
        # self.label.setStyleSheet()
        self.state_1.setFrameShape(QFrame.Box)
        self.state_1.setAlignment(Qt.AlignCenter) 
        self.state_1.setStyleSheet("QLabel{color:green;font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")
        
        self.state_2 = QtWidgets.QLabel("短路")
        self.grid.addWidget(self.state_2,1,0)
        # 显示位置与大小：(x, y, w, h)
        self.state_2.setFrameShape(QtWidgets.QFrame.Box)
        # 设置阴影 据说只有加了这步才能设置边框颜色。///可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
        self.state_2.setFrameShadow(QtWidgets.QFrame.Raised)
        # 设置背景颜色，包括边框颜色
        # self.label.setStyleSheet()
        self.state_2.setFrameShape(QFrame.Box)
        self.state_2.setAlignment(Qt.AlignCenter) 
        self.state_2.setStyleSheet("QLabel{color:red;font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")
        
        self.state_3 = QtWidgets.QLabel("开路")
        self.grid.addWidget(self.state_3,2,0)
        # 显示位置与大小：(x, y, w, h)
        self.state_3.setFrameShape(QtWidgets.QFrame.Box)
        # 设置阴影 据说只有加了这步才能设置边框颜色。///可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
        self.state_3.setFrameShadow(QtWidgets.QFrame.Raised)
        # 设置背景颜色，包括边框颜色
        # self.label.setStyleSheet()
        self.state_3.setFrameShape(QFrame.Box)
        self.state_3.setAlignment(Qt.AlignCenter) 
        self.state_3.setStyleSheet("QLabel{color:rgb(255,165,0);font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")

        self.state_4 = QtWidgets.QLabel("阴影")
        self.grid.addWidget(self.state_4,3,0)
        # 显示位置与大小：(x, y, w, h)
        self.state_4.setFrameShape(QtWidgets.QFrame.Box)
        # 设置阴影 据说只有加了这步才能设置边框颜色。///可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
        self.state_4.setFrameShadow(QtWidgets.QFrame.Raised)
        # 设置背景颜色，包括边框颜色
        # self.label.setStyleSheet()
        self.state_4.setFrameShape(QFrame.Box)
        self.state_4.setAlignment(Qt.AlignCenter) 
        self.state_4.setStyleSheet("QLabel{color:blue;font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")
        for i in range(0,4):
          j=1
          my_state_5 = QtWidgets.QLabel("占比:")
          self.grid.addWidget(my_state_5,i,j)
        # 显示位置与大小：(x, y, w, h)
          my_state_5.setFrameShape(QtWidgets.QFrame.Box)
        # 设置阴影 据说只有加了这步才能设置边框颜色。///可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
          my_state_5.setFrameShadow(QtWidgets.QFrame.Raised)
        # 设置背景颜色，包括边框颜色
        # self.label.setStyleSheet()
          my_state_5.setFrameShape(QFrame.Box)
          my_state_5.setAlignment(Qt.AlignCenter) 
          my_state_5.setStyleSheet("QLabel{font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")
          j=j+1
          
          my_state_6 = QtWidgets.QLabel("准确率:")
          self.grid.addWidget(my_state_6 ,i,j)
          # 显示位置与大小：(x, y, w, h)
          my_state_6 .setFrameShape(QtWidgets.QFrame.Box)
        # 设置阴影 据说只有加了这步才能设置边框颜色。///可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
          my_state_6 .setFrameShadow(QtWidgets.QFrame.Raised)
        # 设置背景颜色，包括边框颜色
        # self.label.setStyleSheet()
          my_state_6 .setFrameShape(QFrame.Box)
          my_state_6 .setAlignment(Qt.AlignCenter) 
          my_state_6 .setStyleSheet("QLabel{font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")
          j=j+1
          
          my_state_7  = QtWidgets.QLabel("精确率:")
          self.grid.addWidget(my_state_7,i,j)
        # 显示位置与大小：(x, y, w, h)
          my_state_7.setFrameShape(QtWidgets.QFrame.Box)
        # 设置阴影 据说只有加了这步才能设置边框颜色。///可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
          my_state_7.setFrameShadow(QtWidgets.QFrame.Raised)
        # 设置背景颜色，包括边框颜色
        # self.label.setStyleSheet()
          my_state_7.setFrameShape(QFrame.Box)
          my_state_7.setAlignment(Qt.AlignCenter) 
          my_state_7.setStyleSheet("QLabel{font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")
          j=j+1
          
          my_state_8 = QtWidgets.QLabel("找回率:")
          self.grid.addWidget(my_state_8,i,j)
        # 显示位置与大小：(x, y, w, h)
          my_state_8.setFrameShape(QtWidgets.QFrame.Box)
        # 设置阴影 据说只有加了这步才能设置边框颜色。///可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
          my_state_8.setFrameShadow(QtWidgets.QFrame.Raised)
        # 设置背景颜色，包括边框颜色
        # self.label.setStyleSheet()
          my_state_8.setFrameShape(QFrame.Box)
          my_state_8.setAlignment(Qt.AlignCenter) 
          my_state_8.setStyleSheet("QLabel{font-size:30px;font-weight:normal;font-family:Arial;border-width: 1px;border-style: solid;border-color: black;}")
        


        
        
        # self.table=QtWidgets.QTableWidget(self.form3)
        # self.table.setGeometry(QtCore.QRect(50, 350, 400, 200))
        # self.table.setObjectName("table")
        # self.table.setRowCount(self.num)
        # self.table.setColumnCount(4)
        # self.table.setHorizontalHeaderLabels(['电压(V)','电流(A)','功率(W)','时间'])
        # self.table.setVerticalHeaderLabels(self.a)
        


        # x4=0
        # for i in range(0,self.num):
        #   for j in range(0,4):
        #    if j==0:
        #     x1 = random.uniform(0,100)
        #     item1 = QtWidgets.QTableWidgetItem(str(x1))
        #     self.table.setItem(i,j,item1)
        #    if j==1:
        #     x2 = random.uniform(0,100)
        #     item2 = QtWidgets.QTableWidgetItem(str(x2))
        #     self.table.setItem(i, j, item2)
        #    if j==2:
        #     x3 = x1*x2
        #     item3 = QtWidgets.QTableWidgetItem(str(x3))
        #     self.table.setItem(i, j, item3)
        #    if j==3:
        #     item4 = QtWidgets.QTableWidgetItem(str(x4))

        #     self.table.setItem(i, j, item4)
        #   temp=[x1,x2,x3,x4]
        #   x4=x4+1
        #   self.data.append(temp)

        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        

        

        
        
        
      
        self.stackedWidget=QtWidgets.QStackedWidget()
        self.Layout = QVBoxLayout(self.centralwidget)
        self.Layout.addWidget(self.stackedWidget)
        self.stackedWidget.addWidget(self.form1)
        self.stackedWidget.addWidget(self.form2)
        self.stackedWidget.addWidget(self.form3)
        

        
  
        
      

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        
    def update_table_data(self):
        self.table.clearContents()  # 清空表格数据
        a=[]
        self.data=[]
        if self.num > 0:
            self.table.setRowCount(self.num)
            self.a = [str(i) for i in range(1, self.num+1)]
            self.table.setVerticalHeaderLabels(self.a)


            x4=0
            #my_temp=eng.myls(0, 100,self.num)
            for i in range(0,self.num):

             for j in range(0,4):
              if j==0:
                x1 = random.uniform(0,100)

                #x1=my_temp[i][j]
                item1 = QtWidgets.QTableWidgetItem(str(x1))
                self.table.setItem(i,j,item1)
              if j==1:
                x2 = random.uniform(0,100)
                #x2 = my_temp[i][j]
                item2 = QtWidgets.QTableWidgetItem(str(x2))
                self.table.setItem(i, j, item2)
              if j==2:
                x3 = x1*x2
                item3 = QtWidgets.QTableWidgetItem(str(x3))
                self.table.setItem(i, j, item3)
              if j==3:
                item4 = QtWidgets.QTableWidgetItem(str(x4))

                self.table.setItem(i, j, item4)
             temp=[x1,x2,x3,x4]
             x4=x4+1
             self.data.append(temp)
      
    def slot(self,id):
        self.id=id
    def gotoanother0(self):
        self.stackedWidget.setCurrentIndex(0)
    def gotoanother1(self):
        self.stackedWidget.setCurrentIndex(1)
    def gotoanother2(self):
        self.stackedWidget.setCurrentIndex(2)
    
          
        
        
        
        
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))





