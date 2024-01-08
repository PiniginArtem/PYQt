"""
Реализовать виджет, который будет работать с потоком WeatherHandler из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода широты и долготы (после запуска потока они должны блокироваться)
2. поле для ввода времени задержки (после запуска потока оно должно блокироваться)
3. поле для вывода информации о погоде в указанных координатах
4. поток необходимо запускать и останавливать при нажатии на кнопку
"""
import time
from PySide6 import QtWidgets
from form_weather import Ui_FormWeather
from a_threads import WeatherHandler


class WindowWeather(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_FormWeather()
        self.ui.setupUi(self)

        self.ui.lineEditLatitude.setText(str(59.938778))
        self.ui.lineEditLongitude.setText(str(30.314629))

        self.weatherTread = WeatherHandler(float(self.ui.lineEditLatitude.text()),
                                           float(self.ui.lineEditLongitude.text()))

        self.initSignals()

    def initSignals(self):
        self.ui.pushButtonGetData.clicked.connect(self.onPushButtonGetDataClicked)
        self.ui.pushButtonStopGetData.clicked.connect(self.onPushButtonStopGetDataClicked)
        self.weatherTread.weatherInfoReceived.connect(lambda data:
            self.ui.textEditData.setText(f'--- {time.ctime()} | '
                                                          f'{data["latitude"]}°, {data["longitude"]}° ---'
                  f'\n-Температура: {data["current_weather"]["temperature"]}'
                  f'\n-Скорость ветра: {data["current_weather"]["windspeed"]}'
                  f'\n-Направление ветра: {data["current_weather"]["winddirection"]}\n')
        )
        self.ui.radioButton3.toggled.connect(self.updateDelay)
        self.ui.radioButton5.toggled.connect(self.updateDelay)
        self.ui.radioButton10.toggled.connect(self.updateDelay)

    def updateDelay(self, _):

        rbtn = self.sender()

        if rbtn.isChecked() == True:
            self.weatherTread.setDelay(int(rbtn.text()))

    def onPushButtonGetDataClicked(self):

        if self.weatherTread.getStatus():
            return

        self.weatherTread.setСoordinates(float(self.ui.lineEditLatitude.text()), float(self.ui.lineEditLongitude.text()))

        self.ui.lineEditLatitude.setEnabled(False)
        self.ui.lineEditLongitude.setEnabled(False)

        self.weatherTread.setStatus(True)
        self.weatherTread.start()

    def onPushButtonStopGetDataClicked(self):
        if not self.weatherTread.getStatus():
            return

        self.ui.lineEditLatitude.setEnabled(True)
        self.ui.lineEditLongitude.setEnabled(True)

        self.weatherTread.setStatus(False)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = WindowWeather()
    window.show()

    app.exec()