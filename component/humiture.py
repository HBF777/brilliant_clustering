#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/13 22:23
# @Author  : 李帅兵
# @Project : Brilliant_Lamp_clustering
# @File    : humiture.py
# @Software: PyCharm
from component.sensor import Sensor
from .driver.humiture import driver


class Humiture(Sensor):
    def __init__(self, COMPONENT_CONFIG):
        super(Humiture, self).__init__(COMPONENT_CONFIG)

    def init_Driver(self):
        self._driver = driver(self._pins)

    def get_data(self):
        return self._driver.get_data()
