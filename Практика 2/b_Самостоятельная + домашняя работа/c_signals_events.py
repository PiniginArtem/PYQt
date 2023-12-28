"""
Реализация программу проверки состояния окна:
Форма для приложения (ui/c_signals_events.ui)

Программа должна обладать следующим функционалом:

1. Возможность перемещения окна по заданным координатам.
2. Возможность получения параметров экрана (вывод производить в plainTextEdit + добавлять время).
    * Кол-во экранов
    * Текущее основное окно
    * Разрешение экрана
    * На каком экране окно находится
    * Размеры окна
    * Минимальные размеры окна
    * Текущее положение (координаты) окна
    * Координаты центра приложения
    * Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)
3. Возможность отслеживания состояния окна (вывод производить в консоль + добавлять время).
    * При перемещении окна выводить его старую и новую позицию
    * При изменении размера окна выводить его новый размер
"""


from PySide6 import QtWidgets, QtCore, QtGui
from ui.c_signals_events import Ui_Form


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.__initSignals()

    def __initSignals(self) -> None:
        """
        Инициализация сигналов
        """
        self.ui.pushButtonLT.clicked.connect(self.__onPushButtonLTClicked)
        self.ui.pushButtonRT.clicked.connect(self.__onPushButtonRTClicked)
        self.ui.pushButtonLB.clicked.connect(self.__onPushButtonLBClicked)
        self.ui.pushButtonRB.clicked.connect(self.__onPushButtonRBClicked)
        self.ui.pushButtonCenter.clicked.connect(self.__onPushButtonCenterClicked)
        self.ui.pushButtonMoveCoords.clicked.connect(self.__onPushButtonMooveItMooveItClicked)
        self.ui.pushButtonGetData.clicked.connect(self.__onPushButtonGetDataClicked)

    def __onPushButtonLTClicked(self) -> None:
        """
        Перемещение окна в левый верхний угол
        """
        self.move(0, 0)

    def __onPushButtonRTClicked(self) -> None:
        """
        Перемещение окна в правый верхний угол
        """
        screen = self.screen().availableSize().toTuple()
        size = self.rect().size().toTuple()
        x = screen[0] - size[0]
        self.move(x, 0)

    def __onPushButtonLBClicked(self) -> None:
        """
        Перемещение окна в левый нижний угол
        """
        screen = self.screen().availableSize().toTuple()
        size = self.rect().size().toTuple()
        y = screen[1] - size[1]
        self.move(0, y)

    def __onPushButtonRBClicked(self) -> None:
        """
        Перемещение окна в правый нижний угол
        """
        screen = self.screen().availableSize().toTuple()
        size = self.rect().size().toTuple()
        x = screen[0] - size[0]
        y = screen[1] - size[1]
        self.move(x, y)

    def __onPushButtonCenterClicked(self) -> None:
        """
        Перемещение окна в центр
        """
        screen = self.screen().availableSize().toTuple()
        size = self.rect().size().toTuple()
        x = screen[0] // 2 - size[0] // 2
        y = screen[1] // 2 - size[1] // 2
        self.move(x, y)

    def __onPushButtonMooveItMooveItClicked(self) -> None:
        self.move(self.ui.spinBoxX.value(), self.ui.spinBoxY.value())

    def __onPushButtonGetDataClicked(self):
        app = QtCore.QCoreApplication.instance()
        screens = app.screens()
        log_ = f"Лог от {QtCore.QDateTime.currentDateTime().toString('dd.MM.yyyy HH:mm:ss')} \n"
        log_ += "Количество экранов: " + str(len(screens)) + "\n"

        current_win = QtGui.QGuiApplication.focusWindow().objectName()
        log_ += "Текущее основное окно: " + str(current_win) + "\n"

        screen_resolution = QtGui.QGuiApplication.primaryScreen().size().toTuple()
        log_ += "Текущее разрешение экрана: " + str(screen_resolution) + "\n"

        screen = QtGui.QGuiApplication.primaryScreen().name()
        log_ += "Текущий экран: " + str(screen) + "\n"

        current_size = QtGui.QGuiApplication.focusWindow().size().toTuple()
        log_ += "Размеры окна: " + str(current_size) + "\n"

        min_size = QtGui.QGuiApplication.focusWindow().minimumSize().toTuple()
        log_ += "Минимальные размеры окна: " + str(min_size) + "\n"

        coords = QtGui.QGuiApplication.focusWindow().geometry().getCoords()
        log_ += "Текущее положение (координаты) окна: " + str(coords) + "\n"

        position = QtGui.QGuiApplication.focusWindow().position().toTuple()
        size = QtGui.QGuiApplication.focusWindow().size().toTuple()
        x = int(round(size[0] / 2 + position[0], 0))
        y = int(round(size[1] / 2 + position[1], 0))
        log_ += "Координаты центра приложения: (" + str(x) + ", " + str(y) + ")\n"

        status = ""
        if QtGui.QGuiApplication.focusWindow().isActive():
            status += "Окно активно\n"
        if QtGui.QGuiApplication.focusWindow().isVisible():
            status += "Окно отображено\n"
        if QtGui.QGuiApplication.focusWindow().isExposed():
            status += "Окно развёрнуто\n"
        if QtGui.QGuiApplication.focusWindow().isModal():
            status = "Окно свёрнуто\n"
        log_ += "Текущее состояние окна: \n" + str(status) + "\n"

        self.ui.plainTextEdit.setPlainText(log_)

    def moveEvent(self, event: QtGui.QMoveEvent) -> None:
        """
        Событие изменения положения окна

        :param event: QtGui.QMoveEvent
        :return: None
        """
        print(QtCore.QDateTime.currentDateTime().toString("dd.MM.yyyy HH:mm:ss"))
        print("Старая позиция:", event.oldPos().toTuple())
        print("Новая позиция:", event.pos().toTuple())
        print("-------------")

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        """
        Событие изменения размера окна

        :param event: QtGui.QResizeEvent
        :return: None
        """

        print(QtCore.QDateTime.currentDateTime().toString("dd.MM.yyyy HH:mm:ss"))
        print("Новый размер окна:", event.size().toTuple())
        print("-------------")


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()