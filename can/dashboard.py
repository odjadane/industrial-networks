import sys, os, can
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLCDNumber, 
)
OPTIONS = {'update_time': 100}
node1 = can.interface.Bus(bustype='kvaser', channel='1')

class ApplicationWindow(QDialog):
    def __init__(self, ):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.setup_timer()
        
        
    def setupUi(self, Dialog):
        self.verticalLayout = QVBoxLayout(Dialog)

        self.lcd_reading = QLCDNumber(Dialog)
        self.lcd_reading.setMinimumSize(QtCore.QSize(300, 100))
        self.verticalLayout.addWidget(self.lcd_reading)


    def initUI(self):
        self.setFixedSize(330, 180)
        self.setWindowTitle("PyQt CAN bus Dashboard")
        
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width()-size.width())/2, 
            (screen.height()-size.height())/2)


    def setup_timer(self):
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(OPTIONS['update_time'])
        self.timer.timeout.connect(self.update_reading)
        self.timer.start()


    def get_value(self):
        msg = node1.recv(timeout=0.001)
        value = list(msg.data)[0] 
        return value


    def update_reading(self):
        try:
            reading = self.get_value()
            self.lcd_reading.display(str(reading))
        except:
            pass


    def closeEvent(self, event):
        self.timer.stop()
            

if __name__ == '__main__':
    print('Waiting for simulation to start..')
    while True:
        try:
            msg = node1.recv(timeout=0.001)
            arbit = msg.arbitration_id
            value = list(msg.data)[0]
            if arbit == 200 and value == 1:
                break
        except AttributeError:
            pass
    print('Launching dashboard...')
    app = QApplication(sys.argv)
    main = ApplicationWindow()
    main.show()
    sys.exit(app.exec_())