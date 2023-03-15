#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/15 1:48
# @Author  : 李帅兵
# @Project : Brilliant_Lamp_clustering
# @File    : test_parse.py
# @Software: PyCharm
# a = .format(humidity=22, temperature=11)
a = "{{\"data\":{{\"humidity\":{humidity},\"temperature\":{temperature},\"time\":{time}}}}}".format(humidity="31",temperature="43",time='22')
print(a)