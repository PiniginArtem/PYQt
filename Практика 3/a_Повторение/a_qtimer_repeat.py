"""
Файл для повторения темы QTimer

Напомнить про работу с QTimer.

Предлагается создать приложение-которое будет
с некоторой периодичностью вызывать определённую функцию.
"""
import time

from PySide6 import QtWidgets, QtCore


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.timer = QtCore.QTimer()

        self.initUi()
        self.initSignals()

    def initUi(self) -> None:
        """

        :return:
        """

        self.setWindowTitle('Работа с таймером')
        self.setFixedSize(400, 300)

        self.labelTempDescription = QtWidgets.QLabel()

        self.pbHandle = QtWidgets.QPushButton('Старт')
        self.pbHandle.setCheckable(True)

        l = QtWidgets.QVBoxLayout()
        l.addWidget(self.labelTempDescription)
        l.addWidget(self.pbHandle)

        self.setLayout(l)

    def initSignals(self) -> None:
        self.pbHandle.clicked.connect(self.onPbHandleClicked)
        self.timer.timeout.connect(lambda: self.labelTempDescription.setText(f"{time.ctime()} >>> Таймер сработал"))

    def onPbHandleClicked(self, status) -> None:

        self.timer.setInterval(5000)
        self.timer.setSingleShot(True)

        if status and not self.timer.isActive():
            self.timer.start()
        else:
            self.timer.stop()

        self.pbHandle.setText("Стоп" if status else "Старт")
        # print(f"{time.ctime()} >>> {status}")


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
