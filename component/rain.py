#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/19/15:03
# @Author  : 周伟帆
# @Project : brilliant_clustering - new
# @File    : rain
# @Software: PyCharm
from component.sensor import Sensor
from .driver.rain import driver


class Rain(Sensor):
    def __init__(self, COMPONENT_CONFIG):
        super(Rain, self).__init__(COMPONENT_CONFIG)

    def init_Driver(self):
        self._driver = driver(self._pins)

    def get_data(self):
        return self._driver.get_data()