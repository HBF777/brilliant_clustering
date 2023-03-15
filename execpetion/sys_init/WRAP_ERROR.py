#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/16 10:35
# @Author  : 李帅兵
# @Project : Brilliant_Lamp_clustering
# @File    : WRAP_ERROR.py
# @Software: PyCharm
class WrapDataError(Exception):
    def __init__(self):
        super(WrapDataError, self).__init__()