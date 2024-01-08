"""
Реализовать виджет, который будет работать с потоком SystemInfo из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода времени задержки
2. поле для вывода информации о загрузке CPU
3. поле для вывода информации о загрузке RAM
4. поток необходимо запускать сразу при старте приложения
5. установку времени задержки сделать "горячей", т.е. поток должен сразу
реагировать на изменение времени задержки
"""

from PySide6 import QtWidgets
from a_threads import SystemInfo


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.CpuRamInfo = SystemInfo()
        self.CpuRamInfo.start()

        self.initUi()
        self.initSignals()


    def initUi(self):

        labelDelay = QtWidgets.QLabel("Интревал обновления, с")
        self.spinBoxDelay = QtWidgets.QSpinBox()
        self.spinBoxDelay.setMinimum(1)

        l_delay = QtWidgets.QHBoxLayout()
        l_delay.addWidget(labelDelay)
        l_delay.addWidget(self.spinBoxDelay)

        labelCPU = QtWidgets.QLabel("CPU: ")
        labelCPU.setMinimumWidth(50)
        self.lineEditCPU = QtWidgets.QLineEdit()
        self.lineEditCPU.setReadOnly(True)

        l_cpu = QtWidgets.QHBoxLayout()
        l_cpu.addWidget(labelCPU)
        l_cpu.addWidget(self.lineEditCPU)

        labelRAM = QtWidgets.QLabel("RAM: ")
        labelRAM.setMinimumWidth(50)
        self.lineEditRAM = QtWidgets.QLineEdit()
        self.lineEditRAM.setReadOnly(True)

        l_ram = QtWidgets.QHBoxLayout()
        l_ram.addWidget(labelRAM)
        l_ram.addWidget(self.lineEditRAM)

        l_main = QtWidgets.QVBoxLayout()
        l_main.addLayout(l_delay)
        l_main.addLayout(l_cpu)
        l_main.addLayout(l_ram)

        self.setLayout(l_main)

    def initSignals(self):
        self.CpuRamInfo.systemInfoReceived.connect(lambda data: self.lineEditCPU.setText(str(data[0])))
        self.CpuRamInfo.systemInfoReceived.connect(lambda data: self.lineEditRAM.setText(str(data[1])))
        self.spinBoxDelay.valueChanged.connect(self.CpuRamInfo.setDelay)


if __name__ == '__main__':
    app = QtWidgets.QApplication()

    win = Window()
    win.show()

    app.exec()
