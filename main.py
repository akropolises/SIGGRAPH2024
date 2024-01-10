import threading
import key_thread
import osc_thread
from actuator_utils import *
import global_value as g

t_o = threading.Thread(target=osc_thread.run)
t_o.setDaemon(True)
t_o.start()

t_k = threading.Thread(target=key_thread.run)
t_k.setDaemon(True) 
t_k.start()

initialize()
for client in g.clients:
    client.send_message("/reset", 0)
"""ここまで初期セットアップ"""

while True:
    r = g.ser.readline()
    print(r)
    if r == b"quit\r\n":
        break
    if r == b"moved!\r\n":
        g.g.move_ok()
        continue
    if r[:2] == b"X:":
        print(g.g.getX(), g.g.getY())
        continue
    print("through",g.g.getcnt())
    if not g.g.movable():
        continue
    g.g.cntUP()
    if g.g.getY() > g.HM_Y and g.g.getcnt() > 10:
        action = "right" if g.g.getX() < 140 else "left"
        for client in g.clients:
            client.send_message("/play", action_dict[action])
        moveX(280-g.g.getX())
        g.g.reset_cnt()
        continue
    if g.g.getcnt() <= 20:
        continue
    if g.g.get_realcnt() < 3:
        g.g.realcntUP()
        if g.g.getX()<g.HM_X:
            move250_circle()
        else:
            move30_circle()
        # moveXY(280-g.g.getX(),0)
        action = "turn" if g.g.get_realcnt()%2 else "move"
        for client in g.clients:
            client.send_message("/play", action_dict[action])
    else:
        g.g.reset_realcnt()
        t_s = threading.Thread(target=stay)
        t_s.setDaemon(True)
        t_s.start()