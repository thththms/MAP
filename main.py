import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt


class Map(QWidget):
    def __init__(self):
        super().__init__()
        self.request = "https://static-maps.yandex.ru/1.x"
        self.params = {
            "ll": "37.530887,55.703118",
            "spn": "0.002,0.002",
            "l": "map"
        }

        self.initUI()
        self.updateMap(self.params)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            print(1)
            a = float(self.params['spn'].split(',')[0])
            a = a + 0.01 if a + 0.01 < 21 else a
            self.params['spn'] = f'{a},{a}'
            self.updateMap(self.params)
        if event.key() == Qt.Key_PageDown:
            a = float(self.params['spn'].split(',')[0])
            a = a - 0.01 if a - 0.01 > 0 else a

            self.params['spn'] = f'{a},{a}'
            self.updateMap(self.params)

    def updateMap(self, params):
        response = requests.get(self.request, params=params)
        print(self.params['spn'])
        if not response:
            print("Ошибка выполнения запроса:")
            print(self.request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def initUI(self):
        self.setGeometry(100, 100, 600, 450)
        self.setWindowTitle('Карта')
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Map()
    ex.show()
    sys.exit(app.exec())