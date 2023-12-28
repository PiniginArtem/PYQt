"""
Файл для повторения темы фильтр событий

Напомнить про работу с фильтром событий.

Предлагается создать кликабельный QLabel с текстом "Красивая кнопка",
используя html - теги, покрасить разные части текста на нём в разные цвета
(красивая - красным, кнопка - синим)
"""

from PySide6 import QtWidgets, QtCore


class CutieButton(QtWidgets.QWidget):
    clicked = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        label_main = QtWidgets.QLabel("<span style='color: red'>Красивая</span> <span style='color: blue'>кнопка</span>")
        label_main.setObjectName("layout_main")
        label_main.installEventFilter(self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label_main)

        self.setLayout(layout)

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if watched.objectName() == "layout_main":
            if event.type() == QtCore.QEvent.Type.MouseButtonRelease:
                self.clicked.emit()
        return super(CutieButton, self).eventFilter(watched, event)

    # def handle(self):
    #     print("Делаю что-то")


class MainWindow(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)

        c_b_0 = CutieButton()
        c_b_0.clicked.connect(lambda: print("c_b_0 нажата"))
        c_b_1 = CutieButton()
        c_b_1.clicked.connect(lambda: print("c_b_1 нажата"))

        l = QtWidgets.QVBoxLayout()
        l.addWidget(c_b_0)
        l.addWidget(c_b_1)

        self.setLayout(l)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = MainWindow()
    window.show()

    app.exec()
