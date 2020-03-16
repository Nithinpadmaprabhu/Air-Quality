'''
Created on 15 September 2017
@author: Yahya Almardeny

This class for measuring the Relative Humidity level in air
'''

class Humidity():
    def __init__(self, mcp, channel, sys_volt):
        self.mcp = mcp						# ADC object
        self.channel = channel				# channel on ADC to read from (RH Sensor is connected to)
        self.sys_volt = float(sys_volt)		# Vcc
        self.ADC_RES = 1023.0				# ADC Resolution
        
		
    ############################### Read ###########################################
	# Input: temperature
	# Output: pre-formatted String with the reading result (3-digits after decimal point)
	# Remarks: The result heavily depends on the mesaured Temperature. 
	# Technically speaking, this sensor gets affected by light (keep it in dark) 
	###############################################################################    
    def read(self, temp):
        #ADC Resolution/System Voltage = ADC Reading / Voltage Measured
        voltage_measured = (self.sys_volt * self.mcp.read(self.channel)) / self.ADC_RES
        # from datasheet, at 25C when vout=0.8v ->  HR=0%, when vout=3.9v -> RH=100%
        # we can do scatter plot in which (y-axis is humidity and x-axis is analog reading)
        # for 25C the equation is %RH = mX + b
        # Vout = (Vsupply)(0.0062(Sensor RH) + 0.16), we need to find out Sensor RH
        sensor_RH = ((voltage_measured / (0.0062 * self.sys_volt)) - 25.81)
        # to get true humidity at specific temperature 
        true_RH = sensor_RH / (1.0546 - (0.00216 * temp))
        return "{\"Relative Humidity % \":\"" + "{}".format(round(true_RH,5)) +  "\"}"


