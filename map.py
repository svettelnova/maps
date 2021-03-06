import sys
import requests
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QMainWindow, QCheckBox
from PyQt5.QtWidgets import QTextEdit, QErrorMessage, QComboBox
from PyQt5.QtCore import QSize, QBuffer, QByteArray, Qt
from PyQt5.QtGui import QPixmap, QPalette, QColor
from io import BytesIO
from PIL import Image


class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scale = 6
        self.longitude = 56
        self.latitude = 56
        self.pt_longitude = 0
        self.pt_latitude = 0
        self.delta_longitude = 2
        self.delta_latitude = 2
        self.layer = "map"
        self.address = ''
        self.post_code = ""
        self.initUI()
        self.loadMap()

    def initUI(self):
        self.setGeometry(100, 100, 1060, 760)
        self.setWindowTitle("Карта")
        self.txt_search = QTextEdit('', self)
        self.txt_search.move(10, 10)
        self.txt_search.resize(QSize(600, 30))
        self.btn = QPushButton('Искать', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(self.txt_search.geometry().right() + 10, 10)
        self.btn.clicked.connect(self.search)
        self.btn_delete = QPushButton('Сброс', self)
        self.btn_delete.resize(self.btn_delete.sizeHint())
        self.btn_delete.move(self.btn.geometry().right() + 10, 10)
        self.btn_delete.clicked.connect(self.discharge)
        self.layers = ['map', 'sat', 'sat,skl']
        self.btn_layers = QComboBox(self)
        self.btn_layers.addItems(self.layers)
        self.btn_layers.resize(self.btn_layers.sizeHint())
        self.btn_layers.move(self.btn_delete.geometry().right() + 100, 10)
        self.btn_layers.currentIndexChanged.connect(self.layer_changed)
        self.cb_include_post_code = QCheckBox('Включить почтовый индекс в адрес', self)
        self.cb_include_post_code.resize(self.cb_include_post_code.sizeHint())
        self.cb_include_post_code.move(10, 50)
        self.cb_include_post_code.clicked.connect(self.post_code_changed)
        self.lb_full_address = QLabel(self)
        self.lb_full_address.move(self.cb_include_post_code.geometry().right() + 10, 50)

        self.mapView = QLabel(self)
        self.mapView.move(10, 90)
        self.mapView.resize(1040, 660)
        self.txt_search.keyPressEvent = self.keyPressEvent
        self.lb_errortext = QLabel("test", self)
        self.lb_errortext.move(10, self.mapView.geometry().top() + 5)
        self.lb_errortext.setStyleSheet("font: 18pt Comic Sans MS;color:red")

    def layer_changed(self, index):
        self.layer = self.layers[index]
        self.loadMap()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown and self.scale > 1:
            self.scale -= 1
            self.loadMap()
        if event.key() == Qt.Key_PageUp and self.scale < 17:
            self.scale += 1
            self.loadMap()
        if event.key() == Qt.Key_Up:
            if self.delta_latitude > 0 and self.latitude < 90 - self.delta_latitude:
                self.latitude += self.delta_latitude
                if self.latitude > 90:
                    self.latitude = 90
                self.loadMap()
        if event.key() == Qt.Key_Down:
            if self.delta_latitude > 0 and self.latitude > -90 + self.delta_latitude:
                self.latitude -= self.delta_latitude
                if self.latitude < -90:
                    self.latitude = -90
                self.loadMap()
        if event.key() == Qt.Key_Right:
            if self.delta_longitude > 0 and self.longitude < 180 - self.delta_longitude:
                self.longitude += self.delta_longitude
                if self.longitude > 180:
                    self.longitude = 180
                self.loadMap()
        if event.key() == Qt.Key_Left:
            if self.delta_longitude > 0 and self.longitude > -180 + self.delta_longitude:
                self.longitude -= self.delta_longitude
                if self.longitude < -180:
                    self.longitude = -180
                self.loadMap()
        event.ignore()
        return QTextEdit.keyPressEvent(self.txt_search, event)

    def show_error(self, error):
        self.lb_errortext.setText(error)
        self.lb_errortext.resize(self.lb_errortext.sizeHint())

    def search(self):
        toponym_to_find = self.txt_search.toPlainText()
        if toponym_to_find == '':
            self.show_error('Введите адрес.')
            return
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": toponym_to_find,
            "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params)

        if not response:
            self.show_error('Ошибка выполнения запроса: ' + response.reason)
            return
        self.show_error('')

        # Преобразуем ответ в json-объект
        json_response = response.json()
        # Получаем первый топоним из ответа геокодера.
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        # Координаты центра топонима:
        toponym_coodrinates = toponym["Point"]["pos"]
        self.longitude, self.latitude = map(float, toponym_coodrinates.split(" "))
        self.pt_longitude = self.longitude
        self.pt_latitude = self.latitude
        envelope = toponym['boundedBy']['Envelope']
        lb = envelope['lowerCorner'].split()
        lb_long, lb_lat = float(lb[0]), float(lb[1])
        rt = envelope['upperCorner'].split()
        rt_long, rt_lat = float(rt[0]), float(rt[1])
        self.delta_latitude = abs(rt_lat - lb_lat)
        self.delta_longitude = abs(rt_long - lb_long)
        address = toponym['metaDataProperty']['GeocoderMetaData']['Address']
        self.address = address['formatted']
        if ('postal_code' in address):
            self.post_code = address['postal_code']
        else:
            self.post_code = ''
        self.post_code_changed()
        self.loadMap()

    def loadMap(self):
        coord = ",".join([str(self.longitude), str(self.latitude)])
        pt_coord = ",".join([str(self.pt_longitude), str(self.pt_latitude)])
        # Собираем параметры для запроса к StaticMapsAPI:
        map_params = {
            "ll": coord,
            "l": self.layer,
            "z": self.scale,
            "size": "650,450",
            "pt": pt_coord + ",pm2rdm"
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        # ... и выполняем запрос
        response = requests.get(map_api_server, params=map_params)
        if not response:
            # обработка ошибочной ситуации
            self.show_error('Ошибка выполнения запроса: ' + response.reason)
            return
        self.show_error('')
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

    def discharge(self):
        self.pt_latitude = 0
        self.pt_longitude = 0
        self.txt_search.setPlainText('')
        self.address = ''
        self.post_code = ''
        self.post_code_changed()
        self.loadMap()

    def post_code_changed(self):
        if self.address == '':
            self.lb_full_address.setText('')
            return
        text = 'Адрес объекта: ' + self.address
        if self.cb_include_post_code.isChecked() and self.post_code != '':
            text += ', почтовый индекс: ' + self.post_code
        self.lb_full_address.setText(text)
        self.lb_full_address.resize(self.lb_full_address.sizeHint())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapWindow()
    ex.show()
    sys.exit(app.exec())
