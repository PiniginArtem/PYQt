"""
Файл для повторения темы сигналов

Напомнить про работу с сигналами и изменением Ui.

Предлагается создать приложение, которое принимает в lineEditInput строку от пользователя,
и при нажатии на pushButtonMirror отображает в lineEditMirror введённую строку в обратном
порядке (задом наперед).
"""

from PySide6 import QtWidgets


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__initUi()
        self.__initSignals()

    def __initUi(self) -> None:
        """
        Дополнительная инициализация графического интерфейса
        :return:
        """

        # direct
        labelDirect = QtWidgets.QLabel("Исходный текст")
        labelDirect.setMinimumWidth(100)

        self.__lineEditDirect = QtWidgets.QLineEdit()
        self.__lineEditDirect.setPlaceholderText("Введите текст")

        l_direct = QtWidgets.QHBoxLayout()
        l_direct.addWidget(labelDirect)
        l_direct.addWidget(self.__lineEditDirect)

        # reverse
        labelRevers = QtWidgets.QLabel("Текст наоборот")
        labelRevers.setMinimumWidth(100)

        self.__lineEditReverse = QtWidgets.QLineEdit()
        self.__lineEditReverse.setPlaceholderText("Результат")

        l_reverse = QtWidgets.QHBoxLayout()
        l_reverse.addWidget(labelRevers)
        l_reverse.addWidget(self.__lineEditReverse)

        self.__pbHandle = QtWidgets.QPushButton("Очистить")

        l_main = QtWidgets.QVBoxLayout()
        l_main.addLayout(l_direct)
        l_main.addLayout(l_reverse)
        l_main.addWidget(self.__pbHandle)

        self.setLayout(l_main)

    def __initSignals(self) -> None:
        """

        """

        self.__pbHandle.clicked.connect(self.clear)
        # self.__pbHandle.clicked.connect(lambda: self.__lineEditReverse.setText(self.__lineEditDirect.text()[::-1]))

        self.__lineEditDirect.textChanged.connect(self.__reverseText)

    def __reverseText(self):
        direct = self.__lineEditDirect.text()
        reverse = direct[::-1]
        self.__lineEditReverse.setText(reverse)

    def clear(self):
        self.__lineEditDirect.clear()
        self.__lineEditReverse.clear()


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
