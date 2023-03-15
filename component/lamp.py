#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/15 19:09
# @Author  : 李帅兵
# @Project : Brilliant_Lamp_clustering
# @File    : lamp.py
# @Software: PyCharm
import time
from .driver import temp


class Lamp(object):
    def __init__(self, conf, serial_send, mqtt_send):
        self.name = conf['name']
        self.serial = conf['serial']
        self.SERIAL_SEND = serial_send
        self.MQTT_SEND = mqtt_send
        if self.name == "lamp3":
            self.temp_main()

    def temp_main(self):
        temp.Init()

    def get_name(self):
        return self.name

    def power_on(self, data):
        if self.name == "lamp3":
            temp.power_on()
            return None
        #print(str(self.name)+","+str(self.serial)+","+str(self.SERIAL_SEND)+","+str(self.MQTT_SEND) )   
        op = self.serial["command"][0]["power_on"]
        target = self.serial["serial_id"]
        if data > self.serial['command'][2][1]:
            data = self.serial['command'][3][0]
        elif data > self.serial['command'][2][2]:
            data = self.serial['command'][3][1]
        elif data > self.serial['command'][2][3]:
            data = self.serial['command'][3][2]
        elif data > self.serial['command'][2][4]:
            data = self.serial['command'][3][3]
        #elif data == 0:
            #self.power_off()
            #return
        else:
            data = self.serial['command'][3][4]
        command = str(op) + str(target) + str(data) + str(self.serial["end"])
        self.SERIAL_SEND.put(command)

    def power_off(self):
        if self.name == "lamp3":
            temp.power_off()
            return None
        op = self.serial["command"][0]["power_off"]
        target = self.serial["serial_id"]
        data = self.serial["command"][2][-1]
        command = str(op) + str(target) + str(data) +str(self.serial['end'])
        self.SERIAL_SEND.put(command)

    def set_Light(self, value):
        if self.name == "lamp3":
            temp.set_light(value)
            return None
        self.power_on(value)

    def heartbeat(self, data):
        self.MQTT_SEND.put()

    def switch(self, data):
        if data == 1:
            self.power_on(50)
        else:
            self.power_off()

    def error(self):
        pass

    def exception(self):
        pass
