#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/20 21:39
# @Author  : 李帅兵
# @Project : brilliant_clustering
# @File    : luminance.py
# @Software: PyCharm
from .sensor import Sensor
from .driver.luminance import driver


class Luminance(Sensor):
    def get_data(self):
        return self.driver.get_data()

    def __init__(self,COMPONENT_CONFIG):
        self.driver = None
        super(Luminance, self).__init__(COMPONENT_CONFIG)

    def init_Driver(self):
        self.driver = driver
