import DBaccess as db
import datetime
import json 
import re

print ("Reading file..")
with open('HONOR Health-Data User\'s health information.json', 'r') as file:
	content = file.read()

print ("Parsing json..")
matches = re.findall(r'\[.*?\]', content)
#data = json.loads(content)
data = []
for match in matches:
    data.extend(json.loads(match))

print("Inserting more or less ",len(data), "elements...")
bufferSize=20000
i=0
n_points=0
baseQuery="INSERT INTO `health_rawData` (`type`, `unit`, `startTime`, `start`, `endTime`, `end`, `value`, `key`) VALUES "
dataQuery=""
for el in data:
	v_type=el['dataType']
	if v_type not in ['heart_rate']:
		continue
	i += 1
	startTime=el['startTime']
	start=startTime
	endTime=el['endTime']
	end=endTime
	point=el['samplePoint']
	v_value=point['dynamicHeartRate']
	#print("LOG: ",v_type," ",unit," ",startTime," ",start,"",endTime," ",end,"",v_value," ",v_key)
	dataQuery+="('1989', '1989', '"+str(startTime)+"', '"+str(start)+"', '"+str(endTime)+"', '"+str(end)+"', '"+str(v_value)+"', '"+str(v_type)+"'), "
	# facciamo l'insert ogni tot elementi
	if i%bufferSize==0:
		query=baseQuery+dataQuery[:-2]	
		#print(query);
		db.executeSql(query)
		dataQuery=""
# Perform the last insert
query=baseQuery+dataQuery[:-2]	
#print(query);
db.executeSql(query)

print("C'erano ",i," elementi.")