#!/usr/bin/python3

'''
Created on 01 October 2017
@author: Yahya Almardeny

This is the main entry point to the program
The Flow of this program goes here

'''

import time as t , socket, os, datetime
from mq import MQ
from mcp3008 import MCP3008
from point import Point
from groveO2 import Grove_O2
from soundDetector import Sound_Detector
from tmp36 import TMP36
from humidity import Humidity
from gp2y import *
import promptWindow as window
import db as db
import localdb as localdb

if __name__ == '__main__':
        pass

    ########################### Format JSON ############################
    # Input: device name, sensors readings in JSON format
    # Output: data
    ###################################################################
def format(deviceName, *args):
    data = "{\"" +deviceName+"\":["
    for i in range(len(args)):
        if(i==len(args)-1):
            data += str(args[i])
        else:
            data += str(args[i]) +","

    data += "]}"
    return data

while True:

    # global scope vars to set the interval time for sending data to the database (3600 means every 1 hour)
    global counter, limit
    counter, limit = 0, 30 # every 30 second , that means 120 readings in one hour of deployment (gives nice graph, not crowded)

    global localcounter
    localcounter = 0

    # Ask user for Device and Server Information at startup in the first run
    window.get_information("/home/pi/Desktop/EAPMS/device_info.csv")


    # Data for MQ Sensors from Datasheet
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

    new_mq131_data = { "Ozone": [Point(10, 1.1893), Point(50, 2), Point(100, 2.6409), Point(200, 4), Point(500, 6), Point(1000, 8)] }

    mq131_data = {"Ozone":[Point(5,6),Point(10,4),Point(20, 1.5),Point(100,0.5)],
                  "NO2": [Point(5,9),Point(10,8), Point(20,7), Point(100,4.5)],
                  "CL2": [Point(5,8),Point(10,6.8), Point(20,4.8), Point(100,0.8)]};

    so2_data =  {"SO2":[Point(35,1),Point(100,1.5),Point(200, 1.95),
                        Point(300,2.2),Point(400,2.35),Point(500,2.45),Point(600,2.5)]};



    # Initalize the required sensors devices
    mcp = MCP3008()
    mq2 = MQ("MQ2", mcp,0,5,9.8, mq2_data)
    mq135 = MQ("MQ135", mcp,1,20,3.75, mq135_data)
    mq131 = MQ("MQ131", mcp, 2, 20,20,new_mq131_data)
    o2 = Grove_O2(mcp, 3, 3.3, 7.43)
    noise = Sound_Detector(mcp, 4)
    sh12 = MQ("2SH12", mcp, 5, 50, 6, so2_data)
    tmp36 = TMP36(mcp, 6, 3.3)
    humidity = Humidity(mcp, 7, 3.3)
    pm = GP2Y(13, 3.3, 1)


    try:
        # Initialize Connection with UDP Server & MySQL Server
        device_infoFile = open("/home/pi/Desktop/EAPMS/device_info.csv", 'r')
        info = device_infoFile.read().split(',')
        deviceName, serverIp, port = info[0],str(info[1]), int(info[2])
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cursor = db.connect_to_mysqlServer(serverIp, 'pi', 'pi', 'eapmsDB', 'data')
        localcursor = localdb.connect_to_sqlite_database('/home/pi/Desktop/EAPMS/eapms_db.sqlite')

        while True:
            mq2R, mq135R, mq131R, sh12R, o2R, noiseR, tempR, humidityR, pmR = mq2.read(),mq135.read(),mq131.read(), sh12.read(), o2.read(), noise.read(), tmp36.read(), humidity.read(tmp36.readTemp()), pm.read();
            data = format(deviceName,mq2R, mq135R, mq131R, sh12R, o2R, noiseR, tempR, humidityR, pmR)
            print(data)
            localcounter = localdb.send_to_database(localcursor, deviceName, localcounter, limit, mq2R, mq135R, mq131R, sh12R, o2R, noiseR, tempR, humidityR, pmR)
            try:
                serverSocket.sendto(bytes(data, 'UTF-8'), (serverIp, port))  # send data in JSON format to the Server
            except Exception as msg:
                print(msg)
            try:
                counter = db.send_to_database(cursor, deviceName, counter, limit, mq2R, mq135R, mq131R, sh12R, o2R, noiseR, tempR, humidityR, pmR)  # send data to database on the Server
            except Exception as msg:
                print(msg)
            t.sleep(1)
    except Exception as mssg:
        GPIO.cleanup()
        if not os.path.isfile("/home/pi/Desktop/EAPMS/log.txt"):
            logFile = open("/home/pi/Desktop/EAPMS/log.txt", 'w+')
        else:
            logFile = open("/home/pi/Desktop/EAPMS/log.txt", 'a')
        date = datetime.date.today()
        time = datetime.datetime.now().time()
        log = str(date) + " " + str(time) + " " + str(mssg) +"\n"
        logFile.write(log)
        logFile.close()

    t.sleep(10) # wait 10 seconds before restart
        #window.notify_erro(str(mssg))
