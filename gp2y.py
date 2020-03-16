'''
Created on 15 September 2017
@author: Yahya Almardeny

This class for the dust sensor (GY2P) which detects the particulate matters (PM2.5 & PM10)
Its output is analog but it requires a digital sginal from RPi to switch off/on the LED inside it
'''

import RPi.GPIO as GPIO
from mcp3008 import MCP3008
import time

class GP2Y():
    def __init__(self, pin, sys_volt, device):
        self.pin = pin					#The pin on RPi that this sensor LED will be connected to
        self.sys_volt = float(sys_volt)	# Vcc
        self.ADC_RES = 1023.0			# MCP Resolution
        self.mcp = MCP3008(0,device)	# MCP object, note that device is either 0 or 1 (in this case is gonna be 1)
        GPIO.setmode(GPIO.BOARD)		# BOARD mode which follows the numbering on the RPi
        GPIO.setup(self.pin, GPIO.OUT)	# RPi will signal out to the LED 
       
	############################### Read ###########################################
	# Output: pre-formatted String with the reading result (4-digits after decimal point)
	# Remarks: Sampling time is 32 nano-second for each reading (from datasheet)
	###############################################################################
    def read(self):
        #turn on the internal LED
        GPIO.output(self.pin, 0)
        #give sampling time
        time.sleep(0.00028)
        #read analog and convert to mV
        voltage_measured = ((self.sys_volt * self.mcp.read()) / self.ADC_RES)
        # give delta time
        time.sleep(0.00004)
        #switch off the LED
        GPIO.output(self.pin, 1)
        #apply linear equation (the Line from datasheet)
        dustDensity = (0.17 * voltage_measured) - 0.1
        if dustDensity<0.0:
            dustDensity = 0.000001
        return "{\"Particulate Matter mg/m3\":" + "\"" + "{}".format(round(dustDensity,6)) +  "\"}"

 
