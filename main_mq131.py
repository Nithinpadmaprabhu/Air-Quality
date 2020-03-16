import time as t, socket, os, datetime, json, csv
from mq import MQ
from mcp3008 import MCP3008
from point import Point
import promptWindow as window

if __name__ == '__main__':
    pass

def format(deviceName, *args):
    data = "{\"" + deviceName + "\":["
    for i in range(len(args)):
        if(i == len(args)-1):
            data += str(args[i])
        else:
            data += str(args[i]) + ","

    data += "]}"

    return data

while True:
    window.get_information("/home/pi/Desktop/EAPMS/device_info.csv")

    mq131_data = {"Ozone":[Point(10,1.1893),Point(50,2),Point(100, 2.6409),Point(200,4),Point(500,6),Point(1000,8)],
                  "NO2": [Point(5,9),Point(10,8), Point(20,7), Point(100,4.5)],
                  "CL2": [Point(5,8),Point(10,6.8), Point(20,4.8), Point(100,0.8)]}

    mcp = MCP3008()
    mq131 = MQ("MQ131", mcp, 2, 20, 20, mq131_data)

    counter = 0
    limit = 30

    try:
        device_infoFile = open("/home/pi/Desktop/EAPMS/device_info.csv", 'r')
        info = device_infoFile.read().split(',')
        deviceName = info[0]
        
        ozone = 0
        cl2 = 0

        while True:
            if counter == limit:
                ozone /= limit
                cl2 /= limit
                
                if not os.path.isfile("/home/pi/Desktop/EAPMS/mq131_log.csv"):
                    logfile = open("/home/pi/Desktop/EAPMS/mq131_log.csv", 'w+')
                    writer = csv.DictWriter(logfile, fieldnames=['ozone', 'cl2'])
                    writer.writeheader()
                else:
                    logfile = open("/home/pi/Desktop/EAPMS/mq131_log.csv", 'a')
                    
                writer = csv.DictWriter(logfile, fieldnames=['ozone', 'cl2'])
                writer.writerow({'ozone': ozone, 'cl2': cl2})
                
                print(str(counter))
                print('data written')
                
                counter = 0
                ozone = 0
                cl2 = 0
            mq131R = mq131.read()
            data = format(deviceName, mq131R)
            print(json.loads(mq131R))
            mq = json.loads(mq131R)
            print(mq['Ozone'])
            ozone += float(mq['Ozone'])
            cl2 += float(mq['CL2'])
            

            counter += 1

            t.sleep(1)

    except Exception as msg:
            GPIO.cleanup()

    t.sleep(10)
