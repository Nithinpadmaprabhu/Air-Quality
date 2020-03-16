'''
Created on 01 October 2017
@author: Yahya Almardeny

This helper file to communicate with the MySQL Server and
send data to the database on interval time

'''


import pymysql,json

# global scope vars for database
global smoke,propane,LPG,CH4,CO2,benzene,NH4,CO,NO2,CL2,Ozone,SO2,O2,noiseV,temp,rh,pmV
smoke=propane=LPG=CH4=CO2=benzene=NH4=CO=NO2=CL2=Ozone=SO2=O2=noiseV=temp=rh=pmV = 0.0
global db

###################### Initialize Connection with DB #######################
# Input: cursor, deviceName , senosrs readings in JSON format
# Output: the cursor object of this cconnection
###########################################################################
def connect_to_mysqlServer(serverIp, username, password, fileName, dbName):
    global db
    cursor = None
    try:
        db = pymysql.connect(serverIp, username, password, fileName)
        cursor = db.cursor()
        cursor.execute("use " +dbName+";")
    except Exception as msg:
        print(msg)
    return cursor

############################ Send Data to DB ###############################
# Input: cursor, deviceName , senosrs readings in JSON format
# Output: cursor
# Remarks: Send the average of readings over pre-set specific time to DB
###########################################################################
def send_to_database(cursor, deviceName, counter, limit, *args):
    data = args
    mq2, mq135, mq131, so2R, o2R, noiseR, tmp36, humidityR, pmR = json.loads(data[0]),json.loads(data[1]),json.loads(data[2]),json.loads(data[3]),json.loads(data[4]),json.loads(data[5]),json.loads(data[6]),json.loads(data[7]), json.loads(data[8])
    global smoke, propane, LPG, CH4, CO2, benzene, NH4, CO, NO2, CL2, Ozone, SO2, O2, noiseV, temp, rh, pmV, db
    smoke += float(mq2['Smoke'])
    propane += float(mq2['Propane'])
    LPG += float(mq2['LPG'])
    CH4 += float(mq2['CH4'])
    CO2 += float(mq135['CO2'])
    benzene += float(mq135['Benzene'])
    NH4 += float(mq135['NH4'])
    CO += float(mq135['CO'])
    NO2 += float(mq131['NO2'])
    CL2 += float(mq131['CL2'])
    Ozone += float(mq131['Ozone'])
    SO2 += float(so2R['SO2'])
    O2 +=  float(o2R['O2%'])
    noiseV += float(noiseR['Noise dBSPL'])
    temp += round(float(tmp36['Temprature °C']))
    rh += float(humidityR['Relative Humidity % '])
    pmV += float(pmR['Particulate Matter mg/m3'])

    if counter>=limit:
        try:
            cursor.callproc('addReading', [deviceName, float(smoke/limit), float(propane/limit), float(LPG/limit), float(CH4/limit), float(CO2/limit), float(benzene/limit), float(NH4/limit), float(CO/limit), float(NO2/limit), float(CL2/limit), float(Ozone/limit), float(SO2/limit), float(O2/limit), float(noiseV/limit), float(temp/limit), float(rh/limit), float(pmV/limit)])
            db.commit()
            print('Remote data recorded.')
        except Exception as mssg:
            print(mssg)
        finally:
            counter = 0
            smoke=propane=LPG=CH4=CO2=benzene=NH4=CO=NO2=CL2=Ozone=SO2=O2=noiseV=temp=rh=pmV = 0.0

    counter += 1
    return counter

def reset(counter, *args):
    global smoke, propane, LPG, CH4, CO2, benzene, NH4, CO, NO2, CL2, Ozone, SO2, O2, noiseV, temp, rh, pmV, db
    smoke=propane=LPG=CH4=CO2=benzene=NH4=CO=NO2=CL2=Ozone=SO2=O2=noiseV=temp=rh=pmV = 0.0
    counter = 0
    return counter
