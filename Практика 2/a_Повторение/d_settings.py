"""
Файл для повторения темы QSettings

Напомнить про работу с QSettings.

Предлагается создать виджет с plainTextEdit на нём, при закрытии приложения,
сохранять введённый в нём текст с помощью QSettings, а при открытии устанавливать
в него сохранённый текст
"""

from PySide6 import QtWidgets, QtCore, QtGui


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__plainTextEdit = QtWidgets.QPlainTextEdit()
        l = QtWidgets.QVBoxLayout()
        l.addWidget(self.__plainTextEdit)

        self.setLayout(l)

        self.__load()

    def __load(self):
        settings = QtCore.QSettings("MySettingsApp")

        text = settings.value("text", "")
        self.__plainTextEdit.setPlainText(text)

        pos = settings.value("pos", QtCore.QPoint(10, 10))

        # app = QtCore.QCoreApplication.instance()
        # screens = app.screens()
        # print(screens)
        #
        # if len(screens) == 1:
        #     pos = QtCore.QPoint(30, 30)

        self.move(pos)
        self.resize(settings.value("size", QtCore.QSize(640, 480)))

    def __save(self):
        settings = QtCore.QSettings("MySettingsApp")
        settings.setValue("text", self.__plainTextEdit.toPlainText())
        settings.setValue("pos", self.pos())
        settings.setValue("size", self.size())

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.__save()


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()

