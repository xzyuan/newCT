import clr
import time
import sys
import threading

sys.path.append("..\Xray")
clr.AddReference("XrayNsrl")
from XrayNsrl import XrayFunc
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class dllForPython():
    gXrayLogic = XrayFunc()

    def start(self):
        return self.gXrayLogic.start()

    def stop(self):
        return self.gXrayLogic.stop()

    def prepare(self, parameter):
        return self.gXrayLogic.prepare(parameter)

    def expose(self):
        return self.gXrayLogic.expose()

    def test(self):
        return self.gXrayLogic.test()

    def getStatus(self):
        return self.gXrayLogic.getStatus()



class Example(QWidget):

    gXrayLogic = XrayFunc()

    def __init__(self):
        super().__init__()

        self.initUI()

        print(self.gXrayLogic.test())



    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        self.setToolTip('This is a <b>QWidget</b> widget')

        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)
        btn.clicked.connect(self.btnClk)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Tooltips')
        self.show()

    def btnClk(self):
        self.gXrayLogic.start()
        QMessageBox.critical(self, "Critical",
                             self.tr("start"))

        para = "kv=80;ma=50;focal_spot_size=Large;exposure_time=1"
        self.gXrayLogic.prepare(para)
        QMessageBox.critical(self, "Critical",
                             self.tr("prepare"))
        self.gXrayLogic.expose()
        QMessageBox.critical(self, "Critical",
                             self.tr("expose"))
        self.gXrayLogic.stop()
        QMessageBox.critical(self, "Critical",
                             self.tr("stop"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


# gXrayLogic = XrayFunc()
#
# # gXrayLogic.start()
#
# def func():
#     print("timer")
#     gXrayLogic.start()
#
# timer = threading.Timer(10, func)
# timer.start()