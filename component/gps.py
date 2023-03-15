# -*- codeing = utf-8 -*-
# @Time : 2022/10/14 15:00
# @Autor: 李帅兵 202003024036
# @File : gps.py
# @Software：PyCharm
from component.sensor import Sensor
from .driver.gps import driver


class Gps(Sensor):
    def __init__(self, COMPONENT_CONFIG):
        super(Gps, self).__init__(COMPONENT_CONFIG)

    def init_Driver(self):
        self._driver = driver(self._pins)

    def get_data(self):
        return self._driver.get_data()