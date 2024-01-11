"""
Файл для повторения темы QThread

Напомнить про работу с QThread.

Предлагается создать небольшое приложение, которое будет с помощью модуля request
получать доступность того или иного сайта (возвращать из потока status_code сайта).

Поработать с сигналами, которые возникают при запуске/остановке потока,
передать данные в поток (в данном случае url),
получить данные из потока (статус код сайта),
попробовать управлять потоком (запуск, остановка).

Опционально поработать с валидацией url
"""
import re
import time

import requests
from PySide6 import QtWidgets, QtCore, QtGui

# URL_REGEX = '^(https?:\/\/)?((([a-z0-9-]+\.)+([a-z]{2,}))|((\d{1,3}\.){3}\d{1,3}))(:\d{1,5})?$/i'
def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if re.match(regex, url):
        return True
    return False

class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.request_thread = RequestTread()

        self.initUi()
        self.initSignals()

    def initUi(self):
        self.lineEditUrl = QtWidgets.QLineEdit()
        self.lineEditUrl.setPlaceholderText("URL-адрес")
        # self.lineEditUrl.setValidator(QtGui.QRegularExpressionValidator(URL_REGEX))

        self.pbPing = QtWidgets.QPushButton("Ping")
        self.pbPing.setCheckable(True)

        label = QtWidgets.QLabel("Время повтора, с")
        self.spinBoxDelay = QtWidgets.QSpinBox()
        self.spinBoxDelay.setMinimum(1)

        self.plainTextEditLog = QtWidgets.QPlainTextEdit()
        self.plainTextEditLog.setReadOnly(True)

        l_settings = QtWidgets.QHBoxLayout()
        l_settings.addWidget(label)
        l_settings.addWidget(self.spinBoxDelay)
        l_settings.addWidget(self.pbPing)

        l = QtWidgets.QVBoxLayout()
        l.addWidget(self.lineEditUrl)
        l.addLayout(l_settings)
        l.addWidget(self.plainTextEditLog)

        self.setLayout(l)

    def initSignals(self) -> None:
        """

        :return:
        """
        self.pbPing.clicked.connect(self.onPbPingClicked)
        self.spinBoxDelay.valueChanged.connect(self.request_thread.setDelay)
        self.lineEditUrl.textChanged.connect(self.lineEditUrlTextChanged)
        self.request_thread.responsed.connect(
            lambda data: self.plainTextEditLog.appendPlainText(
                f"{time.ctime()} >>> Статус сайта: {'не существует' if data == -1 else data}"))

        self.request_thread.started.connect(lambda: self.spinBoxDelay.setEnabled(False))
        self.request_thread.finished.connect(lambda: self.spinBoxDelay.setEnabled(True))

    def onPbPingClicked(self) -> None:
        """

        :return:
        """
        if self.request_thread.isRunning():
            self.request_thread.status = False
            return

        if not is_valid_url(self.lineEditUrl.text()):
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Неправильный адрес")
            self.pbPing.setChecked(False)
            return

        self.request_thread.url = self.lineEditUrl.text()
        self.request_thread.delay = self.spinBoxDelay.value()
        self.request_thread.start()

    def lineEditUrlTextChanged(self, url):
        if is_valid_url(url):
            self.lineEditUrl.setStyleSheet("background-color: green")
        else:
            self.lineEditUrl.setStyleSheet("background-color: orange")



class RequestTread(QtCore.QThread):
    responsed = QtCore.Signal(int)
    def __init__(self, parent=None):
        super().__init__(parent)

        self.delay = None
        self.url = None
        self.status = None

    def setDelay(self, delay):
        self.delay = delay

    def run(self) -> None:

        if self.delay is None and self.url is None:
            return

        self.status = True

        while self.status:
            try:
                response = requests.get(self.url)
                self.responsed.emit(response.status_code)
            except requests.exceptions.MissingSchema:
                self.responsed.emit(-1)

            time.sleep(self.delay)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    # t = RequestTread()
    # t.delay = 5
    # t.url = 'https://dl-ido.spbstu.ru'
    # t.responsed.connect(lambda data: print(data))
    # t.start()

    app.exec()
