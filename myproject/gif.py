import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
 
class loadingGif(QWidget):
    def __init__(self):
        super(loadingGif, self).__init__()
        self.label=QLabel("",self)
        #fixed  adj. 确定的；固执的
        self.setFixedSize(50,50)

        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint)
        self.movie=QMovie("C:\\Users\\whitefork\\Desktop\\python\\myproject\\gif\\loading.gif")
        self.movie.setScaledSize(QSize(50,50))
        self.label.setMovie(self.movie)
        self.movie.start()
 
 