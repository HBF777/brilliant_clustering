#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/12 9:21
# @Author  : 李帅兵
# @Project : Brilliant_Lamp_clustering
# @File    : component.py
# @Software: PyCharm
import abc


class Component(object):
    """
        元件类：
            属性：name        元件的名称应与配置文件中name一致
                 status      元件状态是否可用 布尔类型
                 pub_topic   元件发布主题
                 sub_topic   元件订阅主题
                 device_code 元件码
                 pins        元件所用管脚字典

    """

    def __init__(self, COMPONENT_CONFIG):
        """
        元件属性的初始化
        :param COMPONENT_CONFIG:
        """
        self._name = COMPONENT_CONFIG['name']
        self._status = COMPONENT_CONFIG['status']
        self._device_code = COMPONENT_CONFIG['device_code']
        self._pins = COMPONENT_CONFIG['pins']
        self._driver = None
        self.init_Driver()

    @abc.abstractmethod
    def init_Driver(self):
        pass

    def get_name(self):
        return self._name

