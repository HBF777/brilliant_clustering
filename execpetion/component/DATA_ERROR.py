#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/16 10:34
# @Author  : 李帅兵
# @Project : Brilliant_Lamp_clustering
# @File    : DATA_ERROR.py
# @Software: PyCharm
class GetDataError(Exception):
    def __init__(self):
        super(GetDataError, self).__init__()