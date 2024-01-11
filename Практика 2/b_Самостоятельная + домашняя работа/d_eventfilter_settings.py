"""
Реализация программу взаимодействия виджетов друг с другом:
Форма для приложения (ui/d_eventfilter_settings.ui)

Программа должна обладать следующим функционалом:

1. Добавить для dial возможность установки значений кнопками клавиатуры(+ и -),
   выводить новые значения в консоль

2. Соединить между собой QDial, QSlider, QLCDNumber
   (изменение значения в одном, изменяет значения в других)

3. Для QLCDNumber сделать отображение в различных системах счисления (oct, hex, bin, dec),
   изменять формат отображаемого значения в зависимости от выбранного в comboBox параметра.

4. Сохранять значение выбранного в comboBox режима отображения
   и значение LCDNumber в QSettings, при перезапуске программы выводить
   в него соответствующие значения
"""

from PySide6 import QtWidgets, QtCore, QtGui
from ui.d_eventfilter_settings import Ui_Form


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = QtCore.QSettings("EventFilter")

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.comboBox.addItems(['bin', 'oct', 'dec', 'hex'])

        self.loadData()

        self.__initSignals()

    def __initSignals(self) -> None:
        """
        Инициализация сигналов

        :return: None
        """
        self.ui.dial.valueChanged.connect(self.__doValueChangedDial)
        self.ui.horizontalSlider.valueChanged.connect(self.__doValueChangedSlider)
        self.ui.comboBox.currentTextChanged.connect(self.__setLcdMode)


    def __doValueChangedDial(self) -> None:
        """
        Действия при изменении Dial

        :return: None
        """
        self.ui.lcdNumber.display(self.ui.dial.value())
        self.ui.horizontalSlider.setValue(self.ui.dial.value())
        print("Новое значение =", self.ui.dial.value())

    def __doValueChangedSlider(self) -> None:
        """
        Действия при изменении Slider

        :return: None
        """
        self.ui.lcdNumber.display(self.ui.horizontalSlider.value())
        self.ui.dial.setValue(self.ui.horizontalSlider.value())

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        """
        Вращение Dial клавишами "+" и "-"
        """
        if event.key() == 43:
            self.ui.dial.setValue(self.ui.dial.value() + 1)
        if event.key() == 45:
            self.ui.dial.setValue(self.ui.dial.value() - 1)

    def __setLcdMode(self) -> None:
        """
        Изменение системы счисления для QLCDNumber
        """
        text = self.ui.comboBox.currentText()
        if text == 'dec':
            self.ui.lcdNumber.setDecMode()
        elif text == 'bin':
            self.ui.lcdNumber.setBinMode()
        elif text == 'hex':
            self.ui.lcdNumber.setHexMode()
        elif text == 'oct':
            self.ui.lcdNumber.setOctMode()

    def loadData(self) -> None:
        """
        Загрузка данных в Ui

        :return: None
        """

        self.ui.comboBox.setCurrentText(self.settings.value("ComboBox", "dec"))
        self.__setLcdMode()
        self.ui.dial.setValue(self.settings.value("Dial", 0))
        self.ui.horizontalSlider.setValue(self.settings.value("Dial", 0))
        self.ui.lcdNumber.display(self.ui.horizontalSlider.value())

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        Событие закрытия окна

        :param event: QtGui.QCloseEvent
        :return: None
        """

        self.settings.setValue("Dial", self.ui.dial.value())
        self.settings.setValue("ComboBox", self.ui.comboBox.currentText())


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
