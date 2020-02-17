import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMainWindow
from PyQt5.QtWidgets import QTextEdit, QErrorMessage
from PyQt5.QtCore import QSize, QBuffer, QByteArray, QEvent, Qt
from PyQt5.QtGui import QPixmap
from io import BytesIO
from PIL import Image


class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scale = 6
        self.longitude = 56
        self.lattitude = 56
        self.initUI()
        self.loadMap()

    def initUI(self):
        self.setGeometry(100, 100, 1060, 780)
        self.setWindowTitle("Карта")
        self.txt_search = QTextEdit('', self)
        self.txt_search.move(10, 10)
        self.txt_search.resize(QSize(800, 30))
        self.btn = QPushButton('Искать', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(self.txt_search.size().width() + 20, 10)
        self.btn.clicked.connect(self.search)

        self.mapView = QLabel(self)
        self.mapView.move(10, 50)
        self.mapView.resize(1040, 720)
        self.txt_search.keyPressEvent = self.keyPressEvent

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown and self.scale > 1:
            self.scale -= 1
            self.loadMap()
        if event.key() == Qt.Key_PageUp and self.scale < 17:
            self.scale += 1
            self.loadMap()
        event.ignore()
        return QTextEdit.keyPressEvent(self.txt_search, event)

    def search(self):
        toponym_to_find = self.txt_search.toPlainText()
        if toponym_to_find == '':
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Введите адрес')
            return
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": toponym_to_find,
            "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params)

        if not response:
            # обработка ошибочной ситуации
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Ошибка выполнения вопроса: ' + response.reason)
            return

        # Преобразуем ответ в json-объект
        json_response = response.json()
        # Получаем первый топоним из ответа геокодера.
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        # Координаты центра топонима:
        toponym_coodrinates = toponym["Point"]["pos"]
        self.longitude, self.lattitude = toponym_coodrinates.split(" ")
        self.loadMap()

    def loadMap(self):
        coord = ",".join([str(self.longitude), str(self.lattitude)])
        # Собираем параметры для запроса к StaticMapsAPI:
        map_params = {
            "ll": coord,
            "l": "map",
            "z": self.scale,
            "size": "650,450"
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        # ... и выполняем запрос
        response = requests.get(map_api_server, params=map_params)
        bytes = BytesIO(response.content)
        img = Image.open(bytes)
        img = img.resize((1040, 720))
        ba = QByteArray()
        buffer = QBuffer(ba)
        buffer.open(QBuffer.ReadWrite)
        img.save(buffer, "PNG")
        buffer.close()
        pixmap = QPixmap()
        pixmap.loadFromData(ba, "PNG")
        self.mapView.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapWindow()
    ex.show()
    sys.exit(app.exec())
