#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/14 7:34
# @Author  : 李帅兵
# @Project : Brilliant_Lamp_clustering
# @File    : test_driver.py
# @Software: PyCharm
import time

from component.humiture import Humiture
import RPi.GPIO as GPIO
obj1_conf = {
    "name": "ext_Humiture",
    "component": "Humiture",
    "device_code": "03",
    "pins": {
        'a': 16
    },
    "status": True,
    "pub_topic": "server/monitor/{}",
    "sub_topic": "monitor/{}"
}
obj2_conf = {
    "name": "ext_Humiture",
    "component": "Humiture",
    "device_code": "03",
    "pins": {
        'a': 20
    },
    "status": True,
    "pub_topic": "server/monitor/{}",
    "sub_topic": "monitor/{}"
}
GPIO.cleanup()
time.sleep(2)
obj1 = Humiture(obj1_conf)
obj2 = Humiture(obj2_conf)
print(obj1.get_data())
print(obj2.get_data())
