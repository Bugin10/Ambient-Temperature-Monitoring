import sqlite3
from w1thermsensor import W1ThermSensor
import json
import time
import datetime



sensors = []
i = 0
for sensor in W1ThermSensor.get_available_sensors():
	sensors.append(sensor)
	i = i+1

# the main sensor reading and plotting loop
while True:
   currtime = datetime.datetime.now()
   print(currtime)
   conn=sqlite3.connect('templog.db')
   curs=conn.cursor()
   temps = [0,0]
   for count in range(0,i):       
      	 # temperature in celsius
       	 temp_C = sensors[count].get_temperature()
      	 # convert celsius to fahrenheit
      	 temp_F = sensors[count].get_temperature(W1ThermSensor.DEGREES_F)
      	 # show only one decimal place for temperature
      	 temp_C = "%.1f" % temp_C
      	 # write the data to plotly
         temps[count] = temp_C
   print(temps[0])
   curs.execute("INSERT INTO temps values(datetime('now','localtime'), (?), (?))", ( temps[0], temps[1],))
   conn.commit() 
   time.sleep(300)

