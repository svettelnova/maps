import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLabel
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ЯндексКартыИлиЕгоПодобие.ui', self)
        #global z

    #def initUI(self):
        #self.pixmap = QPixmap('orig.png')
        #self.MAP.setPixmap(self.pixmap)

    '''def keyPressEvent(self, event):
        if event.key() == Qt.Key_PgUp:
            z += 1
        elif event.key() == Qt.Key_PgDn:
            z -= 1 '''


app = QApplication(sys.argv)
ex = Window()
ex.show()
sys.exit(app.exec())