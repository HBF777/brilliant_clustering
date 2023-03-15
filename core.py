#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/6 11:26
# @Author  : 李帅兵
# @Project : Brilliant_Lamp_clustering
# @File    : core.py
# @Software: PyCharm
import json
import re
import time
from queue import Queue

import uuid
from threading import Thread
import importlib
# 初始化日志类
from execpetion.component.DATA_ERROR import GetDataError
from execpetion.sys_init.WRAP_ERROR import WrapDataError
from log import Logger
# 导入错误
from execpetion.sys_init.FILE_ERROR import *
from execpetion.sys_init.OBJECT_ERROR import *
from com.mqtt import Mqtt
from com.serial import Serial
from component.humiture import Humiture
from component.gps import Gps
from component.luminance import Luminance
from component.lamp import Lamp
from component.co2 import Co2
from component.rain import Rain
from component.brightness import Brightness

MAC = str(uuid.uuid1()).split('-')[4]

# mqtt消息队列
RECEIVING_MQTT = Queue()
SEND_MQTT = Queue()
# Serial消息队列
RECEIVING_SERIAL = Queue()
SEND_SERIAL = Queue()
# 异常处理队列
FAULTS = Queue()




error_json = {"Error":
                  [{"error_name": "Net_Error",
                    "test_func": "Net()",
                    }]}

##################################################
# 在这里写错误类
import socket
from time import sleep
import threading

# 断网的检测方法
def Net(testserver=('www.baidu.com', 443)):
    s = socket.socket()

    s.settimeout(3)
    try:
        status = s.connect_ex(testserver)
        if status == 0:
            s.close()
            return True
        else:
            raise No_Internet_connection_Error
    except Exception as e:
        raise No_Internet_connection_Error


# 异常检测器
def checkError(func='Net()'):
    try:
        exec(func)
        return True
    except Exception as e:
        print(e)
        return False


# 网络状态异常
class No_Internet_connection_Error(Exception):
    def __init__(self):
        super().__init__(self)  # 初始化父类
        self.errorinfo = "No Internet connection Error"

    def __str__(self):
        return self.errorinfo

    @staticmethod
    def getMessage(self):
        print(self.errorinfo)

myerrors = json.loads(json.dumps(error_json))

'''
现在目前的流程：
    一个跑线程的方法（模板）
        核心在这个线程方法里：
        1，需要确认是否有该异常名  error_name
        2，进行检查方法判断   test_func
        3,


    func（被装饰的方法）

    启动线程

'''

class Error_decorator1(object):
    def __init__(self, error='INFO'):
        self.error = error

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            def threadfunc():
                firstFlag = True
                # 判断是否有该异常
                for i in myerrors['Error']:
                    if i['error_name'] == self.error:
                        # 如果没有异常会继续执行下去
                        # 有异常会进入这一步，直到异常解决
                        while True:
                            # 检测程序
                            try:
                                if not checkError(i['test_func']):
                                    # 如果有异常
                                    firstFlag = True
                                    # 处理异常
                                    #func(*args, **kwargs)
                                    print("Exception handling")
                                    print("======================================")
                                    sleep(5)
                                    continue
                                else:
                                    # not error
                                    if firstFlag == True:
                                        func(*args, **kwargs)
                                        firstFlag = False
                                    print("No problem!")
                                    sleep(10)
                                    continue
                            except Exception as e:
                                print(e)
                                sleep(5)

            threadA = threading.Thread(target=threadfunc)
            threadA.start()
        return wrapper


class Core:
    """
    配置核心
    """
    STATUS = {
        "offline": None,
        "online": None,
    }
    
    def __init__(self):
        self.logger = logger
        self.config = conf
        self.register = Register()
        self.handler = Handler()
        self.manager = manager
        self.mqtt = None
        self.serial = None
        try:
            self.mqtt = self.register.mqtt(self.config.com_profile['mqtt'])
            self.serial = self.register.serial(self.config.com_profile['serial'])
            self.register.component(self.config.component_profile)
            self.register.lamp(self.config.lamp_profile)
            # Thread(target=self.heartbeat()).start()
        except CreateObjectError:
            self.logger.logger.error("注册路灯或传感器失败")
        except ConnectionError:
            self.logger.logger.error("与服务器连接失败")

    # def heartbeat(self):
    #     while True:
    #         for i in self.config.topics['pub']:
    #             if i['isLamp']:
    #                 topic = i['topic']
    #                 data = self.manager.getLampByName(i['name']).heartbeat()
    #                 msg = i['format'].format(data=data)
    #                 Msg = {
    #                     "topic": topic,
    #                     "data": msg
    #                 }
    #                 self.logger.logger.info("将" + str(Msg) + "加入发送队列")
    #                 SEND_MQTT.put(Msg)
    #         time.sleep(5)


class Config:
    """
    配置类
    """

    def __init__(self):
        self._basic_PATH = "./resources/configuration.json"
        self._topics_PATH = "./resources/topics.json"
        self._lamp_PATH = "./resources/lamp.json"
        self._component_PATH = "./resources/component.json"
        self._com_PATH = "./resources/communication.json"
        try:
            self.lamp_profile = self.load_json(self._lamp_PATH)['lamps']
            self.com_profile = self.load_json(self._com_PATH)
            self.component_profile = self.load_json(self._component_PATH)['components']
            self.basic_profile = self.load_json(self._basic_PATH)
            self.topics = self.load_json(self._topics_PATH)
        except FileLoadError:
            logger.logger.error("加载配置文件失败")

    @staticmethod
    def load_json(path):
        try:
            with open(path) as f:
                data = json.load(f)
            profile = data
            return profile
        except Exception as e:
            logger.logger.error(e)
            raise FileLoadError

    @staticmethod
    def write_json(path):
        pass

    @staticmethod
    def load_ini(self):
        pass


class Handler:
    """
    消息处理器器
    """

    @staticmethod
    def mqtt(topic, msg):
        for i in conf.topics['sub']:
            try:
                if i['topic'] == topic:
                    # 获取目标类
                    if i['isLamp']:
                        target_obj = manager.getLampByName(i['name'])
                        ret = re.match(pattern=i['format'],
                                       string=str(msg['data']).replace(" ", "").replace("\n", "").replace("\'", "\""))
                        exec("target_obj.%s(%s)" % (i['fun'], ret.group(i['value'])))
                    else:
                        target_obj = manager.getComponentByName(i['name'])
                        data = target_obj.get_data()
                        target_topic, wrap_data = Handler.component_wrap(name=i['name'], data=data)
                        Msg = {
                            "topic": target_topic,
                            "data": wrap_data
                        }
                        #core.logger.logger.info("将" + str(Msg) + "加入发送队列")
                        SEND_MQTT.put(Msg)
                        core.logger.logger.info("将" + str(Msg) + "加入发送队列")
            except GetDataError:
                logger.logger.error(i['name'] + "数据获取异常")
            except WrapDataError:
                logger.logger.error(i['name'] + "数据包装异常")

    @staticmethod
    def serial(data):
        try:
            op = dict(conf.com_profile['serial']['command'][0]).get(data[0])
            target = dict(conf.com_profile['serial']['command'][1]).get(data[1])
            data = dict(conf.com_profile['serial']['command'][2]).get(data[2])
            if op == "heartbeat":
                target_topic, wrap_data = Handler.lamp_wrap(name=target, data=data)
                Msg = {
                    "topic": target_topic,
                    "data": wrap_data,
                }
                core.logger.logger.info("将" + str(Msg) + "加入发送队列")
                SEND_MQTT.put(Msg)
        except Exception as e:
            logger.logger.error(e)
            raise ConnectionAbortedError

    @staticmethod
    def component_wrap(name, data):
        try:

            for i in conf.topics['pub']:
                if i['name'] == name:
                    return i['topic'], i['format'].format(data=data)
        except Exception as e:
            logger.logger.error(e)
            raise WrapDataError

    @staticmethod
    def lamp_wrap(name, data):
        try:
            data = {"lightness":data,"time":time.time()}
            for i in conf.topics['pub']:
                if i['name'] == name:
                    return i['topic'], i['format'].format(data=data)
        except Exception as e:
            logger.logger.error(e)
            raise WrapDataError


class Register:
    """
    注册器，负责注册元件及路灯或其他设备
    """

    @staticmethod
    def lamp(profiles):
        for profile in profiles:
            try:
                manager.addLamp(Lamp(conf=profile, serial_send=SEND_SERIAL, mqtt_send=SEND_MQTT))
                logger.logger.info("成功创建" + profile['name'] + "[路灯]")
            except Exception as e:
                logger.logger.error(e)
                raise CreateObjectError

    @staticmethod
    def component(profiles):
        for profile in profiles:
            try:
                exec("manager.addComponent(%s(profile))" % profile['component'])
                logger.logger.info("成功创建" + profile['name'] + "[元件]")
            except Exception as e:
                logger.logger.error(e)
                raise CreateObjectError

    @staticmethod
    @Error_decorator1('Net_Error')
    def mqtt(profile):
        try:
            profile['RECEIVING_MQTT'] = RECEIVING_MQTT
            profile['SEND_MQTT'] = SEND_MQTT
            profile['logger'] = logger
            profile['sub_topics'] = conf.topics['sub']
            return Mqtt(profile)
        except Exception as e:
            logger.logger.error(e)
            raise ConnectionError

    @staticmethod
    def serial(profile):
        try:
            profile['RECEIVING_SERIAL'] = RECEIVING_SERIAL
            profile['SEND_SERIAL'] = SEND_SERIAL
            profile['logger'] = logger
            return Serial(profile)
        except Exception as e:
            logger.logger.error(e)
            raise ConnectionError


class DeviceManager:
    def __init__(self):
        self.components = []
        self.lamps = []

    def addLamp(self, lamp):
        self.lamps.append(lamp)

    def addComponent(self, component):
        self.components.append(component)

    def getLampByName(self, name):
        for i in self.lamps:
            if i.get_name() == name:
                return i

    def getComponentByName(self, name):
        for i in self.components:
            if i.get_name() == name:
                return i


logger = Logger(level="debug")
conf = Config()
manager = DeviceManager()
core = Core()
