import threading
class GlobalValue:
    def __init__(self) -> None:
        self.__X = -10
        self.__Y = -10
        self.__lock = threading.Lock()
        self.__movable = False
        self.__beyondable = False
        self.__count = 0
        self.__touch_count = 0
        self.__real_count = 0
    
    #XY関係
    def setX(self, value):
        self.__lock.acquire()
        if not (0<=value<=280):
            value = max(0, value)
            value = min(280, value)
        self.__X = value
        self.__lock.release()

    def setY(self, value):
        self.__lock.acquire()
        if not (0<=value<=250):
            value = max(0, value)
            value = min(250, value)
        self.__Y = value
        self.__lock.release()
    
    def maxX(self):
        if self.__Y > HM_Y:
            return 280
        else:
            return 250

    def minX(self):
        if self.__Y > HM_Y:
            return 0
        else:
            return 30 
    
    def getX(self):
        return self.__X
    
    def getY(self):
        return self.__Y

    # movable関係
    def move_lock(self):
        self.__lock.acquire()
        self.__movable = False
        self.__count = 0
        self.__lock.release()

    def move_ok(self):
        self.__lock.acquire()
        self.__movable = True
        self.__lock.release()
    
    def movable(self):
        return self.__movable

    # beyondable関係
    def beyond_lock(self):
        self.__lock.acquire()
        self.__beyondable = False
        self.__lock.release()
    
    def beyond_ok(self):
        self.__lock.acquire()
        self.__beyondable = True
        self.__lock.release()
    
    def beyondable(self):
        return self.__beyondable

    # count関係
    def cntUP(self):
        if not self.__movable:
            return
        self.__lock.acquire()
        self.__count += 1
        self.__lock.release()

    def reset_cnt(self):
        self.__lock.acquire()
        self.__count = 0
        self.__lock.release()

    def getcnt(self):
        return self.__count
    
    # touch_count関係
    def touch(self):
        self.__lock.acquire()
        self.__touch_count += 1
        self.__lock.release()
    
    def reset_touch(self):
        self.__lock.acquire()
        self.__touch_count = 0
        self.__lock.release()
    
    def get_touch_count(self):
        return self.__touch_count
    
    # real_count関係
    def realcntUP(self):
        if not self.__movable:
            return
        self.__lock.acquire()
        self.__real_count += 1
        self.__lock.release()

    def reset_realcnt(self):
        self.__lock.acquire()
        self.__real_count = 0
        self.__lock.release()

    def get_realcnt(self):
        return self.__real_count

g = GlobalValue()
HM_Y = 100
HM_X = 140
STAY_X = 0
STAY_Y = 250

import serial
import time
"""アクチュエータと接続"""
ser = serial.Serial("COM4", 250000, timeout=0.5)
time.sleep(1)

from pythonosc import udp_client
"""OSC setup"""
# IP = ["127.0.0.1"]
IP = ["157.82.206.185", "157.82.207.199"]
PORT = 8000
clients = []
for ip in IP:
    clients.append(udp_client.SimpleUDPClient(ip, PORT))