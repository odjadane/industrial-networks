import sys, serial
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (
    QApplication, QDialog,
    QHBoxLayout, QGroupBox,
    QRadioButton, QMessageBox
)

SERIAL_PORT = 'COM6'

class ApplicationWindow(QDialog):
    def __init__(self, ):
        super().__init__()
        self.initUI()
        self.setupUi()
        self.setupConnect()
        
        self.arduino_is_connected = True
        try:
            self.arduino = serial.Serial(SERIAL_PORT, 9600, timeout=1)
        except serial.serialutil.SerialException:
            _ = QMessageBox.critical(
                self, 'Error', 'Could not open port {}'.format(SERIAL_PORT))
            self.arduino_is_connected = False
            for group in (self.grp_left, self.grp_right):
                for widget in group.findChildren(QRadioButton):
                    widget.setEnabled(False)
                    

    def initUI(self):
        self.setWindowTitle("PyQt Arduino LED")


    def setupUi(self):
        self.rd_left_on = QRadioButton("ON")
        self.rd_left_off = QRadioButton("OFF")
        self.rd_left_off.setChecked(True)
        self.grp_left_hbox = QHBoxLayout()
        self.grp_left_hbox.addWidget(self.rd_left_on)
        self.grp_left_hbox.addWidget(self.rd_left_off)
        self.grp_left = QGroupBox()
        self.grp_left.setLayout(self.grp_left_hbox)
        self.grp_left.setTitle("Red LED")
        
        self.rd_right_on = QRadioButton("ON")
        self.rd_right_off = QRadioButton("OFF")
        self.rd_right_off.setChecked(True)
        self.grp_right_hbox = QHBoxLayout()
        self.grp_right_hbox.addWidget(self.rd_right_on)
        self.grp_right_hbox.addWidget(self.rd_right_off)
        self.grp_right = QGroupBox()
        self.grp_right.setLayout(self.grp_right_hbox)
        self.grp_right.setTitle("Green LED")

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.addWidget(self.grp_left)
        self.horizontalLayout.addWidget(self.grp_right)
        
        self.setLayout(self.horizontalLayout)


    def setupConnect(self):
        self.rd_left_on.clicked.connect(self.onRdLeftOnClick)
        self.rd_left_off.clicked.connect(self.onRdLeftOffClick)
        self.rd_right_on.clicked.connect(self.onRdRightOnClick)
        self.rd_right_off.clicked.connect(self.onRdRightOffClick)


    def onRdLeftOnClick(self):
        self.arduino.write(b'0')


    def onRdLeftOffClick(self):
        self.arduino.write(b'1')


    def onRdRightOnClick(self):
        self.arduino.write(b'2')


    def onRdRightOffClick(self):
        self.arduino.write(b'3')


    def closeEvent(self, event):
        if self.arduino_is_connected:
            self.arduino.write(b'1')
            self.arduino.write(b'3')
            self.arduino.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = ApplicationWindow()
    main.show()
    sys.exit(app.exec_())