import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea, QLabel
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt,QTimer
import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QTimer

class ScrollTextWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 设置垂直滚动条不显示
        # 创建包含状态文本的QLabel
        scroll_area.setStyleSheet("border: none;")  # 移除边框样式

        self.label = QLabel()
        scroll_area.setWidget(self.label)

        layout.addWidget(scroll_area)
        self.setLayout(layout)

        self.setWindowTitle("滚动显示状态数据")

        # 创建一个定时器，用于更新状态
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateStatus)
        self.timer.start(1000)  # 每秒更新一次状态

        self.updateStatus()

    def updateStatus(self):
        # 定义状态和相应的颜色
        status_color_mapping = {
           "": QColor("white"),
           "": QColor("white"),
            "正常": QColor("green"),
            "短路": QColor("red"),
            "开路": QColor("blue"),
            "阴影": QColor("yellow"),
           "": QColor("white"),
           "": QColor("white"),
           "": QColor("white"),
        }

        # 随机选择一个状态
        selected_status = random.choice(list(status_color_mapping.keys()))
        if selected_status=='正常':
            scroll_bar = self.layout().itemAt(0).widget().verticalScrollBar()
            scroll_bar.setValue(0)  # 将滚动条设置到位置50
        if selected_status=='短路':
            scroll_bar = self.layout().itemAt(0).widget().verticalScrollBar()
            scroll_bar.setValue(25)  # 将滚动条设置到位置50
        if selected_status=='开路':
            scroll_bar = self.layout().itemAt(0).widget().verticalScrollBar()
            scroll_bar.setValue(50)  # 将滚动条设置到位置50
        if selected_status=='阴影':
            scroll_bar = self.layout().itemAt(0).widget().verticalScrollBar()
            scroll_bar.setValue(100)  # 将滚动条设置到位置50
        # 更新QLabel的文本和样式
        text = ""
        for status, color in status_color_mapping.items():
            if status == selected_status and status :
                # 如果是选择的状态，设置字体大一点，颜色与其他状态不同
                text += f"<span style='font-size: 22pt; color: {color.name()}'>{status}</span><br>"
            else:
                # 其他状态设置默认样式
                text += f"<span style='font-size: 16pt; color: gray'>{status}</span><br>"
        
        self.label.setText(text)
                # 将滚动条滚动到固定位置




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScrollTextWidget()
    window.show()
    sys.exit(app.exec_())
