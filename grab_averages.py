import os, datetime, csv, pymysql, json

db = pymysql.connect('87.44.18.66', 'pi', 'pi');
cursor = db.cursor()
cursor.execute('use data;')

cursor.execute("SELECT * FROM reading WHERE place='EPA Callan Kilkenny';")
readings = []

for row in cursor:
    data = { 'Place': row[0], 'Day': row[1], 'Month': row[2], 'Year': row[3], 'Time': row[4], 'Smoke': row[5], 'Propane': row[6], 'LPG': row[7], 'CH4': row[8], 'CO2': row[9], 'Benzene': row[10], 'NH4': row[11], 'CO': row[12], 'NO2': row[13], 'CL2': row[14], 'Ozone': row[15], 'SO2': row[16], 'O2': row[17], 'Noise': row[18], 'Temp': row[19], 'Humidity': row[20], 'PM': row[21] }
    readings.append(data)

db.close()

averages = []

start_time = readings[0]['Time']

for i in range(len(readings)):
    if ':00:' in readings[i]['Time']:
        #print(readings[i]['Time'])
        #print('Index closest to hour is ' + str(i))
        readings = readings[i:]
        #print(readings[0]['Time'])
        break

data_file = open('average_data.csv', 'w+')

units = int(len(readings) / 30)
for i in range(units):
    no2_counter = 0
    o3_counter = 0
    time = ''
    for j in range(30):
        no2_counter += readings[(i*30) + j]['NO2']
        o3_counter += readings[(i*30) + j]['Ozone']
        if j == 29:
            time = readings[(i*30) + j]['Time']
    no2_counter /= 30
    o3_counter /= 30
    data = { 'Time': time, 'NO2': no2_counter, 'O3': o3_counter}
    data_file.write(time + "," + str(no2_counter) + "," + str(o3_counter)+"\n")
    averages.append(data)

data_file.close()

print(averages)


# 1 reading every 30 seconds. 2 per minute. 30 per 15 minutes.
