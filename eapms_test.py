from mcp3008 import MCP3008
import time
import RPi.GPIO as GPIO
from gp2y import *
from mq import MQ
from point import Point
from groveO2 import Grove_O2
from soundDetector import Sound_Detector
from tmp36 import TMP36
from humidity import Humidity

if __name = '__main__':
    pass

# Data for MQ sensors from datasheets
mq2_data = {"Smoke":[Point(200,3.45) ,Point(500,2.5), Point(800,2), Point(1000,1.9),
                         Point(1600,1.65), Point(2000,1.5),Point(3000,1.3),Point(5000,0.92), Point(10000,0.6)],
            "LPG":[Point(200,1.75) ,Point(500,1.2), Point(800,0.88), Point(1000,0.68),
                         Point(1600,0.56), Point(2000,0.48),Point(3000,0.38),Point(5000,0.28), Point(10000,0.24)],
            "Propane":[Point(200,1.78) ,Point(500,1.2), Point(800,0.88), Point(1000,0.7),
                         Point(1600,0.6), Point(2000,0.5),Point(3000,0.40),Point(5000,0.30), Point(10000,0.25)],
            "CH4":[Point(200,3) ,Point(500,2.4), Point(800,1.9), Point(1000,1.8),
                         Point(1600,1.6), Point(2000,1.4),Point(3000,1.3),Point(5000,0.92), Point(10000,0.7)]};

mq135_data = {"CO2":[Point(10,2.5) ,Point(40,1.5), Point(100,1.1), Point(200,0.8)],
                 "CO":[Point(10,2.9) ,Point(40,1.95), Point(100,1.7), Point(200,1.5)],
         "NH4":[Point(10,2.7) ,Point(40,1.53), Point(100,1), Point(200,0.785)],
                 "Benzene":[Point(10,1.6) ,Point(40,1.1), Point(100,0.8), Point(200,0.65)]};

mq131_data = {"Ozone":[Point(5,6),Point(10,4),Point(20, 1.5),Point(100,0.5)],
              "NO2": [Point(5,9),Point(10,8), Point(20,7), Point(100,4.5)],
              "CL2": [Point(5,8),Point(10,6.8), Point(20,4.8), Point(100,0.8)]};

so2_data =  {"SO2":[Point(35,1),Point(100,1.5),Point(200, 1.95),
                    Point(300,2.2),Point(400,2.35),Point(500,2.45),Point(600,2.5)]};

mcp = MCP3008()
mq2 = MQ('MQ2', mcp, 0, 5, 9.8, mq2_data)
mq135 = MQ('MQ135', mcp, 1, 20, 3.75, mq135_data)
mq131 = MQ('MQ131', mcp, 2, 20, 20, mq131_data)
o2 = Grove_O2(mcp, 3, 3.3, 7.43)
noise = Sound_Detector(mcp, 4)
sh12 = MQ('2SH12', mcp, 5, 50, 6, so2_data)
tmp36 = TMP36(mcp, 6, 3.3)
humidity = Humidity(mcp, 7, 3.3)
pm = GP2Y(13, 3.3, 1)

print('---------------------------------------')
print('Reading MQ-2 sensor...')
mq2R = mq2.read()
print(mq2R)
print('Finished reading MQ-2 sensor')
print('---------------------------------------')

print('---------------------------------------')
print('Reading MQ-135 sensor...')
mq135R = mq135.read()
print(mq135)
print('Finished reading MQ-135 sensor')
print('---------------------------------------')

print('---------------------------------------')
print('Reading MQ-131 sensor...')
mq131R = mq131.readPPB()
print(mq131R)
print('Finished reading MQ-131 sensor')
print('---------------------------------------')

print('---------------------------------------')
print('Reading O2 sensor...')
o2R = o2.read()
print(mq131R)
print('Finished reading O2 sensor')
print('---------------------------------------')

print('---------------------------------------')
print('Reading Noise sensor...')
noiseR = noise.read()
print(noiseR)
print('Finished reading Noise sensor')
print('---------------------------------------')

print('---------------------------------------')
print('Reading SO2 sensor...')
sh12R = sh12.read()
print(sh12R)
print('Finished reading SO2 sensor')
print('---------------------------------------')

print('---------------------------------------')
print('Reading Temperature sensor...')
tempR = tmp36.read()
print(tempR)
print('Finished reading Temperature sensor')
print('---------------------------------------')

print('---------------------------------------')
print('Reading Humidity sensor...')
humidityR = humidity.read(tmp36.readTemp())
print(humidityR)
print('Finished reading Humidity sensor')
print('---------------------------------------')

print('---------------------------------------')
print('Reading PM sensor...')
pmR = pm.read()
print(pmR)
print('Finished reading PM sensor')
print('---------------------------------------')
