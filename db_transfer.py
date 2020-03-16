'''
Created on 19 January 2018
@author: Ryan McCloskey

Transfers data from the local SQLite database to the
remote MySQL database.
This is used in case of a lost internet connection during
device operation. Data is logged locally for this purpose,
and can be sent to the remote database using this file.
'''

import sqlite3, pymysql, os

global db

"""
Connects to an SQLite database and reads all data stored in the table.

@param      fileName    The name of the file containing the SQLite database.
@return     readings    The list of rows, in dictionary form, read from the DB.
"""
def read_from_sqlite_database(fileName):
    # Open a connection to the SQLite database
    conn = sqlite3.connect(fileName)
    # Fetch all rows from the database
    cur = conn.execute('SELECT * FROM reading;')
    # Initialises the list which will contain each row in the table as a separate dictionary.
    readings = []

    for row in cur:
        # Creates a dictionary to hold the data from each row in the table
        data = { 'Place': row[0], 'Day': row[1], 'Month': row[2], 'Year': row[3], 'Time': row[4], 'Smoke': row[5], 'Propane': row[6], 'LPG': row[7], 'CH4': row[8], 'CO2': row[9], 'Benzene': row[10], 'NH4': row[11], 'CO': row[12], 'NO2': row[13], 'CL2': row[14], 'Ozone': row[15], 'SO2': row[16], 'O2': row[17], 'Noise': row[18], 'Temp': row[19], 'Humidity': row[20], 'PM': row[21] }
        # Adds the data dictionary to the list of rows
        readings.append(data)

    # Close the connection to the database
    conn.close()
    # Return the list containing all row dictionaries
    return readings

"""
Connects to the SQLite database, and clears all data from the table.

@param      fileName    The name of the local SQLite database file.
"""
def clear_sqlite_database(fileName):
    try:
        # Open a connection to the SQLite database
        conn = sqlite3.connect(fileName)
        # Delete all rows from table
        cur = conn.execute('DELETE FROM reading;')
        # Commit changes
        conn.commit()
        # Close the database connection
        conn.close()
    except Exception as msg:
        print(msg)

"""
Creates a connection to the MySQL server, and selects the
specified database.

@param      host        The IP address or name of the MySQL server.
@param      username    The SQL user credential for connection.
@param      password    The SQL password credential.
@param      dbName      The name of the database to use.
"""
def connect_to_mysqlServer(host, username, password, dbName):
    try:
        global db
        # Initialise a connection to the MySQL server
        db = pymysql.connect(host, username, password, dbName)
        # Set the database connection cursor
        cursor = db.cursor()
        # Select the database to use
        cursor.execute('use ' + dbName + ';')
    except Exception as msg:
        print(msg)
    # Return the database connection cursor
    return cursor

"""
Sends data to the MySQL database by executing the stored procedure
on the database.

@param      cursor      The cursor to execute commands through the DB connection.
@param      data        The list of rows, in dictionary form, read from the SQLite database.
@return     success     A boolean indicating whether the operation has been successful.
"""
def send_to_database(cursor, data):
    # Used to indicate whether the operation was successful. Defaults to false.
    success = False
    try:
        global db
        for reading in data:
            # Reads the required data from the dictionary objec
            place, day, month, year, time, smoke, propane, lpg, ch4, co2, benzene, nh4, co, no2, cl2, ozone, so2, o2, noise, temp, rh, pm = reading['Place'], reading['Day'], reading['Month'], reading['Year'], reading['Time'], reading['Smoke'], reading['Propane'], reading['LPG'], reading['CH4'], reading['CO2'], reading['Benzene'], reading['NH4'], reading['CO'], reading['NO2'], reading['CL2'], reading['Ozone'], reading['SO2'], reading['O2'], reading['Noise'],  reading['Temp'], reading['Humidity'], reading['PM']

            cursor.callproc('addNewReading', [place, day, month, year, time, smoke, propane, lpg, ch4, co2, benzene, nh4, co, no2, cl2, ozone, so2, o2, noise, temp, rh, pm])

        # Commit all changes to the database
        db.commit()
        # Close the connection to the MySQL server
        db.close()
        # Indicate that the operation was successful
        success = True
    except Exception as msg:
        print(msg)
    finally:
        # Return the success status of the operation
        return success

# Open device_info file
device_infoFile = open('device_info.csv', 'r')
# Parse the data in the device_info file
info = device_infoFile.read().split(',')
# Read the server IP from parsed data. Data format is 'Device Name, Server IP, Port'
serverIp = str(info[1])
# Close the device_info file
device_infoFile.close()

# Read data from the SQLite database.
data = read_from_sqlite_database('eapms_db.sqlite')
# Open a connection to the remote MySQL database.
cursor = connect_to_mysqlServer(serverIp, 'pi', 'pi', 'data')
# Send all readings from the local database, to the remote MySQL DB.
success = send_to_database(cursor, data)
if success:
    print('Readings have been successfully transferred to the remote database.')
    # If data was successfully sent to MySQL server, clear the SQLite database.
    clear_sqlite_database('eapms_db.sqlite')
    print('Local SQLite database has been cleared.')
else:
    print('Unable to send readings to the remote database.')
