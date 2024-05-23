import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QDesktopWidget,QWidget,QGridLayout,QComboBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt,QTimer
from functools import partial
import untitled
from test2 import NewDialog

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




class LoadingProgress(QtWidgets.QDialog):
    update_signal = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super(LoadingProgress, self).__init__(parent)
        self.value = 0
        self.update_signal.connect(self.update_progress)
        vbox = QtWidgets.QVBoxLayout(self)
        self.steps = [5, 10, 8, 15]  # 模拟每个步骤的时间消耗（以秒为单位）
        self.movie_label = QtWidgets.QLabel()
        self.movie = QtGui.QMovie("loading.gif")
        self.movie_label.setMovie(self.movie)
        self.movie.start()
        self.progress_label = QtWidgets.QLabel()
        self.label_update()

        vbox.addWidget(self.movie_label)
        vbox.addWidget(self.progress_label)
        self.setLayout(vbox)
        self.exec_()
        
    def label_update(self):
        time_consumed = sum(self.steps[:self.value])  # 计算已经完成的步骤的总时间消耗
        self.progress_label.setText(f"已用时间：{time_consumed}秒")

    def update_progress(self, boolean: bool) -> None:
        self.value += 1
        if boolean and self.value < len(self.steps):
            self.label_update()
        else:
            self.close()
