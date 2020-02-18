import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLabel
from PyQt5 import uic
from PyQt5.QtCore import QSize, QBuffer, QByteArray, QEvent, Qt
from PyQt5.QtGui import QPixmap
import sys
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image


z = 5
mainmap = "http://static-maps.yandex.ru/1.x/?ll=37.6214,54.1552&spn=0.002,0.002&l=map"

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ЯндексКартыИлиЕгоПодобие.ui', self)
        self.loadMap()
        self.longitude = 79
        self.lattitude = 79
        global z
        self.POISK.clicked.connect(self.found)
        self.SBROS.clicked.connect(self.delete)

    def getImage(self):
        map_request = mainmap
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.pixmap = QPixmap(self.map_file)
        self.MAP.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown and self.z > 1:
            self.z -= 1
            self.loadMap()
        if event.key() == Qt.Key_PageUp and self.z < 17:
            self.z += 1
            self.loadMap()
        event.ignore()
        return QTextEdit.keyPressEvent(self.MAP, event)

    def found(self):
        map_request = self.OKNOPOISKA.text()

    def delete(self):
        map_request = mainmap

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def search(self):
        toponym_to_find = self.txt_search.toPlainText()
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
                "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                "geocode": toponym_to_find,
                "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

# Преобразуем ответ в json-объект
        json_response = response.json()
# Получаем первый топоним из ответа геокодера.
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
# Координаты центра топонима:
        toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

        delta = "0.005"

# Собираем параметры для запроса к StaticMapsAPI:
        map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "spn": ",".join([delta, delta]),
            "l": "map",
            "z": z
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
        response = requests.get(map_api_server, params=map_params)

        Image.open(BytesIO(
            response.content)).show()
# Создадим картинку
# и тут же ее покажем встроенным просмотрщиком операционной системы


app = QApplication(sys.argv)
ex = Window()
ex.show()
sys.exit(app.exec())