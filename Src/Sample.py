import sys
import time
import socket
import struct
from threading import Thread
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication



Sample_Address = ("192.168.0.9",502)
TurnStage_Address = ("192.168.0.10",2000)

def connectToSampleStage():
    global s_sample
    s_sample = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s_sample.connect(Sample_Address)
    except Exception:
        s_sample.close()
        print("无法连接到样品台控制器")

def recognizeSampleError(data)  :
    error_arr = ("无错误",
                 "升降电机使能错误", "升降电机回原点错误", "升降电机JOG错误", "升降电机定位错误", "升降电机到达上极限", "升降电机到达下极限",
                 "旋转电机使能错误", "旋转电机回原点错误", "旋转电机JOG错误", "旋转电机定位错误",
                 "运动模块错误", "CAN模块错误")
    # if(s != 1):
    #     msg = QMessageBox()
    #     msg.setText(error_arr[s])
    #     msg.exec()
    error_code = struct.unpack('8B',data)[1]
    if(error_code != 0):
        print(error_arr[error_code])



def connectToTurnStage():
    global s_turn
    s_turn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s_turn.connect(TurnStage_Address)
    except Exception:
        s_turn.close()
        print("无法连接到转台控制器")



