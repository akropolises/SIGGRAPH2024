from readchar import readkey,key
import global_value as g
from actuator_utils import *

def run():
   while True:
      c = readkey()
      if c == "q":
         g.ser.write(str.encode("M118 quit\n"))
         break
      elif c == "s":
         g.ser.write(str.encode("M118 stay\n"))
      elif c == "h":
         moveXY(g.HM_X, g.HM_Y)
      elif c == key.LEFT:
         moveX(10, relative=True)
      elif c == key.RIGHT:
         moveX(-10, relative=True)
      elif c == key.UP:
         moveY(10, relative=True)
      elif c == key.DOWN:
         moveY(-10, relative=True)
      elif c == key.SPACE:
         g.ser.write(str.encode("M114\n"))
         print(g.g.getX(), g.g.getY())
      elif c == key.BACKSPACE:
         for client in g.clients:
            client.send_message("/play", 1)
         if g.g.getY() == 250:
            moveXY(g.STAY_X, 0)
         else:
            moveXY(g.STAY_X, 250)
      else:
         for client in g.clients:
            if "0" <= c <= "9":
               client.send_message("/play", int(c))
            elif c == "r":
               client.send_message("/reflect", c)
            elif c == "b":
               client.send_message("/beyond", c)
            elif c == "R":
               client.send_message("/reset", c)
            else:
               g.g.reset_cnt()