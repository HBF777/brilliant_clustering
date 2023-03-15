#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/13 18:36
# @Author  : 李帅兵
# @Project : Brilliant_Lamp_clustering
# @File    : sensor.py
# @Software: PyCharm
import abc

from component.component import Component


class Sensor(Component):
    def __init__(self, COMPONENT_CONFIG):
        super().__init__(COMPONENT_CONFIG)

    @abc.abstractmethod
    def get_data(self):
        pass
