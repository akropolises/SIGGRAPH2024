import global_value as g
from time import sleep
from random import random

"""
ylim = 0.1
zlim = 0.06/0.41
x = -0.14/0.21
X 280~0
Y(z) 0~250

X280
Y250
speed20000も可
"""

action_dict = {"default":0, "appear":1, "disappear":2, "dodge_L":3, "dodge_R":4, "left":5, "right":6, "rotate":7, "super":8, "warp":9, "move":10, "turn":11}

def moving():
    g.ser.write(str.encode("M400\n"))
    g.ser.write(str.encode("M118 moved!\n"))
    g.g.move_lock()

def wait_moved():
    while True:
        r = g.ser.readline()
        print(r)
        if r == b"moved!\r\n":
            print("break")
            break
    g.g.move_ok()

def initialize():
    g.ser.write(str.encode("G28 XY\n"))
    while True:
        r = g.ser.readline()
        print(r)
        if r == b"ok\n":
            print("break")
            break
    g.g.setX(0)
    g.g.setY(0)
    g.g.move_ok()
    g.ser.write(str.encode("G1 X"+str(g.STAY_X) + " Y"+str(g.STAY_Y)+"\n"))
    moving()
    g.g.setX(g.STAY_X)
    g.g.setY(g.STAY_Y)

def moveX(x:int, relative = False):
    if not g.g.movable():
        return
    if relative:
        x = g.g.getX() + x
    x = max(g.g.minX(), x)
    x = min(g.g.maxX(), x)
    g.ser.write(str.encode("G1 X"+str(x)+"\n"))
    moving()
    g.g.setX(x)

def moveY(y:int, relative = False):
    if not g.g.movable():
        return
    if relative:
        y = g.g.getY() + y
    x = g.g.getX()
    # assert(0<=y<=250)
    if g.g.getY() < g.HM_Y < y or y < g.HM_Y < g.g.getY() or y == g.HM_Y:
        g.ser.write(str.encode("G1 X"+str(g.HM_X)+"\n"))
        g.ser.write(str.encode("G1 Y"+str(g.HM_Y)+"\n"))
        moving()
        while not g.g.movable():
            continue
        for client in g.clients:
            client.send_message("/beyond", "b")
    g.g.setY(y)
    x = max(g.g.minX(), x)
    x = min(g.g.maxX(), x)
    g.ser.write(str.encode("G1 X"+str(x)+" Y"+str(y)+"\n"))
    moving()

def moveXY(x:int, y:int, relative = False):
    if not g.g.movable():
        return
    if relative:
        x = g.g.getX() + x
        y = g.g.getY() + y
    x = max(g.g.minX(), x)
    x = min(g.g.maxX(), x)
    # assert(0<=y<=250)
    if g.g.getY() < g.HM_Y < y or y < g.HM_Y < g.g.getY() or y == g.HM_Y:
        g.ser.write(str.encode("G1 X"+str(g.HM_X)+"\n"))
        g.ser.write(str.encode("G1 Y"+str(g.HM_Y)+"\n"))
        moving()
        while not g.g.movable():
            continue
        for client in g.clients:
            client.send_message("/beyond", "b")
        r = random()
        print(r)
        if r < 0.5:
            g.ser.write(str.encode("G1 Y"+str(y)+"\n"))
    g.ser.write(str.encode("G1 X"+str(x) + " Y"+str(y)+"\n"))
    moving()
    g.g.setX(x)
    g.g.setY(y)

def stay():
    for client in g.clients:
        # client.send_message("/play", action_dict["disappear"])
        client.send_message("/play", action_dict["move"])
    moveXY(g.STAY_X, g.STAY_Y)
    g.g.beyond_lock()

def move250_circle():
    if not g.g.movable():
        return
    g.ser.write(str.encode("G2 X250 Y0 R115\n"))
    moving()
    g.g.setX(250)
    g.g.setY(0)

def move30_circle():
    if not g.g.movable():
        return
    g.ser.write(str.encode("G3 X30 Y0 R115\n"))
    moving()
    g.g.setX(30)
    g.g.setY(0)