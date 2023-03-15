# -*- codeing = utf-8 -*-
# @Time : 2022/10/14 15:15
# @Autor: 李帅兵 202003024036
# @File : OBJECT_ERROR.py
# @Software：PyCharm
class CreateObjectError(BaseException):
    def __init__(self):
        super(CreateObjectError, self).__init__()