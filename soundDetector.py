'''
Created on 15 September 2017
@author: Yahya Almardeny

This class for measuring the Noise in the surrounding area
'''

import math

class Sound_Detector():
    def __init__(self, mcp, channel):
        self.mcp = mcp			# ADC object
        self.channel = channel	# channel on ADC to read from (Sound Sensor is connected to)
        
		
    ############################### Read ##################################################
	# Output: pre-formatted String with the reading result (3-digits after decimal point)
	# Remarks: Technical Note: 6-bits for every 1-decible;
	# thus, to capture the noise > 70 dBSPL we need ADC with higher resolution (e.g 24-bit)
	######################################################################################     
    def read(self):
        # 25 is the raw ADC_READING at 39dBA when calibrated via external "Sound Level Meter"
        # the equation is: 20*log(reading/reference)
        sound_pressure = 20 * math.log10(self.mcp.read(self.channel)/25) + 39
        return "{\"Noise dBSPL\":" + "\"" + "{}".format(round(sound_pressure,5)) +  "\"}"