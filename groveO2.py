'''
Created on 15 September 2017
@author: Yahya Almardeny

This class for measuring the Oxygen level in air
'''

class Grove_O2():
    def __init__(self, mcp, channel, sys_volt, slope):
        self.mcp = mcp						# ADC object
        self.channel = channel				# channel on ADC to read from (O2 Sensor is connected to)
        self.sys_volt = float(sys_volt)		# Vcc
        self.slope = slope					# Line Slope (from datasheet)
        self.ADC_RES = 1023.0				# ADC Resulotion
        self.AMP = 121 # 121 or 201, depending on sensor version
        # 201 for sensor version 1.0
        # 121 for sensor version 1.1

    ############################### Read ###########################################
	# Output: pre-formatted String with the reading result (3-digits after decimal point)
	# Remarks: datasheet needs to be read
	###############################################################################
    def read(self):
        #ADC Resolution/System Voltage = ADC Reading / Voltage Measured
        voltage_measured = (self.sys_volt * self.mcp.read(self.channel)) / self.ADC_RES
        # convert from volt to ampere, then to microA then to percentage
        # 201 is constant resistance value to convert to ampere
        # from ampere to microAmpere we multiply by 1000000
        # to convert to percentage like(number%) we divide by 100
        sensor_value = (voltage_measured / AMP) * 10000.0
        # the relation between O2 level and mA from datasheet is linear
        o2_level = sensor_value/self.slope
        return "{\"O2%\":" + "\"" + "{}".format(round(o2_level,5)) +  "\"}"
