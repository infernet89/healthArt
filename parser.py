import DBaccess as db
import datetime
import json 

print ("Reading file..")
with open('health_detail_data.json', 'r') as file:
	content = file.read()
#content = Path('health_detail_data.json').read_text()
# print ("File content: ",content)

print ("Parsing json..")
data = json.loads(content)

print("Inserting more or less ",len(data), "elements...")
bufferSize=20000
i=0
n_points=0
baseQuery="INSERT INTO `health_rawData` (`type`, `unit`, `startTime`, `start`, `endTime`, `end`, `value`, `key`) VALUES "
dataQuery=""
for el in data:
	i += 1
	v_type=el['type']
	points=el['samplePoints']
	for subel in points:
		unit=subel['unit']
		startTime=subel['startTime']
		start=datetime.datetime.fromtimestamp(startTime/1000).strftime('%Y-%m-%d %H:%M:%S')
		endTime=subel['endTime']
		end=datetime.datetime.fromtimestamp(endTime/1000).strftime('%Y-%m-%d %H:%M:%S')
		v_value=subel['value']
		v_key=subel['key']
		#print("LOG: ",v_type," ",unit," ",startTime," ",start,"",endTime," ",end,"",v_value," ",v_key)
		dataQuery+="('"+str(v_type)+"', '"+str(unit)+"', '"+str(startTime)+"', '"+str(start)+"', '"+str(endTime)+"', '"+str(end)+"', '"+str(v_value)+"', '"+str(v_key)+"'), "
	# facciamo l'insert ogni tot elementi
	if i%bufferSize==0 or i==len(data):
		query=baseQuery+dataQuery[:-2]	
		# print(query);
		db.executeSql(query)
		dataQuery=""
	# executeSql("INSERT INTO `temperatura` (temperature,normalized_timestamp) VALUES ('"+str(temperature)+"',DATE_ADD(CURRENT_TIMESTAMP, interval -SECOND(CURRENT_TIMESTAMP) SECOND))")

print("C'erano ",i," elementi.")