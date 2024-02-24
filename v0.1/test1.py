import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QDesktopWidget,QWidget,QGridLayout,QComboBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from functools import partial
import untitled
import test2
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


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import matlab
import matlab.engine
eng = matlab.engine.start_matlab()
eng.cd("C:\\Users\\whitefork\\Desktop\\python\\myproject\\test",nargout=0)
label=['正常','短路','开路','阴影']
yticks=[1.0,2.0,3.0,4.0]


    


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
    x=[]
    y_test=[]
    y_pred=[]
    y_test_label=[]
    y_pred_label=[]
    count=0
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
        self.PrepareLineCanvas()


    def PrepareSamples(self):
        
     # 获取 y_pred 结果
        [self.y_test_label,self.y_pred_label]=eng.test(nargout=2)

        for temp in self.y_pred_label:
         self.x.append(self.count)
         self.y_pred.append(int(temp[0]))
         self.count=self.count+1
        for temp in self.y_test_label:
         self.y_test.append(int(temp[0]))

    def PrepareLineCanvas(self):
        self.LineFigure = Figure_Canvas()
        self.LineFigureLayout = QGridLayout(self.LineDisplayGB)
        self.LineFigureLayout.addWidget(self.LineFigure)
        self.LineFigure1 = Figure_Canvas()
        self.LineFigureLayout1 = QGridLayout(self.LineDisplayGB1)
        self.LineFigureLayout1.addWidget(self.LineFigure1)

        self.LineFigure.ax.set_xlim(np.min(self.x), np.max(self.x))
        self.LineFigure1.ax.set_xlim(np.min(self.x), np.max(self.x))
        self.LineFigure.ax.set_ylim(0, 6)
 
        self.line = Line2D(self.x, self.y_test)
        self.line.set_color('red') 
        self.line.set_label("测试集的标签")
        self.LineFigure.ax.set_yticks(yticks,label)  
        self.LineFigure.ax.add_line(self.line)
        self.line1 = Line2D(self.x, self.y_pred)
        self.line1.set_color('blue') 
        self.line1.set_label("预测后的测试集的标签") 
        self.LineFigure.ax.add_line(self.line1)
        
        self.line2 = Line2D(self.x, self.y_test)
        self.line2.set_color('red') 
        self.line2.set_label("测试集的标签")
        self.line3 = Line2D(self.x, self.y_pred)
        self.line3.set_color('blue') 
        self.line3.set_label("预测后的测试集的标签") 
        self.LineFigure1.ax.set_yticks(yticks,label)  
        self.LineFigure1.ax.add_line(self.line2)
        self.LineFigure1.ax.add_line(self.line3)
        




        self.LineFigure.ax.legend()

        self.LineFigure.ax.set_xlabel("时间")
        self.LineFigure.ax.set_ylabel("标签")
        
        self.LineFigure1.ax.legend()
        self.LineFigure1.ax.set_xlabel("时间")
        self.LineFigure1.ax.set_ylabel("标签")


        
       
    # def changeLineCanvas(self):
    #     if len(self.x)!=0:
    #        self.LineFigure.ax.set_xlim(np.min(self.x), np.max(self.x))
    #     temp1=0.0
    #     temp2=0.0
    #     temp=""

    #     if self.voltage_state==True:
    #         temp1=np.min(self.y)
    #         temp2=np.max(self.y)
    #         self.line = Line2D(self.x, self.y)
    #         self.line.set_color('red')
    #         self.line.set_label("电压")

    
    #         self.LineFigure.ax.add_line(self.line)
    #         self.LineFigure.ax.legend()
    #         temp=temp+"电压\V  "
    #     if self.current_state==True:
    #         temp1=min(temp1,np.min(self.z))
    #         temp2=max(temp2,np.max(self.z))
    #         self.line1 = Line2D(self.x, self.z)
    #         self.line1.set_color('blue')
    #         self.line1.set_label("电流")

    #         self.LineFigure.ax.add_line(self.line1)
    #         self.LineFigure.ax.legend() 
    #         temp=temp+"电流\A  "
    #     if self.power_state==True:
    #         temp1=min(temp1,np.min(self.r))
    #         temp2=max(temp2,np.max(self.r))
    #         self.line2 = Line2D(self.x, self.r)
    #         self.line2.set_color('green')
    #         self.line2.set_label("功率") 
    #         self.LineFigure.ax.legend(['功率'])      
    #         self.LineFigure.ax.add_line(self.line2)
    #         self.LineFigure.ax.legend() 
    #         temp=temp+"功率\W  "
            
        
        

    #     self.LineFigure.ax.set_ylim(temp1, temp2+10)
    #     self.LineFigure.ax.set_xlabel("时间")
    #     self.LineFigure.ax.set_ylabel(temp)

    
    # def changeBarCanvas(self):
    #     if len(self.x)!=0:
    #        self.LineFigure.ax.set_xlim(-2, np.max(self.x)+2)
    #     temp1=0.0
    #     temp2=0.0
    #     temp=""
    #     if self.voltage_state==True:

    #         temp2=np.max(self.y)
    #         self.bar = self.LineFigure.ax.bar(self.x, self.y, width=0.4)

    #         self.patches = self.bar.patches   

    #         self.bar.set_label("电压")
    #         temp1=temp1+1

    #         self.LineFigure.ax.legend()
    #         temp=temp+"电压\V  "
    #     if self.current_state==True:

    #         temp2=max(temp2,np.max(self.z))
    #         self.bar = self.LineFigure.ax.bar([i+0.4*temp1 for i in range(len(self.x))], self.z, width=0.4)
    #         self.patches = self.patches+self.bar.patches               
    #         self.bar.set_label("电流")
    #         temp1=temp1+1
    #         self.LineFigure.ax.legend()
    #         temp=temp+"电流\A  "
    #     if self.power_state==True:
    #         temp1=temp1+1
    #         temp2=max(temp2,np.max(self.r))
    #         self.bar = self.LineFigure.ax.bar([i+0.4*temp1 for i in range(len(self.x))], self.r, width=0.4)
    #         self.patches = self.patches+self.bar.patches               
    #         self.bar.set_label("功率")
    #         temp1=temp1+1
    #         self.LineFigure.ax.legend()
    #         temp=temp+"功率\A  "

    #     self.LineFigure.ax.set_ylim(0, temp2+10)
    #     self.LineFigure.ax.set_xlabel("时间")
    #     self.LineFigure.ax.set_ylabel(temp)

    
    
    # def UpdateImgs(self):
    #     self.x=[]
    #     self.y=[]
    #     self.r=[]
    #     self.z=[]
    #     self.LineFigure.clear()
 
    #     self.LineFigure.fig.canvas.draw()  # 这里注意是画布重绘，self.figs.canvas
    #     self.LineFigure.fig.canvas.flush_events()  # 画布刷新self.figs.canvas
    #     self.PrepareSamples()




    # def LineUpdate(self):
    #     self.changeLineCanvas()
    #     self.LineFigure.draw()
    
    # def BarUpdate(self):
    #     self.changeBarCanvas()
    #     '''        
    #     for i in range(len(self.patches)):
    #         self.patches[i].set_height(self.y[i])
    #         '''
    #     self.bar.patches=self.patches
    #     self.LineFigure.draw()
          



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



