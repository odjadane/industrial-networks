import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QPushButton, QLCDNumber
)
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

OPTIONS = {'update_time': 200, 'pb_delay': 200}

class ApplicationWindow(QDialog):
    def __init__(self, ):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.setupSig()
        self.setupTimer()
        self.client = OpenPlcModbus()
        
        
    def setupUi(self, Dialog):
        self.verticalLayout = QVBoxLayout(Dialog)

        self.hbox_btns = QHBoxLayout()
        self.btn_on = QPushButton()
        self.btn_on.setText("Turn On")
        self.btn_off = QPushButton()
        self.btn_off.setText("Turn Off")
        self.hbox_btns.addWidget(self.btn_on)
        self.hbox_btns.addWidget(self.btn_off)
        self.verticalLayout.addLayout(self.hbox_btns)

        self.hbox_motor = QHBoxLayout()
        self.btn_motor = QPushButton()
        self.btn_motor.setText("Motor OFF")
        self.btn_motor.setStyleSheet("background-color : #ff94ab")
        self.hbox_motor.addWidget(self.btn_motor)
        self.verticalLayout.addLayout(self.hbox_motor)

        self.lcd_reading = QLCDNumber(Dialog)
        self.lcd_reading.setMinimumSize(QtCore.QSize(300, 100))
        self.verticalLayout.addWidget(self.lcd_reading)


    def initUI(self):
        self.setFixedSize(330, 220)
        self.setWindowTitle("PyQt pyModbus OpenPLC")
        
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width()-size.width())/2, 
            (screen.height()-size.height())/2)

    
    def setupSig(self):
        self.btn_on.clicked.connect(self.turn_on)
        self.btn_off.clicked.connect(self.turn_off)


    def setupTimer(self):
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(OPTIONS['update_time'])
        self.timer.timeout.connect(self.update_reading)
        self.timer.start()


    def turn_on(self):
        self.client.turn_on(1)
        # let enough time for modbus signal to be processed by the plc
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(OPTIONS['pb_delay'], loop.quit)
        loop.exec_()
        self.client.turn_on(0)


    def turn_off(self):
        self.client.turn_off(1)
        # let enought time for modbus signal to be processed by the plc
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(OPTIONS['pb_delay'], loop.quit)
        loop.exec_()
        self.client.turn_off(0)


    def update_reading(self):
        try:
            counter = self.client.get_counter_value()
            status = self.client.get_motor_status()

            self.lcd_reading.display(str(counter))

            if status:
                self.btn_motor.setStyleSheet("background-color : #ccff90")
                self.btn_motor.setText("Motor ON")
            else:
                self.btn_motor.setStyleSheet("background-color : #ff94ab")
                self.btn_motor.setText("Motor OFF")
        except:
            pass


    def closeEvent(self, event):
        self.client.close()
        self.timer.stop()


class OpenPlcModbus:    
    def __init__(self):
        self.plc = ModbusClient('localhost', port=502)


    def get_counter_value(self):
        request = self.plc.read_holding_registers(1024, 1)
        value = request.registers[0]
        return value


    def get_motor_status(self):
        request = self.plc.read_coils(0, 1)
        status = request.bits[0]
        return status


    def turn_on(self, action):
        if action:
            self.plc.write_coil(1, True)
        else:
            self.plc.write_coil(1, False)


    def turn_off(self, action):
        if action:
            self.plc.write_coil(2, True)
        else:
            self.plc.write_coil(2, False)


    def close(self):
        self.plc.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = ApplicationWindow()
    main.show()
    sys.exit(app.exec_())