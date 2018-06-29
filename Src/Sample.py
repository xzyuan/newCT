import sys
import time
import socket
from threading import Thread
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication


address = ("192.168",12225)

def recognizeSampleError(s)  :
    error_arr = ("无错误",
                 "升降电机使能错误", "升降电机回原点错误", "升降电机JOG错误", "升降电机定位错误", "升降电机到达上极限", "升降电机到达下极限",
                 "旋转电机使能错误", "旋转电机回原点错误", "旋转电机JOG错误", "旋转电机定位错误",
                 "运动模块错误", "CAN模块错误")
    if(s != 1):
        msg = QMessageBox()
        msg.setText(error_arr[s])
        msg.exec()