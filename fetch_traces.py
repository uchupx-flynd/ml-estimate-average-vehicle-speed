from dotenv import dotenv_values
import mysql.connector
import csv
import pandas as pd
from csv import DictReader
from mysql.connector import Error


config = dotenv_values(".env")
field_names = ['id', 'vehicle_id', 'driver_id', 'trip_id', 'trip_leg_id', 'device_id', 'latitude',
               'longitude', 'timestamp', 'speed', 'travelled_distance', 'bearing', 'battery', 'signal']
traces = None
vehicle_ids = []



# open file in read mode
with open('data/vehicles.csv', 'r') as read_obj:
    # pass the file object to DictReader() to get the DictReader object
    dict_reader = DictReader(read_obj)
    # get a list of dictionaries from dct_reader
    list_of_vehicles = list(dict_reader)
    # print list of dict i.e. rows
    for vehicle in list_of_vehicles:
      vehicle_ids.append(vehicle['id'])

try:
    connection = mysql.connector.connect(
        host=config['HOST'],
        port=config['PORT'],
        database=config['DATABASE_GPS'],
        user=config['USERNAME'],
        password=config['PASSWORD'],
    )

    if connection.is_connected():
        vehicle_ids_string = ",".join(vehicle_ids)

        sql_select_Query = "SELECT * FROM traces WHERE vehicle_id IN (vehicles_ids) AND trip_id IS NOT NULL LIMIT 100000"
        sql_select_Query = sql_select_Query.replace('vehicles_ids', vehicle_ids_string)
        print(sql_select_Query)
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql_select_Query)
        # get all records
        traces = cursor.fetchall()
        print("Total number of rows in table: ", cursor.rowcount)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

with open('data/traces.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(traces)
print(config['DATABASE'])
