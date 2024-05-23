import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class FirstMainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('主界面')

        ###### 创建界面 ######
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.Layout = QVBoxLayout(self.centralwidget)

        # 设置顶部三个按钮
        self.topwidget = QWidget()

        self.buttonLayout = QHBoxLayout(self.topwidget)

        self.pushButton1 = QPushButton()
        self.pushButton1.setText("第一面板")
        self.buttonLayout.addWidget(self.pushButton1)

        self.pushButton2 = QPushButton()
        self.pushButton2.setText("第二面板")
        self.buttonLayout.addWidget(self.pushButton2)

        self.pushButton3 = QPushButton()
        self.pushButton3.setText("第三面板")
        self.buttonLayout.addWidget(self.pushButton3)

        self.Layout.addWidget(self.topwidget)

        # 设置stackedWidget
        self.stackedWidget = QStackedWidget()
        self.Layout.addWidget(self.stackedWidget)

        # 设置第一个面板
        self.form1 = QWidget()
        self.formLayout1 = QHBoxLayout(self.form1)
        self.label1 = QLabel()
        self.label1.setText("第一个面板")
        self.label1.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setFont(QFont("Roman times", 50, QFont.Bold))
        self.formLayout1.addWidget(self.label1)

        # 设置第二个面板
        self.form2 = QWidget()
        self.formLayout2 = QHBoxLayout(self.form2)
        self.label2 = QLabel()
        self.label2.setText("第二个面板")
        self.label2.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setFont(QFont("Roman times", 50, QFont.Bold))
        self.formLayout2.addWidget(self.label2)

        # 设置第三个面板
        self.form3 = QWidget()
        self.formLayout3 = QHBoxLayout(self.form3)
        self.label3 = QLabel()
        self.label3.setText("第三个面板")
        self.label3.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.label3.setAlignment(Qt.AlignCenter)
        self.label3.setFont(QFont("Roman times", 50, QFont.Bold))
        self.formLayout3.addWidget(self.label3)

        # 将三个面板，加入stackedWidget
        self.stackedWidget.addWidget(self.form1)
        self.stackedWidget.addWidget(self.form2)
        self.stackedWidget.addWidget(self.form3)

        # 设置状态栏
        self.statusBar().showMessage("当前用户")

        # 窗口最大化
        self.showMaximized()

        ###### 三个按钮事件 ######
        self.pushButton1.clicked.connect(self.on_pushButton1_clicked)
        self.pushButton2.clicked.connect(self.on_pushButton2_clicked)
        self.pushButton3.clicked.connect(self.on_pushButton3_clicked)

    # 按钮一：打开第一个面板
    def on_pushButton1_clicked(self):
        self.stackedWidget.setCurrentIndex(0)

    # 按钮二：打开第二个面板
    def on_pushButton2_clicked(self):
        self.stackedWidget.setCurrentIndex(1)

    # 按钮三：打开第三个面板
    def on_pushButton3_clicked(self):
        self.stackedWidget.setCurrentIndex(2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    the_mainwindow = FirstMainWindow()
    the_mainwindow.show()
    sys.exit(app.exec_())
