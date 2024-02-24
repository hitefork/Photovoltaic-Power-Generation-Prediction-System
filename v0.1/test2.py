import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QDesktopWidget,QWidget,QGridLayout,QComboBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from functools import partial

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


class InfomationWindow(QWidget):
    def __init__(self, parent=None):
        super(InfomationWindow, self).__init__(parent)
        self.resize(400, 400)
        self.setStyleSheet("background: white")

    def handle_click(self):
        if not self.isVisible():
            self.show()

    def handle_close(self):
        self.close()

class SecondWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("弹出窗口")
        self.resize(300, 200)

        self.label = QLabel("请选择一个选项：", self)
        self.label.move(20, 20)

        self.button1 = QPushButton("选项1", self)
        self.button1.move(20, 50)
        self.button1.clicked.connect(self.show_message)

        self.button2 = QPushButton("选项2", self)
        self.button2.move(120, 50)
        self.button2.clicked.connect(self.show_input_form)
        
        self.s=InfomationWindow()

    def show_message(self):

        self.s.show()

    def show_input_form(self):
        form_dialog = QDialog(self)
        form_dialog.setWindowTitle("输入表单")
        form_layout = QFormLayout(form_dialog)

        label_name = QLabel("姓名：")
        line_edit_name = QLineEdit()
        form_layout.addRow(label_name, line_edit_name)

        label_age = QLabel("年龄：")
        line_edit_age = QLineEdit()
        form_layout.addRow(label_age, line_edit_age)

        submit_button = QPushButton("提交")
        form_layout.addRow(submit_button)

        form_dialog.exec_()