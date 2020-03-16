import time
from spidev import SpiDev

spi = SpiDev()
spi.open(0, 0)
channel = 6

while True:
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    result = ((adc[1] & 3) << 8) + adc[2]
    
    voltage_measured = (3.3 * result) / 1023.0
    temp = (voltage_measured - 0.5) / 10.0
    print("Voltage Measured: ", voltage_measured)
    temp *= 1000.0
    print("Temperature: ", temp)
    time.sleep(2)