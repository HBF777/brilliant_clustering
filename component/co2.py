#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/19/11:41
# @Author  : 周伟帆
# @Project : brilliant_clustering - 新灯
# @File    : co2
# @Software: PyCharm
from component.sensor import Sensor
from .driver.co2 import driver


class Co2(Sensor):
    def __init__(self, COMPONENT_CONFIG):
        super(Co2, self).__init__(COMPONENT_CONFIG)

    def init_Driver(self):
        self._driver = driver(self._pins)

    def get_data(self):
        return self._driver.get_data()