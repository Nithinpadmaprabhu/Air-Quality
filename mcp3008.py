'''
Created on 31 July 2017
@author: Yahya Almardeny

This is a software driver for the ADC (MCP3008)

'''

from spidev import SpiDev


class MCP3008:
    def __init__(self, bus=0, device=0):
        self.spi = SpiDev()
        self.spi.open(bus, device) #Connect to the specified SPI device (CS)
    
	############################### Read ######################################
	# Input: the channel to read from (default is 0)
	# Output: raw digital ADc reading
	# Remarks: Technical Note: this is a 12-bit ADC
	########################################################################### 
    def read(self, channel = 0):
        # to initiate communication with MCP, send 3 bytes
        # 0000 0001 | 0         0  0  0  0000 | 0000 00000
        # start bit | SNGL/DIFF D2 D1 D0 XXXX | XXXX XXXXX
        # Perform SPI transaction. CS on RPi will be held active between blocks
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0]) # (0000 1000 + channel) << 4
        # ???? ?nullB9B8 | B7B6B5B4 B3B2B1B0
        # bitmask: keep B9B0 and shift'em to the beginning, the resulted integer + last byte value
        return ((adc[1] & 3) << 8) + adc[2]
    
	
	############################### Close ######################################
	# Disconnects from the interface.
	########################################################################### 
    def close(self):
        self.spi.close()
        