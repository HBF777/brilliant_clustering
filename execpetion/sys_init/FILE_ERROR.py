#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/13 17:32
# @Author  : 李帅兵
# @Project : Brilliant_Lamp_clustering
# @File    : FILE_ERROR.py
# @Software: PyCharm
class FileLoadError(Exception):
    def __init__(self):
        super(FileLoadError, self).__init__()
    
    
class CheckFileError(Exception):
    def __init__(self):
        super(CheckFileError, self).__init__()