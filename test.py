from mcp3008 import MCP3008
import time
from gp2y import *
import RPi.GPIO as GPIO
#mcp = MCP3008(0,1)
pm = GP2Y(13, 3.3, 0)

while True:
    ch0 = pm.read()
    print(ch0)
    time.sleep(1)
