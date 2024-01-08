"""
Реализовать окно, которое будет объединять в себе сразу два предыдущих виджета
"""
from PySide6 import QtWidgets
from b_systeminfo_widget import Window as SystemInfoWidget
from c_weatherapi_widget import WindowWeather as WeatherWidget


class CombinedWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.system_info_widget = SystemInfoWidget()
        self.weather_widget = WeatherWidget()

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.system_info_widget)
        layout.addWidget(self.weather_widget)

        self.weather_widget.ui.pushButtonGetData.clicked.connect(self.weather_widget.onPushButtonGetDataClicked)
        self.weather_widget.ui.pushButtonStopGetData.clicked.connect(self.weather_widget.onPushButtonStopGetDataClicked())


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = CombinedWindow()
    window.show()

    app.exec()