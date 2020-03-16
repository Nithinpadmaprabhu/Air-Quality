'''
Created on 31 Jul 2017

@author: Yahya Almardeny

This class represents the MQx sensor

'''

import time,os,csv, json
from enhanced_linearity import *
from datetime import datetime

class MQ():

    def __init__(self, name, mcp,channel, load_resistance, ratio, gases_points):
        self.name = name                                        # the name of the MQ sensor
        self.adc = mcp                                          # get the MCP3008 Object
        self.channel = channel                                  # the channel in which ADC will read from
        self.load_resistance = load_resistance                  # RL (adjustable: sensitivity v.s accuracy) [the recommended value can be found in datasheet]
        self.all_gases = local_linearities(gases_points, ratio) # dictionary of all gases in which every gas name is a key for a list of lists [[x0,y0,slope],..]
                                                                # every list at every index represents the local linearity between it and the next point
                                                                # the first point for every gas shall be the ratio Rs/R0 in clean air and the corrosponding x
        self.R0 = 0                                             # R0 will be fetched from the csv file but if this is the first time, it will be calculated
        self.ratio = ratio                                      # ratio = Rs/R0 from the datasheet
        self.__calibrate()                                      # start initial calibration in clean air and save the value to a csv file if it's the first run
                                                                # if it's not, just retrieve R0 from the csv file


    def __repr__(self):
        return self.name   # to have a textual rep of this class

    ######################### Rs Calculation ###############################
    # Input:   adc_reading
    # Output:  Rs
    # Remarks: full approach of how I derived this equation can be found at:
    # electronics.stackexchange.com/a/320809/158166
    ########################################################################
    def __get_Rs(self, adc_reading):
        return float(self.load_resistance*(1024-adc_reading)/float(adc_reading))


    #################### First Time Running Check ##########################
    # Returns True if this is the first run of this MQ sensor
    # whether there is a data.csv file exist or not
    ########################################################################
    def __first_time(self):
        if not os.path.isfile("/home/pi/Desktop/EAPMS/data.csv"):
            csvFile = open("/home/pi/Desktop/EAPMS/data.csv", 'w+')
            writer = csv.DictWriter(csvFile, fieldnames= ['MQ_name', 'R0'])
            writer.writeheader()
            return True
        else:
            with open('/home/pi/Desktop/EAPMS/data.csv') as csvFile:
                reader = csv.DictReader(csvFile)
                for row in reader:
                    if(row['MQ_name']==self.name):
                        return False
                return True

    #===========================================================================
    # Performs unit calibration if it has not already been completed.
    # Finds the correct value of R0, after calculating RS in clear air.
    # The R0 value is then saved to a CSV file.
    #===========================================================================
    def __calibrate(self):
        if self.__first_time():
            print("Calibrating " + self.name + "...")

            if not os.path.isfile("/home/pi/Desktop/EAPMS/calibration_log.txt"):
                logfile = open("/home/pi/Desktop/EAPMS/calibration_log.txt", 'w+')
            else:
                logfile = open("/home/pi/Desktop/EAPMS/calibration_log.txt", 'a')

            date_time = datetime.now()

            log = str(self.name) + " - " + str(date_time) + "\n"
            logfile.write(log)

            Rs_freshAir = 0
            for i in range(10):
                reading = self.adc.read(self.channel)
                rs = self.__get_Rs(reading)
                Rs_freshAir += rs
                log = "ADC: " + str(reading) + ", RS: " + str(rs) + "\n"
                logfile.write(log)
                time.sleep(0.5)
            Rs_freshAir /= 10
            R0 = Rs_freshAir / self.ratio
            csvFile = open("/home/pi/Desktop/EAPMS/data.csv", 'a')
            writer = csv.DictWriter(csvFile, fieldnames= ['MQ_name', 'R0'])
            writer.writerow({'MQ_name': self.name, 'R0': R0})
            self.R0 = R0
            print("Calibration completed...\n")

            log = "-------------------------------------------------\n"
            logfile.write(log)
            logfile.close()
        else:
            with open('/home/pi/Desktop/EAPMS/data.csv') as csvFile:
                reader = csv.DictReader(csvFile)
                for row in reader:
                    if(row['MQ_name']==self.name):
                        self.R0 = float(row['R0'])

    ######################### Initial Calibration #########################
    # Find the correct value of R0, after calculating Rs in clear air
    # save the value in a csv file
    #######################################################################
    """def __calibrate(self):
        if self.__first_time():
            #print("Calibrating " + self.name+ "...")
            Rs_freshAir = 0
            for i in range(10):
                Rs_freshAir += self.__get_Rs(self.adc.read(self.channel))
                time.sleep(0.5)
            Rs_freshAir /= 10
            R0 = Rs_freshAir / self.ratio
            csvFile = open("/home/pi/Desktop/EAPMS/data.csv", 'a')
            writer = csv.DictWriter(csvFile, fieldnames= ['MQ_name', 'R0'])
            writer.writerow({'MQ_name': self.name, 'R0': R0})
            self.R0 = R0
            #print("Calibration is done...\n")
            #print("Ro=%f kohm" % self.R0)
        else:
            with open('/home/pi/Desktop/EAPMS/data.csv') as csvFile:
                reader = csv.DictReader(csvFile)
                for row in reader:
                    if(row['MQ_name']==self.name):
                        self.R0 = float(row['R0'])
    """


    #########################  Reading Gas ################################
    # This function returns a JSON of gases and their concentrations in PPM
    #######################################################################
    def read(self):
        val = {}
        for gas in self.all_gases.keys():
            # x = 10 ^ {[log(y) - b] / m} in which y = Rs/R0 (the ratio)
            # but b = log(y0) - m*log(x0) (to avoid finding y-intercept)
            # --> x = 10 ^ {[(log(y) - log(y0)) / m] + log(x0)}
            y = self.__get_Rs(self.adc.read(self.channel))/self.R0
            local_linearity = local_line(gas, self.all_gases, y)
            if local_linearity != None:
                # at index 0 there's a point(x0,y0), at index 1 there's the derivative (local slope)
                x0, y0, m = local_linearity[0].get_x(), local_linearity[0].get_y(), local_linearity[1]
                gas_concentration = pow(10, ((log10(y)-log10(y0))/m) + log10(x0))
                #val[gas] = gas_concentration
                val[gas] = str(round(gas_concentration, 5))
            else:
                val[gas] =  "{}:{},".format(gas, -1)

        return json.dumps(val)

	###################  Reading Gas in Part Per Billion ##################
    # This function returns a JSON of gases and their concentrations in PPB
    #######################################################################
    def readPPB(self):
        val = {}
        for gas in self.all_gases.keys():
            # x = 10 ^ {[log(y) - b] / m} in which y = Rs/R0 (the ratio)
            # but b = log(y0) - m*log(x0) (to avoid finding y-intercept)
            # --> x = 10 ^ {[(log(y) - log(y0)) / m] + log(x0)}
            y = self.__get_Rs(self.adc.read(self.channel))/self.R0
            local_linearity = local_line(gas, self.all_gases, y)
            if local_linearity != None:
                # at index 0 there's a point(x0,y0), at index 1 there's the derivative (local slope)
                x0, y0, m = local_linearity[0].get_x(), local_linearity[0].get_y(), local_linearity[1]
                gas_concentration = pow(10, ((log10(y)-log10(y0))/m) + log10(x0))
                #val[gas] = gas_concentration
                val[gas] = str(round(gas_concentration/1000, 5))
            else:
                val[gas] =  "{}:{},".format(gas, -1)

        return json.dumps(val)
