
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'treewidget.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
import threading
import queue

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(447, 403)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 170, 231, 61))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(18)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(120, 60, 191, 61))
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(26)
        self.label.setFont(font)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 447, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "线程中打开widget"))
        self.label.setText(_translate("MainWindow", "我是主窗体"))


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 234)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(120, 50, 251, 81))
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(26)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "我是弹窗"))


class Main_Test(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Main_Test, self).__init__(parent)
        self.setupUi(self)
        # 实例一个窗体
        self.wd = Widget_Test()
        # 链接槽函数
        self.pushButton.clicked.connect(self.pushbuttonfunc)
        # 为显示子窗口的信号增加槽函数
        self.wd.signal.connect(self.widget_show)

    def pushbuttonfunc(self):
        # 往队列中灌入一个信号
        self.wd.widget_queue.put("show")

    # 显示子窗口
    def widget_show(self):
        self.wd.show()


class Widget_Test(QtWidgets.QWidget, Ui_Form):
    signal = pyqtSignal()

    def __init__(self):
        super(Widget_Test, self).__init__()
        self.setupUi(self)
        # 申请一个消息队列
        self.widget_queue = queue.Queue(maxsize=-1)
        # 初始化一个线程
        self.widget_thread = threading.Thread(target=self.widget_handle)
        # 打开线程
        self.widget_thread.start()

    def send_single(self):
        # 发送信号到主窗体
        self.signal.emit()

    def widget_handle(self):
        while 1:
            # 在队列中获取一个信号
            strinfo = self.widget_queue.get(1)
            print(strinfo)
            if strinfo == "show":
                # 线程中弹出窗体，需要用到信号
                self.send_single()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Main_Test()
    win.show()
    sys.exit(app.exec_())
