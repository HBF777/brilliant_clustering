#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/6 12:42
# @Author  : 李帅兵
# @Project : Brilliant_Lamp_clustering
# @File    : serial.py
# @Software: PyCharm
import threading
import time

import serial as Ser


class Serial:
    def __init__(self, conf):
        self.ser = Ser.Serial(conf['port'], conf['baud_rate'])
        self.SERIAL_SEND = conf["SEND_SERIAL"]
        self.SERIAL_RECEIVING = conf["RECEIVING_SERIAL"]
        self.logger = conf['logger']
        self.open_prot()
        threading.Thread(target=self.read_line).start()
        threading.Thread(target=self.write_line).start()

    def open_prot(self):
        if not self.ser.is_open:
            self.ser.open()

    def close_prot(self):
        self.ser.close()

    def write_line(self):
        while True:
            if self.SERIAL_SEND.empty():
                line = self.SERIAL_SEND.get()
                self.ser.write(line.encode("utf-8"))
                self.logger.logger.info("串口写入指令:"+line)

    def write_lines(self, lines):
        pass

    def read_line(self):
        try:
            while True:
                size = self.ser.inWaiting()
                if size != 0:
                    try:
                        response = str(self.ser.read(size),"utf-8")
                        self.SERIAL_RECEIVING.put(response)
                        self.logger.logger.info("串口读出指令："+response)
                    except Exception as e:
                        self.logger.logger.error("串口读出数据非法")

                    self.ser.flushInput()
                    time.sleep(0.001)
        except KeyboardInterrupt:
            self.ser.close()



