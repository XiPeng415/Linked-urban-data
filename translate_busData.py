import time
import csv
import gzip
import re

"""
#data hierarchy
dict = {
        "de:vvs:10002_::45-T0-94":   # trip_id
        {
            "road" : rg.Curve, # store road curve geometry
            "road_id" : "10002_", # Text DIVA
            "1" : { # stop sequence
                "stop_id" : "de:08116:1905:1:1", #stop_id
                "stop_name" : "Stammheim",
                "stop_lon": 9.198,   # longtitude
                "stop_lat": 48.792,   # latitude
                "arrival_time" : "21:33:00", # arrival time
                "departure_time" : "21:33:00" # departuure time
                },
                
            "2" : { # stop sequence
                "stop_id" : "de:08116:2103:1:2", #stop_id
                "stop_name" : "Asdfasf",
                "stop_lon": 9.236,   # longtitude
                "stop_lat": 47.425,   # latitude
                "arrival_time" : "21:37:00", # arrival time
                "departure_time" : "21:38:00" # departuure time
                }
        },

        "de:vvs:10002_::45-T0-98":   # trip_id
        {
            "road" : rg.Curve, # store road curve geometry
            "road_id" : "10002_", # Text DIVA
            "1" : { # stop sequence
                "stop_id" : "de:08116:1905:1:1", #stop_id
                "stop_name" : "Stammheim",
                "lon": 9.198,   # longtitude
                "lat": 48.792,   # latitude
                "arrival_time" : "21:33:00", # arrival time
                "departure_time" : "21:33:00" # departuure time
                },
                
            "2" : { # stop sequence
                "stop_id" : "de:08116:2103:1:2", #stop_id
                "stop_name" : "Asdfasf",
                "lon": 9.236,   # longtitude
                "lat": 47.425,   # latitude
                "arrival_time" : "21:37:00", # arrival time
                "departure_time" : "21:38:00" # departuure time
                }
        }
    }
"""

# files to read and write

curveName_csvFile_name = r"C:\Users\User\Documents\GitHub\ShareFolder\vvsBusData\busData\curveName.csv.gz" # the input data file
x_csvFile_name = r"C:\Users\User\Documents\GitHub\ShareFolder\vvsBusData\busData\x.csv.gz"
y_csvFile_name = r"C:\Users\User\Documents\GitHub\ShareFolder\vvsBusData\busData\y.csv.gz"
z_csvFile_name = r"C:\Users\User\Documents\GitHub\ShareFolder\vvsBusData\busData\z.csv.gz"
stops_csvFile_name = r"C:\Users\User\Documents\GitHub\ShareFolder\vvsBusData\busData\stops.csv.gz" # the input data file
stopTime_csvFile_name = r"C:\Users\User\Documents\GitHub\ShareFolder\vvsBusData\busData\stopTime.csv.gz"

ttl_file_name = r"C:\Users\User\Documents\GitHub\ShareFolder\vvsBusData\busttl.ttl.gz" # the output data file


curveName_csvFile = gzip.open(curveName_csvFile_name, mode="rt", encoding="utf-8")
x_csvFile = gzip.open(x_csvFile_name, mode="rt", encoding="utf-8")
y_csvFile = gzip.open(y_csvFile_name, mode="rt", encoding="utf-8")
z_csvFile = gzip.open(z_csvFile_name, mode="rt", encoding="utf-8")
stops_csvFile = gzip.open(stops_csvFile_name, mode="rt", encoding="utf-8")
stopTime_csvFile = gzip.open(stopTime_csvFile_name, mode="rt", encoding="utf-8")

ttl_file = gzip.open(ttl_file_name, mode="wt", encoding="utf-8")


curveName_csvobj = csv.reader(curveName_csvFile, delimiter = ',', quotechar="'")
x_csvobj = csv.reader(x_csvFile, delimiter = ',', quotechar="'")
y_csvobj = csv.reader(y_csvFile, delimiter = ',', quotechar="'")
z_csvobj = csv.reader(z_csvFile, delimiter = ',', quotechar="'")
stops_csvobj = csv.reader(stops_csvFile, delimiter = ',', quotechar="'")
stopTime_csvobj = csv.reader(stopTime_csvFile, delimiter = ',', quotechar="'")

next(curveName_csvobj) # skip first row
next(x_csvobj) # skip first row
next(y_csvobj) # skip first row
next(z_csvobj) # skip first row
next(stops_csvobj) # skip first row
next(stopTime_csvobj) # skip first row

dict_shape = {}
dict_trip = {}
dict_stops = {}

# create dict for road_shape
for crvID,xList,yList,zList in zip(curveName_csvobj, x_csvobj, y_csvobj, z_csvobj):
    ID_key = crvID[0]
    if ID_key in dict_shape:
        pass
    else:
        dict_shape[ID_key] = {}
        dict_shape[ID_key]["xList"] = [x for x in xList if x != ""] # combine loop and conditional function
        dict_shape[ID_key]["yList"] = [y for y in yList if y != ""]
        dict_shape[ID_key]["zList"] = [z for z in zList if z != ""]


for st in stops_csvobj:
    #print(st)
    key_stopID = st[0]
    dict_stops[key_stopID] = {}
    dict_stops[key_stopID]["stop_name"] = st[1]
    dict_stops[key_stopID]["stop_lat"] = st[2]
    dict_stops[key_stopID]["stop_lon"] = st[3]


for stTime in stopTime_csvobj:
    # store trip_id
    key_trip = stTime[0] 

    if key_trip in dict_trip:
        pass
    else:
        dict_trip[key_trip] = {}
    
    # store road_id
    tripIdList = key_trip.split(":")
    dict_trip[key_trip]["road_id"] = tripIdList[2]
    
    # store stop order
    stopSeq = int(stTime[4])
    dict_trip[key_trip][stopSeq] = {}
    
    # store stop_id
    stopID = stTime[3]
    dict_trip[key_trip][stopSeq]["stop_id"] = stopID
    
    # store arrival_time
    arrivalTime = stTime[1]
    #arrivalTime = sum(x * int(t) for x, t in zip([3600, 60, 1], arrivalTime.split(":")))
    dict_trip[key_trip][stopSeq]["arrival_time"] = arrivalTime
    
    # store departure_time
    depatureTime = stTime[2]
    #depatureTime = sum(x * int(t) for x, t in zip([3600, 60, 1], depatureTime.split(":")))
    dict_trip[key_trip][stopSeq]["departure_time"] = depatureTime
    
    # store longtitude and latitude
    lon = dict_stops[stopID]["stop_lon"]
    lat = dict_stops[stopID]["stop_lat"]
    dict_trip[key_trip][stopSeq]["stop_lon"] = lon
    dict_trip[key_trip][stopSeq]["stop_lat"] = lat
    
    # store name
    name = dict_stops[stopID]["stop_name"]
    dict_trip[key_trip][stopSeq]["stop_name"] = name
    
    # store shape
    try:
        x = dict_shape[tripIdList[2]]["xList"]
        y = dict_shape[tripIdList[2]]["yList"]
        z = dict_shape[tripIdList[2]]["zList"]
        dict_trip[key_trip]["road"]={}
        dict_trip[key_trip]["road"]["x"] = x
        dict_trip[key_trip]["road"]["y"] = y
        dict_trip[key_trip]["road"]["z"] = z
    except:
        pass


ttl_file.write("@prefix ex: <http://example.org/> .\n")

############################################################################################
for stop in dict_stops:
    try:
        lon = float(dict_stops[stop]['stop_lon'])
        lat = float(dict_stops[stop]['stop_lat'])
    except:
        lon = 0.00
        lat = 0.00
    
    name = dict_stops[stop]['stop_name']
    name = re.sub(r'[^a-zA-ZäöüÄÖÜß]', '', name)

    ttl_file.write(f"ex:stopID_{stop} a ex:Stop ;\n")
    ttl_file.write(f"  ex:name \"{name}\" ;\n")
    ttl_file.write(f"  ex:geo_info ex:stop_location_{stop} .\n")
    ttl_file.write(f"ex:stop_location_{stop} a ex:Stop_Geo ;\n")
    ttl_file.write(f"  ex:long {lon} ;\n")
    ttl_file.write(f"  ex:lat {lat} .\n")

##############################################################################################
for route in dict_shape:
        xList = dict_shape[route]["xList"]
        yList = dict_shape[route]["yList"]
        ttl_file.write(f"ex:routeID_{route} a ex:Route ;\n")
        ttl_file.write(f"ex:routeID '{route}' ;\n")
        for j in range(len(xList)):
            if j != (len(xList)-1):
                ttl_file.write(f"ex:{route}_pts ex:{route}_route_pts_{j} ;\n") # build node pts_id
            else:
                ttl_file.write(f"ex:{route}_pts ex:{route}_route_pts_{j} .\n")

        for id, (x_num, y_num) in enumerate(zip(xList, yList)):
            ttl_file.write(f"ex:{route}_route_pts_{id} a ex:Route_Geo_pts ;\n")
            ttl_file.write(f"ex:x {x_num} ;\n")
            ttl_file.write(f"ex:y {y_num} .\n")


f = 0
for key in dict_trip:
    f += 1 
    # 60593 is the total amount of key in dict_trip
    if f<60593:
        ttl_file.write(f"ex:{key} a ex:Trip ;\n")
        #ttl_file.write(f"ex:road_id '{dict_trip[key]['road_id']}' ;\n") # Add road_id into attribute
        ttl_file.write(f"ex:geo_info ex:routeID_{dict_trip[key]['road_id']}; \n")
        #ttl_file.write(f"ex:geo_info ex:road_location_{key} .\n")  ####################################
        
        ttl_file.write(f"ex:station ex:station_{key} .\n") # Add new node called station_key


        ttl_file.write(f"ex:station_{key} a ex:stationSeq ;\n") # declare station_key as stationSeq class

        for i in range(len(dict_trip[key])-2):
            id = i + 1
            if i + 3 == len(dict_trip[key]):
                ttl_file.write(f"ex:stopSeq ex:{key}_{id} .\n") # Add new node called key_id
            else:
                ttl_file.write(f"ex:stopSeq ex:{key}_{id} ;\n") # Add new node called key_id


        # Run stop sequent from 1 to end
        for i in range(len(dict_trip[key])-2):
            id = i + 1
            if id in dict_trip[key].keys():
                ttl_file.write(f"ex:{key}_{id} a ex:selfStops ; \n")
                stop_id = dict_trip[key][id]['stop_id']
                name = dict_trip[key][id]["stop_name"]
                lon = dict_trip[key][id]["stop_lon"]
                lat = dict_trip[key][id]["stop_lat"]
                arrvTime = dict_trip[key][id]["arrival_time"]
                depTime = dict_trip[key][id]["departure_time"]
                ttl_file.write(f"ex:name \"{name.encode('unicode_escape').decode()}\" ; \n ")
                ttl_file.write(f"ex:long {lon} ; \n ")
                ttl_file.write(f"ex:lat {lat} ; \n ")
                ttl_file.write(f"ex:arrvTime '{arrvTime}' ; \n ")
                ttl_file.write(f"ex:depTime '{depTime}' ; \n ")
                ttl_file.write(f"ex:stop ex:stopID_{stop_id} .\n")


            else:
                # The condition here is due to lack of no.8 station that the absent data in source data
                print(" ")
                #print("key: ", key)
                #print("id: ", id)
                #print("No_", dict_trip[key].keys())

                
print("ok")
print(len(dict_trip))
    





