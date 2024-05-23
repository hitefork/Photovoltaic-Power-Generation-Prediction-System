import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel,QDateEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt,QTimer

class Figure_Canvas(FigureCanvas):

    def __init__(self,parent=None,width=3.9,height=2.7,dpi=100):
        self.fig=Figure(figsize=(width,height),dpi=100)
        super(Figure_Canvas,self).__init__(self.fig)
        self.ax=self.fig.add_subplot(111)
    
    def clear(self):
        self.fig.clf()
        self.ax=self.fig.add_subplot(111)

class NewDialog(QWidget):
    data=[]
    def __init__(self, data):
        super().__init__()
        self.data=data
        self.initUI()
        
    def initUI(self):    
        self.setWindowTitle('单独分析')
        layout = QVBoxLayout()
        layout.setGeometry(QtCore.QRect(0, 100, 600, 400))
        self.setLayout(layout)
        dateLabel = QLabel("选择日期:")
        dateEdit = QDateEdit()
        dateEdit.setDisplayFormat("yyyy-MM-dd")
        dateEdit.setCalendarPopup(True)
        layout.addWidget(dateLabel)
        layout.addWidget(dateEdit)


        self.LineFigure = Figure_Canvas()
        layout.addWidget(self.LineFigure)
        classes = ["正常", "短路", "开路", "阴影"]
        proportion = []
        length = len(self.data)
        for i in self.data:
              for j in i:
                temp = j / (np.sum(i))
                proportion.append(temp)

        pshow = []
        for i in proportion:
            pt = "%.2f%%" % (i * 100)
            pshow.append(pt)
        proportion = np.array(proportion).reshape(length, length)  # reshape(列的长度，行的长度)
        pshow = np.array(pshow).reshape(length, length)

        ax = self.LineFigure.ax
        im = ax.imshow(proportion, interpolation='nearest', cmap=plt.cm.Blues)  # 按照像素显示出矩阵
        ax.set_xticks(np.arange(len(classes)))
        ax.set_yticks(np.arange(len(classes)))
        ax.set_xticklabels(classes, fontsize=12)
        ax.set_yticklabels(classes, fontsize=12)

        thresh = self.data.max() / 2.
        iters = np.reshape([[[i, j] for j in range(length)] for i in range(length)], (self.data.size, 2))
        for i, j in iters:
            if (i == j):
                ax.text(j, i - 0.12, format(self.data[i, j]), va='center', ha='center', fontsize=10, color='white',
                        weight=5)  # 显示对应的数字
            else:
                ax.text(j, i - 0.12, format(self.data[i, j]), va='center', ha='center', fontsize=10)  # 显示对应的数字

        ax.set_ylabel('True label', fontsize=16)
        ax.set_xlabel('Predict label', fontsize=16)
        self.LineFigure.draw()
        self.show()

