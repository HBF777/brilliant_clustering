#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/6 11:30
# @Author  : 李帅兵
# @Project : Brilliant_Lamp_clustering
# @File    : run.py.py
# @Software: PyCharm
import sys
import threading
from utils.monitor import monitor_mqtt, monitor_serial

from core import Core


"""
    本文件为系统的启动脚本，
    ASSIGNMENT 为功能的列表，如果后期增加新功能，只须向导入本文件，将其加入ASSIGNMENT中即可
"""
ASSIGNMENT = [monitor_mqtt, monitor_serial]


def init():
    run()


def run():
    # 为所有子任务开启单独线程
    for task in ASSIGNMENT:
        threading.Thread(target=task, ).start()


if __name__ == "__main__":
    init()
