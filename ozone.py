import time, os, csv, json
from enhanced_linearity import *
from datetime import datetime

from spidev import SpiDev

load_resistance = 20
ratio = 20

spi = SpiDev()
spi.open(0, 0)
channel = 2

data = { "Ozone": [ Point(5, 4), Point(10, 2.3), Point(10, 1.25), Point(20, 1.25), Point(50, 0.5), Point(100, 0.28) ] }

while True:
    # Get reading from ADC
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    adc_reading = ((adc[1] & 3) << 8) + adc[2]

    print("ADC: " + str(adc_reading))

    rs = float(load_resistance * (1024 - adc_reading) / float(adc_reading))

    print("RS: " + str(rs))

    val = {}
    for gas in data.keys():
        y = rs
        local_linearity = local_line(gas, data, y)
        if local_linearity != None:
            x0, y0, m = local_linearity[0].get_x(), local_linearity[0].get_y(), local_linearity[1]
            gas_concentration = pow(10, ((log10(y)-log10(y0))/m) + log10(x0))
            val[gas] = str(round(gas_concentration, 5))
        else:
            val[gas] = "{}:{},".format(gas, -1)

    print(json.dumps(val))

    time.sleep(2)
