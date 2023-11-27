#!/usr/bin/env python

import csv
import gzip

detector_dict = {} 
with open('detector_stuttgart.csv') as f:
  reader = csv.reader(f)
  next(reader) 
  for row in reader:
    detector_dict[row[0]] = row[1]
    

# files to read and write
csv_file_name = "C:/Users/mavis/Desktop/visualizationUTD19.csv.gz" # the input data file
csv_file_name2 = "C:/Users/mavis/Desktop//detector_stuttgart.csv.gz" # the input data file
ttl_file_name =  "C:/Users/mavis/Desktop/utd19_stuttgart.ttl.gz" # the output data file

# prefixes
ontology_prefix = "http://example.org/ontology/" # for classes and properties
resources_prefix = "http://example.org/resource/" # for resources

csv_file = gzip.open(csv_file_name, mode="rt")
csv_file2 = gzip.open(csv_file_name2, mode="rt")
ttl_file = gzip.open(ttl_file_name, mode="wt")
csvobj = csv.reader(csv_file, delimiter = ',', quotechar="'")
csvobj2 = csv.reader(csv_file2, delimiter = ',', quotechar="'")

next(csvobj) # skip first row
next(csvobj2) # skip first row

# detector dict
detectorDict = {}
for raw in csvobj2:
    key = raw[1]
    id = key.find('.')
    if id != -1:
        key = key[:id]
    if key[0] == "0":
        key = key[1:]
    detectorDict[key] = {}
    detectorDict[key]["long"] = raw[4]
    detectorDict[key]["lat"] = raw[5]
    detectorDict[key]["fclass"] = raw[2]


# write prefixes
ttl_file.write("@prefix ex: <http://example.org/> .\n")




# write triples for each row
for row in csvobj:
    id_key = row[3]
    id = id_key.find('.')
    if id != -1:
        id_key = id_key[:id]
    if id_key[0] == "0":
        id_key = id_key[1:]


    ttl_file.write(f"record:rec_{row[0]} a ex:Record ;\n")
    ttl_file.write(f"  ex:date \"{row[1]}\"^^xsd:date ;\n")

    ttl_file.write(f"  ex:fclass fclass:{detectorDict[id_key]['fclass']} ;\n")
    #ttl_file.write("  ex:long long:%s ;\n" % detectorDict[id_key]["long"])
    #ttl_file.write("  ex:lat lat:%s ;\n" % detectorDict[id_key]["lat"])
    ttl_file.write(f"  ex:beginningTime {str(int(row[2]) - 300)} ;\n")
    ttl_file.write(f"  ex:endTime {row[2]} ;\n" )
    #ttl_file.write(f"  ex:location location:dect_{id_key} ;\n")
    ttl_file.write(f"  ex:flow {row[4]} ;\n")
    ttl_file.write(f"  ex:geo_info ex:{id_key} .\n")
    ttl_file.write(f"ex:{id_key} a ex:Detecter_Geo ;\n")
    ttl_file.write(f"  ex:long {detectorDict[id_key]['long']} ;\n")
    ttl_file.write(f"  ex:lat {detectorDict[id_key]['lat']} .\n")
    detector_id = detector_dict['detector_location_' + id_key]
    ttl_file.write(f"ex:detectorID_{detector_id} a ex:Detecter_Geo ;\n")
    ttl_file.write(f"  ex:long {detectorDict[id_key]['long']} ;\n")
    ttl_file.write(f"  ex:lat {detectorDict[id_key]['lat']} .\n")
    




ttl_file.close()
