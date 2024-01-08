import time
import psutil
from PySide6 import QtCore


class SystemInfo(QtCore.QThread):
    """
    Получение информации о процессоре и оперативной памяти
    """
    systemInfoReceived = QtCore.Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__delay = None
        self.__status = None

    def run(self) -> None:
        if self.__delay is None:
            self.__delay = 1

        self.__status = True

        while self.__status:
            cpu_value = psutil.cpu_percent()
            ram_value = psutil.virtual_memory().percent
            self.systemInfoReceived.emit([cpu_value, ram_value])
            time.sleep(self.__delay)

    def setDelay(self, delay: int) -> None:
        self.__delay = delay

    def setStatus(self, status: bool):
        self.__status = status

    def getStatus(self):
        return self.__status

class SystemServices(QtCore.QThread):
    """
    Получение информации о службах
    """
    systemServicesReceived = QtCore.Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__delay = None

    def setDelay(self, delay: int) -> None:
        self.__delay = delay

    def run(self) -> None:
        if self.__delay is None:
            self.__delay = 10

        while True:
            services = list(psutil.win_service_iter())
            self.systemServicesReceived.emit(services)
            time.sleep(self.__delay)


class SystemProc(QtCore.QThread):
    """
    Получение информации о процессах
    """
    systemProcReceived = QtCore.Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__delay = None

    def setDelay(self, delay: int) -> None:
        self.__delay = delay

    def run(self) -> None:
        if self.__delay is None:
            self.__delay = 10

        while True:
            procs = list(psutil.process_iter())
            self.systemProcReceived.emit(procs)
            time.sleep(self.__delay)