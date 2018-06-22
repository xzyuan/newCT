import sys
import time
import math
import json
import socket
from threading import Thread, Timer
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication

from Src.mainwindow import Ui_MainWindow
from Xray.dll import dllForPython
sys.path.append("..\\Xray\\dll.py")


class GUI(QMainWindow):
    Xray = dllForPython()

    def __init__(self):
        super(GUI, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.GuiInit()

        # log
        self.ui.btn_AddLog.clicked.connect(self.writeManualLog)
        self.ui.textEdit_AutoLog.textChanged.connect(self.writeDailyLog)

        # login
        self.ui.btn_Login.clicked.connect(self.login)

        # scan
        self.ui.btn_WriteParameter.clicked.connect(self.scan)
        self.ui.btn_ScanStart.clicked.connect(self.scanStart)
        self.ui.btn_ScanStop.clicked.connect(self.scanStop)

        # xray
        self.ui.btn_XrayStart.clicked.connect(self.xrayStart)
        self.ui.btn_XrayPrepare.clicked.connect(self.xrayPrepare)
        self.ui.btn_XrayExpose.clicked.connect(self.xrayExpose)
        self.ui.btn_XrayStop.clicked.connect(self.xrayStop)

        #Sample
        self.ui.btn_SampleOff.clicked.connect(self.sendSampleParameters)
        self.ui.btn_SampleOn.clicked.connect(self.setSampleUpdownOn)

        #quit
        self.ui.btn_Quit.clicked.connect(QCoreApplication.instance().quit)

        # palette1 = QtGui.QPalette()
        # palette1.setColor(self.backgroundRole(), QColor(200,200,200))
        # # palette1.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('../../../Document/images/17_big.jpg')))   # 设置背景图片
        # self.setPalette(palette1)
        # p = self.ui.tabWidget.palette()
        # p.setColor(self.backgroundRole(),QColor(200,200,70))
        # self.ui.tabWidget.setPalette(p)

    def GuiInit(self):
        self.tabDisplay(False)
        self.ui.lineEdit_PassWord.setEchoMode(QLineEdit.Password)

        print(self.Xray.test())
        global refresh
        refresh = Timer(1, self.refreshStatus)
        refresh.start()

#quit
    def GuiQuit(self):
        sys.exit(0)

#log
    def writeLog(self, strlog):

        currtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # dailylog = "\n" + currtime + " " + strlog
        dailylog = currtime + " " + strlog
        self.ui.textEdit_AutoLog.append(dailylog)

    def writeManualLog(self):
        manual_log = "[手动添加日志]" + self.ui.textEdit_ManualLog.toPlainText()
        self.writeLog(manual_log)

    def writeDailyLog(self):
        logfilename = time.strftime("%Y-%m-%d", time.localtime()) + ".txt"
        log = self.ui.textEdit_AutoLog.toPlainText()
        with open("../Log/" + logfilename, 'a', encoding='utf-8') as f:
            f.write(log)

    def tabDisplay(self, flag):
        self.ui.tab_2.setEnabled(flag)
        self.ui.tab_3.setEnabled(flag)
        self.ui.tab_4.setEnabled(flag)
        self.ui.tab_5.setEnabled(flag)
        self.ui.tab_6.setEnabled(flag)
        self.ui.tab_7.setEnabled(flag)

    # login
    def login(self):
        user = self.ui.lineEdit_UserName.text()
        passWd = self.ui.lineEdit_PassWord.text()
        if passWd == "nsrl" and user == "CT":
            QMessageBox.information(self, "login", "欢迎使用CT原理样机控制软件！", QMessageBox.Ok)
            self.tabDisplay(True)
            self.ui.lineEdit_PassWord.clear()
            self.ui.lineEdit_UserName.clear()
            log = user + "login\n"


            self.writeLog(log)
        else:
            self.tabDisplay(False)
            QMessageBox.information(self, "login", "用户名密码不匹配，请重试！", QMessageBox.Cancel)

    # scan
    def getScanParameter(self):
        CTscan_parameter = {
            "G1光栅周期P": 0,  # 周期 P
            "G1光栅步进步数N": 0,  # N - 1 次， 每次步进 P / N
            "样品转台采集次数K": 0,  # 一圈要采集 K 次, 每次动 2π / K
            "样品高度H": 0,
            "样品视场Y方向长度L": 0,
            "样品台轴向步进层数M": 0,  # 步数 M = [H / L] 向上取整 ， 每次走L， 样品高度 H
            "扫描模式": 0 # 0:保留字段， 1:传统相位步进， 2：周步进， 3：免步进
        }

        CTscan_parameter["G1光栅步进步数N"] = float(self.ui.lineEdit_ScanN.text())
        CTscan_parameter["G1光栅周期P"] = float(self.ui.lineEdit_ScanP.text())
        CTscan_parameter["样品转台采集次数K"] = float(self.ui.lineEdit_ScanK.text())
        CTscan_parameter["样品视场Y方向长度L"] = float(self.ui.lineEdit_ScanL.text())
        CTscan_parameter["样品高度H"] = float(self.ui.lineEdit_ScanH.text())
        H = float(CTscan_parameter["样品高度H"])
        L = float(CTscan_parameter["样品视场Y方向长度L"])
        CTscan_parameter["样品台轴向步进层数M"] = math.ceil(H / L)
        scanMode2Int = {
            "传统相位步进": 1,
            "周步进": 2,
            "免步进": 3
        }
        scanMode = self.ui.comboBox_ScanMode.currentText()
        CTscan_parameter["扫描模式"] = scanMode2Int[scanMode]
        return CTscan_parameter

    def scan(self):
        CTscan_parameter = self.getScanParameter()
        msg = "确认需要写入如下参数：\n" + ''.join('{} = {}\n'.format(key, val) for key, val in CTscan_parameter.items())
        ret = QMessageBox.information(self, "scan", msg, QMessageBox.Yes | QMessageBox.No)

        if ret == QMessageBox.Yes:
            with open('../Conf/conf.json', 'w') as f:
                json.dump(CTscan_parameter, f)
            # write log
            dailylog = " write parameter !\n" + ''.join('{} = {}\n'.format(key, val) for key, val in CTscan_parameter.items())
            # dailylog += "\n"
            self.writeLog(dailylog)
        else:
            return

    def scanStart(self):
        ret = QMessageBox.information(self, "scan", "开始扫描？", QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.Yes:
            self.timeSequnceController()
            self.writeLog("开始扫描\n")
        else:
            return

    def scanStop(self):
        ret = QMessageBox.information(self, "scan", "停止扫描？", QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.Yes:
            pass #todo
            self.writeLog("开始扫描\n")
        else:
            return

    def getSendPara(self):
        CTscan_parameter = self.getScanParameter()
        para = bytes("{},{},{},{},{},{},{}".format(CTscan_parameter["G1光栅周期P"],
                                                   CTscan_parameter["G1光栅步进步数N"],
                                                   CTscan_parameter["样品转台采集次数K"],
                                                   CTscan_parameter["样品高度H"],
                                                   CTscan_parameter["样品视场Y方向长度L"],
                                                   CTscan_parameter["样品台轴向步进层数M"],
                                                   CTscan_parameter["扫描模式"]), encoding="utf-8")
        paralen = bytes(hex(len(para)), encoding="utf-8")
        return para, paralen

    def timeSequnceController(self):
        CTscan_parameter = self.getScanParameter()
        sendSuccess = False
        def sendParameter():
            address = ('192.168.0.10', 1200)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(address)
            para, paraLength = self.getSendPara()
            s.send(paraLength)  # 待发送的参数的长度
            s.send(para)  # 扫描参数
            ret = s.recv(100)
            if ret is "OK":
                sendSuccess = True # 异步通知
            s.close()
        t = Thread(target=sendParameter, args=())
        t.start()

    # xray
    def xrayStart(self):
        # ret = self.Xray.start()
        ret = 0
        if 1 == ret:
            QMessageBox.warning(self, "警告", "start 失败！请重启软件！")
        else:
            self.writeLog("Xray Start\n")
            self.ui.textEdit_XrayLog.append("Start 成功\n等待参数设置\n")

    def xrayPrepare(self):
        kV = self.ui.lineEdit_XrayKv.text()
        mA = self.ui.lineEdit_XrayMa.text()
        eTime = self.ui.lineEdit_XrayTime.text()
        fSize = self.ui.comboBox_XrayFcoal.currentText()
        para = ("kv={0};ma={1};focal_spot_size={2};exposure_time={3}".format(kV, mA, fSize, eTime))
        print(para) # debug
        ret = self.Xray.prepare(para)
        if 1 == ret:
            QMessageBox.warning(self, "警告", "prepare 失败！请重启软件！")
        else:
            self.writeLog("Xray Prepare\n Prepare 参数：{}\n".format(para))
            self.ui.textEdit_XrayLog.append("prepare 成功\n等待曝光\n")

    def xrayExpose(self):
        ret = self.Xray.expose()
        if 1 == ret:
            QMessageBox.warning(self, "警告", "expose 失败！请重启软件！")
        else:
            self.writeLog("Xray Expose\n")
            self.ui.textEdit_XrayLog.append("Expose 成功\n")

    def xrayStop(self):
        ret = self.Xray.start()
        if 1 == ret:
            QMessageBox.warning(self, "警告", "stop 失败！请重启软件！")
        else:
            self.writeLog("Xray Stop\n")
            self.ui.textEdit_XrayLog.append("Stop 成功\n")

    def xrayGetStatus(self):
        return self.Xray.getStatus()

    # TODO 周期刷新
    def xrayStatus(self):
        # self.ui.textEdit_XrayLog.verticalScrollBar().setValue(0)
        self.ui.label_XrayStatus.setText(self.xrayGetStatus())

    def refreshStatus(self):
        self.xrayStatus()
        self.ui.textEdit_XrayLog.append(self.xrayGetStatus() + "\n")
        global refresh
        refresh = Timer(1, self.refreshStatus)
        refresh.start()

    # 读取升降/旋转电机设定参数
    def getSampleParameters(self):
        Sample_parameters = {
            "命令功能": 0,  #0代表控制指令，1代表请求升降电机状态，2代表请求旋转电机状态
            "选择电机": 0,  #0代表升降电机，1代表旋转电机
            "电机动作": 0,    #0代表停止，1代表启动
            "电机使能": 0,  #0代表使能ON，1代表使能OFF
            "运行模式": 0,  #0代表回原点，1代表点动模式，2代表定位运动
            "运动方向": 0,  #0代表正向，1代表反向
            "目标位置": 0,  #升降电机1代表0.01mm，范围0~20000，旋转电机1代表0.01°，设定范围0~35999
            "目标速度": 0   #升降电机1代表0.01mm/s，范围10~400，旋转电机1代表0.01r/min,范围100~3000
        }
        Sample_parameters["选择电机"] = self.ui.comboBox_SampleSelect.currentIndex()
        Sample_parameters["运动方向"] = self.ui.comboBox_SampleDirection.currentIndex()
        Sample_parameters["运行模式"] = self.ui.comboBox_SampleMode.currentIndex()+1
        Sample_parameters["目标位置"] = self.ui.lineEdit_SampleDestPosition.text()
        Sample_parameters["目标速度"] = self.ui.lineEdit_SampleSpeed.text()
        return Sample_parameters

    def getSampleSendParameter(self):
        Sample_parameter = self.getSampleParameters()
        para = bytes("{},{},{},{},{},{},{},{}".format(Sample_parameter["命令功能"],
                                                   Sample_parameter["选择电机"],
                                                   Sample_parameter["电机动作"],
                                                   Sample_parameter["电机使能"],
                                                   Sample_parameter["运行模式"],
                                                   Sample_parameter["运动方向"],
                                                   Sample_parameter["目标位置"],
                                                   Sample_parameter["目标速度"]), encoding="utf-8")
        return para

    # SampleControl
    def sendSampleParameters(self):
        Sample_parameter = self.getSampleSendParameter()
        address = ('192.168.125.118', 12225)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(address)
            s.send(Sample_parameter)
            data = s.recv(1024)
            print(bytes.decode(data))
            QMessageBox.information(self, "Tips", "关闭成功")
            s.close()
        except Exception:
            s.close()
            QMessageBox.information(self, "Tips", "无法连接到样品台控制器")


    def setSampleUpdownOn(self):
        address = ('192.168.125.118', 12225)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(address)
            s.send(bytes(0x02))
            data = s.recv(1024)
            print(bytes.decode(data))
            QMessageBox.information(self, "Tips", "开启成功")
            s.close()
        except Exception:
            s.close()
            QMessageBox.information(self, "Tips", "无法连接到样品台控制器")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())