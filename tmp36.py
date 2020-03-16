'''
Created on 15 September 2017
@author: Yahya Almardeny

This class for measuring the Temperature in the surrounding area
'''

class TMP36():
    def __init__(self, mcp, channel, sys_volt):
        self.mcp = mcp						# ADC Object
        self.channel = channel				# channel on ADC to read from (Temp Sensor is connected to)
        self.sys_volt = float(sys_volt)		# Vcc
        self.ADC_RES = 1023.0				# ADC Resolution
        self.temp = 0.0						# Global Scope, to be used for both methods later


	############################### Read ###########################################
	# Output: pre-formatted String with the reading result (3-digits after decimal point)
	# Remarks: Technical Note: TMP36 Sensor trustworthiness is questionable
	###############################################################################
    def read(self):
        #ADC Resolution/System Voltage = ADC Reading / Voltage Measured
        voltage_measured = (self.sys_volt * self.mcp.read(self.channel)) / self.ADC_RES
        # slope from datasheet is 10
        # there is offset by 0.5 (i.e b is 0.5)
        # the linearity y = m*x + b -> x = (y-b/m)
        self.temp = (voltage_measured -0.5) / 10.0
        # convert from volt to milli-volt -> multiply by 1000
        self.temp  *= 1000.0
        return "{\"Temprature " + u'\N{DEGREE SIGN}' + "C\":" + "\"" + "{}".format(round(self.temp ,5)) +  "\"}"


	############################### Read Temperature ###############################
	# Output: reading result as a number
	# Remarks: This to be used for the Humidity Sensor
	###############################################################################
    def readTemp(self):
        return self.temp
