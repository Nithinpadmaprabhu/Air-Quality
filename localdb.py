'''
Created on 17 January 2018
@author: Ryan McCloskey

Connects to a local SQL database using SQLite, and send_to_data
to this database at a specified interval.
'''

import sqlite3, time, json
import db as db

# Global variables for local database
global localdb

global smoke_l, propane_l, LPG_l, CH4_l, CO2_l, benzene_l, NH4_l, CO_l, NO2_l, CL2_l, Ozone_l, SO2_l, O2_l, noiseV_l, temp_l, rh_l, pmV_l
smoke_l=propane_l=LPG_l=CH4_l=CO2_l=benzene_l=NH4_l=CO_l=NO2_l=CL2_l=Ozone_l=SO2_l=O2_l=noiseV_l=temp_l=rh_l=pmV_l = 0.0

# The location of the SQLite database file
global sqlite_file
sqlite_file = '/home/pi/Desktop/EAPMS/eapms_db.sqlite'

###################### Initialise Connection with DB #######################
# Input: fileName
# Output: the cursor object of this connection
###########################################################################
def connect_to_sqlite_database(fileName):
    global localdb
    c = None
    try:
        # Makes a connection to the SQLite database specified by the fileName parameter.
        localdb = sqlite3.connect(fileName)
        c = localdb.cursor()
        # Create the 'reading' table in the SQLite database if it has not already been created.
        c.execute("CREATE TABLE IF NOT EXISTS `reading` (`place` varchar(255) NOT NULL,`day` varchar(2) NOT NULL,`month` varchar(2) NOT NULL,`year` varchar(4) NOT NULL,`time` varchar(9) NOT NULL,`smoke` float DEFAULT NULL,`propane` float DEFAULT NULL,`LPG` float DEFAULT NULL,`ch4` float DEFAULT NULL,`co2` float DEFAULT NULL,`benzene` float DEFAULT NULL,`nh4` float DEFAULT NULL,`co` float DEFAULT NULL,`no2` float DEFAULT NULL,`cl2` float DEFAULT NULL,`ozone` float DEFAULT NULL,`so2` float DEFAULT NULL,`o2` float DEFAULT NULL,`noise` float DEFAULT NULL,`temp` float DEFAULT NULL,`rh` float DEFAULT NULL,`pm` float DEFAULT NULL,PRIMARY KEY (`day`,`month`,`year`,`time`));")
    except Exception as msg:
        print(msg)
    return c

############################ Send Data to DB ###############################
# Input: cursor, deviceName, counter, limit, sensor readings in JSON format
# Output: counter
# Remarks: Send the average of readings over specified period to DB
###########################################################################
def send_to_database(cursor, deviceName, counter, limit, *args):
    try:
        data = args
        mq2, mq135, mq131, so2R, o2R, noiseR, tmp36, humidityR, pmR = json.loads(data[0]),json.loads(data[1]),json.loads(data[2]),json.loads(data[3]),json.loads(data[4]),json.loads(data[5]),json.loads(data[6]),json.loads(data[7]), json.loads(data[8])
        global smoke_l, propane_l, LPG_l, CH4_l, CO2_l, benzene_l, NH4_l, CO_l, NO2_l, CL2_l, Ozone_l, SO2_l, O2_l, noiseV_l, temp_l, rh_l, pmV_l, localdb
        smoke_l += float(mq2['Smoke'])
        propane_l += float(mq2['Propane'])
        LPG_l += float(mq2['LPG'])
        CH4_l += float(mq2['CH4'])
        CO2_l += float(mq135['CO2'])
        benzene_l += float(mq135['Benzene'])
        NH4_l += float(mq135['NH4'])
        CO_l += float(mq135['CO'])
        NO2_l += float(mq131['NO2'])
        CL2_l += float(mq131['CL2'])
        Ozone_l += float(mq131['Ozone'])
        SO2_l += float(so2R['SO2'])
        O2_l +=  float(o2R['O2%'])
        noiseV_l += float(noiseR['Noise dBSPL'])
        temp_l += round(float(tmp36['Temprature °C']))
        rh_l += float(humidityR['Relative Humidity % '])
        pmV_l += float(pmR['Particulate Matter mg/m3'])

    except Exception as msg:
        print(msg)

    if counter >= limit:
        try:
            t = time.strftime("%d-%m-%Y %H:%M:%S")
            day = t[:2]
            month = t[3 : 5]
            year = t[6 : 10]
            timestamp = t[11:]

            statement = "INSERT INTO reading (place, day, month, year, time, smoke, propane, LPG, ch4, co2, benzene, nh4, co, no2, cl2, ozone, so2, o2, noise, temp, rh, pm) VALUES(\'{place}\', \'{day}\', \'{month}\', \'{year}\', \'{t}\', {smoke}, {propane}, {LPG}, {ch4}, {co2}, {benzene}, {nh4}, {co}, {no2}, {cl2}, {ozone}, {so2}, {o2}, {noise}, {temp}, {rh}, {pm});".format(place=deviceName, day=day, month=month, year=year, t=timestamp, smoke=smoke_l/limit, propane=propane_l/limit, LPG=LPG_l/limit, ch4=CH4_l/limit, co2=CO2_l/limit, benzene=benzene_l/limit, nh4=NH4_l/limit, co=CO_l/limit, no2=NO2_l/limit, cl2=CL2_l/limit, ozone=Ozone_l/limit, so2=SO2_l/limit, o2=O2_l/limit, noise=noiseV_l/limit, temp=temp_l/limit, rh=rh_l/limit, pm=pmV_l/limit)
            cursor.execute(statement)
            localdb.commit()
            print('Local data recorded.')

        except Exception as mssg:
            print(mssg)
        finally:
            counter = 0
            smoke_l=propane_l=LPG_l=CH4_l=CO2_l=benzene_l=NH4_l=CO_l=NO2_l=CL2_l=Ozone_l=SO2_l=O2_l=noiseV_l=temp_l=rh_l=pmV_l = 0.0

    counter += 1
    return counter
