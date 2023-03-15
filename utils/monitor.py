#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/15 11:01
# @Author  : 李帅兵
# @Project : Brilliant_Lamp_clustering
# @File    : monitor.py
# @Software: PyCharm
from core import core
from core import RECEIVING_MQTT, RECEIVING_SERIAL


def monitor_mqtt():
    while True:
        # 检查消息队列
        if not RECEIVING_MQTT.empty():
            msg = RECEIVING_MQTT.get()
            # 解析msg信息
            try:
                topic = msg['topic']
                core.handler.mqtt(topic=topic, msg=msg['data'])
            except Exception as e:
                core.logger.logger.error("未查到对应类", msg['topic'], "消息处理失败" + str(e))


def monitor_serial():
    while True:
        # 检查消息队列
        if not RECEIVING_SERIAL.empty():
            msg = RECEIVING_SERIAL.get()
            # 解析msg信息
            try:

                core.handler.serial(data=msg)
            except Exception as e:
                core.logger.logger.error("未查到对应类", msg['topic'], "消息处理失败" + str(e))

