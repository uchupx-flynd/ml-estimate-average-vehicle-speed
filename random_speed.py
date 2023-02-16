import csv
import random
from csv import DictReader

headers = ["category", "gps_latitude", "gps_longitude", "street_latitude",
           "street_longitude", "display_name", "vehicle_speed", "vehicle_id"]

updated_address = []

with open('data/address2.csv', 'r') as read_obj:
    # pass the file object to DictReader() to get the DictReader object
    dict_reader = DictReader(read_obj)
    # get a list of dictionaries from dct_reader
    list_of_address = list(dict_reader)
    
    for address in list_of_address:
      address['vehicle_speed'] =  random.randint(0,30)
      
      updated_address.append(address)
    
    with open('data/address3.csv', 'w') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=headers)
      writer.writeheader()
      writer.writerows(updated_address)
    
    
    