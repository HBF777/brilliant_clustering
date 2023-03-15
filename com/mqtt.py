#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/6 12:42
# @Author  : 李帅兵
# @Project : Brilliant_Lamp_clustering
# @File    : mqtt.py
# @Software: PyCharm
import json
import sys
import ast
import time
from threading import Thread
import threading
import paho.mqtt.client as mqtt

from execpetion.com.mqtt import *
import inspect
import ctypes

##################################################
# 在这里写错误类
import socket
from time import sleep
import threading

# 错误的检测方法
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


error_json = {"Error":
                  [{"error_name": "Net_Error",
                    "test_func": "Net()",
                    }]}

myerrors = json.loads(json.dumps(error_json))

class Error_decorator2(object):
    def __init__(self, error='INFO'):
        self.error = error

    def __call__(self, func):
        def wrapper(*args, **kwargs):

            #####################################################
            def threadfunc():
                # 判断是否有该异常
                for i in myerrors['Error']:
                    if i['error_name'] == self.error:
                        # 如果没有异常会继续执行下去
                        # 有异常会进入这一步，直到异常解决
                        # 判断是否有该异常
                        while True:
                            if not checkError(i['test_func']):
                                # 如果有异常
                                print('有异常，正在处理')
                                func(*args, **kwargs) #执行杀死方法
                                print('已杀死')
                                return
                            else:
                                print('无异常')
                                sleep(5)

            #########################################################
            threadA = threading.Thread(target=threadfunc)
            threadA.start()

        return wrapper



class Mqtt(object):
    def __init__(self, conf):
        """
              profile: {
                  "host_ip": "",
                  "host_port": "",
                  "account": "",
                  "passwd": "",
                  "keepalive": "",
                  ""
              }
              :param profile:
              """

        self.target_host = conf['host_ip']
        self.target_port = conf['host_port']
        self.account = conf['account']
        self.password = conf['passwd']
        self.RECEIVING_MQTT = conf['RECEIVING_MQTT']
        self.SEND_MQTT = conf['SEND_MQTT']
        self.logger = conf['logger']
        self.client = mqtt.Client()
        self.client.username_pw_set(self.account, self.password)
        self.client.on_message = self.__on_message
        self.client.reconnect_delay_set(min_delay=1, max_delay=2000)
        self.sub_topics = conf['sub_topics']
        self.Connect()
        
    def _async_raise(self,tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,  
            # and you should call it again with exc=NULL to revert the effect"""  
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
          
        
    @Error_decorator2('Net_Error')
    def care(self,a,b):
        self._async_raise(a.ident,SystemExit)
        self._async_raise(b.ident,SystemExit)
        #threading.Thread._Thread__stop(a)
        #threading.Thread._Thread__stop(b)
  
    def Connect(self):
        try:
            self.client.connect(host=self.target_host)
            self.logger.logger.info("成功连接MQTT服务器")
        except Exception as e:
            raise e
        for i in self.sub_topics:
            self.client.subscribe(i['topic'], 0)
        a = Thread(target=self.client.loop_forever)
        b = Thread(target=self.pub)
        a.start()
        b.start()
        self.care(a,b)
     

    def pub(self):
        # mqtt发布启动函数
        def mqtt_publish(sensor_data, topic, qos=2):
            try:
                self.client.publish(topic=topic, payload=sensor_data, qos=qos)
            except KeyboardInterrupt:
                # 这是网络循环的阻塞形式，直到客户端调用disconnect（）时才会返回。它会自动处理重新连接。
                self.client.disconnect()
                sys.exit(0)

        while True:
            if not self.SEND_MQTT.empty():
                msg = self.SEND_MQTT.get()

                # 将msg['data']转化为字符串，然后进行去除 
                pub_msg = json.dumps(msg['data'])
                #print("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww")
                #print(pub_msg)
                #print(type(pub_msg))
                # 将修改后的replace
                pub_msg = pub_msg.replace("\\", "")
                #print("666666666666666666666666666666666")
                pub_msg = pub_msg.strip('"')
                #print(pub_msg)
                #再转为字典
                pub_msg = ast.literal_eval(pub_msg)
                # 解析msg信息
                Msg = json.dumps(pub_msg,indent=2)
                
                print("hhhhhhhhhhhhhhhhhhhhhhhhhhh",Msg)
                self.client.publish(topic=msg['topic'], payload=Msg, qos=1)
                self.logger.logger.info("主题：" + msg['topic'] + "data:" + Msg + '已经发送成功')

    def __on_message(self, client, userdata, msg):
        Msg = {
            'topic': msg.topic,
            'data': eval(str(msg.payload, 'utf-8').replace('\n', ''))
        }
        try:
            self.logger.logger.info('收到消息：' + '主题：' + msg.topic + 'data:' + str(Msg['data']))
            self.RECEIVING_MQTT.put(Msg)
        except Exception as e:
            self.logger.logger.error('收到错误格式信息' + str(e))
