import DBaccess as db
import datetime
import json 

print ("These are the data")
hearth=db.executeSql("SELECT TIME,bpm FROM health_Heart limit 5")
for el in hearth:
	print("bpm: ",el)
