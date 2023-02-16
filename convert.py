
import decimal
import time
import urllib.request
import json
import csv
from csv import DictReader
from math import radians, cos, sin, asin, sqrt


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    r = 6371
    return c * r


headers = ["category", "gps_latitude", "gps_longitude", "street_latitude",
           "street_longitude", "display_name", "vehicle_speed", "vehicle_id"]

with open('data/traces_full.csv', 'r') as read_obj:
    # pass the file object to DictReader() to get the DictReader object
    dict_reader = DictReader(read_obj)
    # get a list of dictionaries from dct_reader
    list_of_traces = list(dict_reader)
    # print list of dict i.e. rows
    lat = None
    lon = None
    count = 0
    realCount = 0
    percentage = 0

    latLonAddress = {}
    addresses = []

    for traces in list_of_traces:
        realCount+=1
        percentage = round((realCount * 100) / len(list_of_traces)) 
        
        print("percentage: %d - data: %d of %d" % (percentage, realCount, len(list_of_traces)), end="\r")
        if decimal.Decimal(traces["speed"]) < 1:
            # print("skipping - gps vehicle speed is 0 Km/h")
            continue
        
        if (lat != None and lon != None):
            distance = haversine(float(lon), float(lat), float(
                traces['longitude']), float(traces['latitude']))
            if (distance < 0.01):
                lastKey = "%s-%s" % ("{:.4f}".format(decimal.Decimal(lat)),
                                        "{:.4f}".format(decimal.Decimal(lon)))

                copy = latLonAddress[lastKey]
                copy["vehicle_speed"]= traces["speed"]
                addresses.append(address)
                
                # print("same with last - index:%d" % (count))
                count += 1
                continue
                

        lat = traces["latitude"]
        lon = traces["longitude"]

        key = "%s-%s" % ("{:.4f}".format(decimal.Decimal(lat)),
                         "{:.4f}".format(decimal.Decimal(lon)))
        if key in latLonAddress:
            copy = latLonAddress[key]
            copy["vehicle_speed"]= traces["speed"]
            addresses.append(address)
            
            # print("data info - index:%d" % (count))
            count += 1
            continue

        # # create delay for anticipate from blocking on nominatim server
        # time.sleep(0.05)

        for x in range(0, 3):
            try:
                with urllib.request.urlopen("https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=%s&lon=%s&zoom=17" % (lat, lon)) as response:
                    data = json.loads(response.read().decode('utf8'))

                if data["category"] == "highway":
                    # print("data info - index: %d - display-name: %s" %
                    #       (count, data["display_name"]))
                    address = {
                        "category": data["category"],
                        "gps_latitude": lat,
                        "gps_longitude": lon,
                        "street_latitude": data["lat"],
                        "street_longitude": data["lon"],
                        "display_name": data["display_name"],
                        "vehicle_speed": traces["speed"],
                        "vehicle_id": traces["vehicle_id"]
                    }

                    # save to dictionary
                    latLonAddress[key] = address
                    addresses.append(address)
                else:
                    print("ini bukan jalan lat=%s , lon=%s" % (lat, lon))
                    lat = None
                    lon = None

                break
            except:
                continue

        count += 1
        # vehicle_ids.append(traces['id'])
    with open('data/address2.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(addresses)
