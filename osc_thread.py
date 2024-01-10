from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
from actuator_utils import *
import global_value as g

IP = "127.0.0.1"
PORT = 8000

cnt = 0

def judge(unused_addr, args, volume):
    if not (g.g.movable() and g.g.beyondable()):
        return
    if g.g.getY() >= g.HM_Y:
        global cnt
        cnt += 1
        if cnt % 10 == 0:
            for client in g.clients:
                client.send_message("/play", action_dict["super"])
            moveY(0)
            sleep(2)
            cnt = 0
        return
    g.g.beyond_lock()
    position = tuple(map(float, volume.replace("(","").replace(")","").split(",")))
    X,Y,Z = transform_leap2actuator(position)
    x = g.g.getX()
    y = g.g.getY()
    print(X,Y,Z,x,y,position)
    if abs(X-x) > 30 or abs(Y-y) > 30:
        g.g.beyond_ok()
        return
    if abs(X-x) < 5 or abs(Y-y) < 5 and Z:
        print(X,Y,Z,x,y,position, "touch")
        hand_touched()
    else:
        print(X,Y,Z,x,y,position, "reach")
        hand_reaching(x-X, y-Y)
    sleep(1)
    g.g.beyond_ok()

def hand_reaching(Xp, Yp):
    x = 10 if Xp>0 else -10
    y = 10 if Yp>0 else -10
    moveXY(x,y,relative=True)
    action = "dodge_R" if x>0 else "dodge_L"
    for client in g.clients:
        client.send_message("/play", action_dict[action])

def hand_touched():
    g.g.touch()
    if g.g.get_touch_count() < 3:
        for client in g.clients:
            client.send_message("/play", action_dict["warp"])
        g.g.move_lock()
        sleep(2)
        g.g.move_ok()
    else:
        g.g.reset_touch()
        for client in g.clients:
            client.send_message("/play", action_dict["rotate"])
        moveXY(g.STAY_X, 250)
        g.g.beyond_lock()
        g.g.reset_realcnt()

"""
ylim = 0.1
zlim = 0.2/0.35
x = -0.1/0.1
X 250~30
Y(z) 0~140
"""
def transform_leap2actuator(position:tuple):
    x,y,z = position
    X = 250-(x+0.1)*(220/0.2)
    Y = (z-0.2)*(140/0.15)
    Z = y < 0.1
    return X,Y,Z

def run():
    dispatcher = Dispatcher()
    dispatcher.map("/index", judge, "ttt")

    server = osc_server.ThreadingOSCUDPServer((IP, PORT), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()