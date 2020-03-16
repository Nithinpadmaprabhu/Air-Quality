from spidev import SpiDev
from enhanced_linearity import *

spi = SpiDev()
spi.open(0, 1)
channel = 1

mq131_data = { "Ozone": [Point(10, 1.1893), Point(50, 2), Point(100, 2.6409), Point(200, 4), Point(500, 6), Point(1000, 8)]}

load_resistance = 1
ratio = 1

r0 = 0

while True:
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    result = ((adc[1] & 3) << 8) + adc[2]
    print(result)

    rs = float(load_resistance * (1024 - result) / float(result))

    for gas in mq131_data.keys():
        y = rs/r0
        local_linearity = local_line(gas, mq131_data, y)
        if local_linearity != None:
            x0, y0, m = local_linearity[0].get_x(), local_linearity[0].get_y(), local_linearity[1]
            gas_concentration = pow(10, ((log10(y) - log10(y0)) / m) + log10(x0))

            val[gas] = str(round(gas_concentration, 5))
            print(val[gas])
