import win32com.client
import cpuinfo
import psutil
from PySide6 import QtWidgets

from TaskManagerThreads import SystemInfo, SystemProc, SystemServices

class TaskManagerApp(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.sysinfo = SystemInfo()
        self.sysservices = SystemServices()
        self.sysprocs = SystemProc()

        self.initUi()

        self.presets()

        self.startTreads()

        self.initSignals()

    def initUi(self) -> None:
        """
        Инициализация интерфейса
        :return: None
        """

        self.setWindowTitle('Мониторинг системы')
        self.setMinimumSize(580, 650)

        # ГрупБокс Система
        lableProcessorName = QtWidgets.QLabel("Процессор")
        lableProcessorName.setMinimumWidth(120)
        self.ProcNameLineEdit = QtWidgets.QLineEdit()
        self.ProcNameLineEdit.setReadOnly(True)
        layoutProcessor = QtWidgets.QHBoxLayout()
        layoutProcessor.addWidget(lableProcessorName)
        layoutProcessor.addWidget(self.ProcNameLineEdit)

        lableCores = QtWidgets.QLabel("Количество ядер")
        lableCores.setMinimumWidth(120)
        self.CoresLineEdit = QtWidgets.QLineEdit()
        self.CoresLineEdit.setReadOnly(True)
        layoutCores = QtWidgets.QHBoxLayout()
        layoutCores.addWidget(lableCores)
        layoutCores.addWidget(self.CoresLineEdit)

        lableProcessorLoad = QtWidgets.QLabel("Текущая загрузка")
        lableProcessorLoad.setMinimumWidth(120)
        self.ProcessorLoadLineEdit = QtWidgets.QLineEdit()
        self.ProcessorLoadLineEdit.setReadOnly(True)
        layoutProcessorLoad = QtWidgets.QHBoxLayout()
        layoutProcessorLoad.addWidget(lableProcessorLoad)
        layoutProcessorLoad.addWidget(self.ProcessorLoadLineEdit)

        self.ProcessorLoadPB = QtWidgets.QProgressBar()

        layoutProc = QtWidgets.QVBoxLayout()
        layoutProc.addLayout(layoutProcessor)
        layoutProc.addLayout(layoutCores)
        layoutProc.addLayout(layoutProcessorLoad)
        layoutProc.addWidget(self.ProcessorLoadPB)

        GBprocessor = QtWidgets.QGroupBox("Процессор")
        GBprocessor.setLayout(layoutProc)

        # ГрупБокс Оперативная память
        lableRAMtotal = QtWidgets.QLabel('Объём памяти')
        lableRAMtotal.setMinimumWidth(120)
        self.RAMtotalLineEdit = QtWidgets.QLineEdit()
        self.RAMtotalLineEdit.setReadOnly(True)
        layoutRAMtotal = QtWidgets.QHBoxLayout()
        layoutRAMtotal.addWidget(lableRAMtotal)
        layoutRAMtotal.addWidget(self.RAMtotalLineEdit)

        lableRAMcurrent = QtWidgets.QLabel('Текущая загрузка ОП')
        lableRAMcurrent.setMinimumWidth(120)
        self.RAMcurrentLineEdit = QtWidgets.QLineEdit()
        self.RAMcurrentLineEdit.setReadOnly(True)
        layoutRAMcurret = QtWidgets.QHBoxLayout()
        layoutRAMcurret.addWidget(lableRAMcurrent)
        layoutRAMcurret.addWidget(self.RAMcurrentLineEdit)

        self.RAMload = QtWidgets.QProgressBar()

        layoutRAM = QtWidgets.QVBoxLayout()
        layoutRAM.addLayout(layoutRAMtotal)
        layoutRAM.addLayout(layoutRAMcurret)
        layoutRAM.addWidget(self.RAMload)

        GBram = QtWidgets.QGroupBox("Оперативная память")
        GBram.setLayout(layoutRAM)

        # ГрупБокс Жесткий диск
        lableDisk = QtWidgets.QLabel("Количество жестких дисков")
        lableDisk.setMinimumWidth(160)
        self.DiskLineEdit = QtWidgets.QLineEdit()
        self.DiskLineEdit.setReadOnly(True)
        layoutD = QtWidgets.QHBoxLayout()
        layoutD.addWidget(lableDisk)
        layoutD.addWidget(self.DiskLineEdit)
        self.DiskInfoPlaintext = QtWidgets.QPlainTextEdit()
        layoutDisk = QtWidgets.QVBoxLayout()
        layoutDisk.addLayout(layoutD)
        layoutDisk.addWidget(self.DiskInfoPlaintext)

        GBdisk = QtWidgets.QGroupBox("Жесткий диск")
        GBdisk.setLayout(layoutDisk)

        FirstTabLayout = QtWidgets.QVBoxLayout()
        FirstTabLayout.addWidget(GBprocessor)
        FirstTabLayout.addWidget(GBram)
        FirstTabLayout.addWidget(GBdisk)

        frame = QtWidgets.QFrame()
        frame.setLayout(FirstTabLayout)

        # Вкладки на Виджете

        self.proccesTableWidget = QtWidgets.QTableWidget()
        self.servisePlaintextedit = QtWidgets.QTableWidget()
        self.tasksPlaintextEdit = QtWidgets.QTableWidget()

        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.addTab(frame, 'Система')
        self.tabWidget.addTab(self.proccesTableWidget, 'Процессы')
        self.tabWidget.addTab(self.servisePlaintextedit, 'Службы')
        self.tabWidget.addTab(self.tasksPlaintextEdit, 'Задачи')

        ComboBoxLabel = QtWidgets.QLabel("Чатсота обновления, сек.")
        self.ComboBox = QtWidgets.QComboBox()

        comboboxLayout = QtWidgets.QHBoxLayout()
        comboboxLayout.addWidget(ComboBoxLabel)
        comboboxLayout.addWidget(self.ComboBox)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.tabWidget)
        mainLayout.addLayout(comboboxLayout)

        self.setLayout(mainLayout)


    def presets(self) -> None:
        self.ProcNameLineEdit.setText(str(cpuinfo.get_cpu_info()['brand_raw']))
        self.CoresLineEdit.setText(str(psutil.cpu_count(logical=True)))
        self.RAMtotalLineEdit.setText(f'{round(psutil.virtual_memory().total / (2**30), 2)} GiB')
        self.DiskLineEdit.setText(str(len(psutil.disk_partitions())))
        self.DiskInfoPlaintext.setPlainText(self.setDiskInfo())
        self.ComboBox.addItems(['1', '2', '5', '10'])

    def setDiskInfo(self) -> str:
        """
        Вывод информации о дисках
        """

        info = ''
        for disc in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(disc.mountpoint)
                info += f'{disc.device}, {disc.fstype}\n' \
                        f'Общий объём памяти: {round(usage.total / (2**30), 2)} GiB\n' \
                        f'Используется: {round(usage.used / (2**30), 2)} GiB\n' \
                        f'Свободно: {round(usage.free / (2**30), 2)} GiB\n' \
                        f'Загружен на {usage.percent} %\n'
            except PermissionError:
                print(f"Нет доступа к диску {disc.mountpoint}")
        return info

    def startTreads(self) -> None:
        """
        Старт потоков
        :return: None
        """
        self.sysinfo.start()
        self.sysprocs.start()
        self.sysservices.start()

    def initSignals(self) -> None:
        """
        Инициализация сигналов
        :return: None
        """

        self.ComboBox.currentTextChanged.connect(self.setDelayAll)
        self.sysinfo.systemInfoReceived.connect(self.setProcInfo)
        self.sysprocs.systemProcReceived.connect(self.updateProcessInfo)
        self.sysservices.systemServicesReceived.connect(self.updateServiseInfo)

        self.updateTaskInfo()

    def setDelayAll(self, text) -> None:
        """
        Установка задержки обновления для всех потоков
        :return: None
        """
        time_ = int(text)
        self.sysinfo.setDelay(time_)
        self.sysprocs.setDelay(time_)
        self.sysservices.setDelay(time_)


    def setProcInfo(self, data):
        """
        Получение информации о текущей загруженности процессора и оперативной памяти
        """

        self.ProcessorLoadLineEdit.setText(str(data[0])+" %")
        self.ProcessorLoadPB.setValue(data[0])
        self.RAMcurrentLineEdit.setText(str(data[1])+" %")
        self.RAMload.setValue(data[1])

    def updateProcessInfo(self, data):
        """
        Вывод информации о процессах
        :param data:
        :return:
        """
        row_count = len(data)
        column_count = 3
        self.proccesTableWidget.setColumnCount(column_count)
        self.proccesTableWidget.setColumnWidth(0, 300)
        self.proccesTableWidget.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("proc_name"))
        self.proccesTableWidget.setColumnWidth(1, 100)
        self.proccesTableWidget.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("cpu_%"))
        self.proccesTableWidget.setColumnWidth(2, 100)
        self.proccesTableWidget.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("mem_%"))
        self.proccesTableWidget.setRowCount(row_count)
        self.proccesTableWidget.setSortingEnabled(True)
        for num, proc in enumerate(data):
            self.proccesTableWidget.setItem(num, 0, QtWidgets.QTableWidgetItem(proc.name()))
            self.proccesTableWidget.setItem(num, 1, QtWidgets.QTableWidgetItem(str(proc.cpu_percent())))
            self.proccesTableWidget.setItem(num, 2, QtWidgets.QTableWidgetItem(str(round(proc.memory_percent(), 2))))

    def updateServiseInfo(self, data):
        """
        Вывод информации о службах
        :param data:
        :return:
        """

        row_count = (len(data))
        column_count = 2
        self.servisePlaintextedit.setColumnCount(column_count)
        self.servisePlaintextedit.setColumnWidth(0, 150)
        self.servisePlaintextedit.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("serv_name"))
        self.servisePlaintextedit.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("Описание"))
        self.servisePlaintextedit.setColumnWidth(1, 350)
        self.servisePlaintextedit.setRowCount(row_count)
        for num, elem in enumerate(data):
            self.servisePlaintextedit.setItem(num, 1, QtWidgets.QTableWidgetItem(elem.display_name()))
            self.servisePlaintextedit.setItem(num, 2, QtWidgets.QTableWidgetItem(elem.name()))

    def updateTaskInfo(self):
        """
        Вывод информации о задачах
        :return:
        """
        service = self.scheduler()
        row_count = len(service)
        column_count = 3
        self.tasksPlaintextEdit.setColumnCount(column_count)
        self.tasksPlaintextEdit.setRowCount(row_count)
        self.tasksPlaintextEdit.setColumnWidth(0, 300)
        self.tasksPlaintextEdit.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("task_path"))
        self.tasksPlaintextEdit.setColumnWidth(1, 100)
        self.tasksPlaintextEdit.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("task_state"))
        self.tasksPlaintextEdit.setColumnWidth(2, 100)
        self.tasksPlaintextEdit.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("task_lust_runtime"))
        for num, work in enumerate(service):
            self.tasksPlaintextEdit.setItem(num, 0, QtWidgets.QTableWidgetItem(work[0]))
            self.tasksPlaintextEdit.setItem(num, 1, QtWidgets.QTableWidgetItem(str(work[1])))
            self.tasksPlaintextEdit.setItem(num, 2, QtWidgets.QTableWidgetItem(str(work[2])))

    def scheduler(self):
        """
        Получение информации о задачах
        :return:
        """
        TASK_STATE = {0: 'Unknown',
                      1: 'Disabled',
                      2: 'Queued',
                      3: 'Ready',
                      4: 'Running'}
        scheduler = win32com.client.Dispatch('Schedule.Service')
        scheduler.Connect()
        folders = [scheduler.GetFolder('\\')]
        schedulertasks = []
        while folders:
            folder = folders.pop(0)
            folders += list(folder.GetFolders(0))
            for task in folder.GetTasks(0):
                task_path = task.Path
                task_state = TASK_STATE[task.State]
                task_lust_runtime = task.LastRunTime
                schedulertasks.append([task_path, task_state, task_lust_runtime])
        return schedulertasks


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    window = TaskManagerApp()
    window.show()
    app.exec()