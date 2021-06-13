import DBaccess as db
from datetime import datetime, timedelta
import json 

startPeriod="2020-05-26"
endPeriod="2021-05-26"

hearthData=db.executeSql("SELECT time,bpm FROM health_Heart WHERE time BETWEEN '"+startPeriod+"' and '"+endPeriod+"' order by time")
sleepData=db.executeSql("SELECT start,end,type,durationMinutes FROM health_Sleep WHERE start BETWEEN '"+startPeriod+"' and '"+endPeriod+"' order by start")
#SHALLOW DREAM WAKE DEEP NOON (NOON è pisolino. Tutto il resto è sonnno. La veglia c'è quando il periodo non è compreso fra start e end. O quando c'è WAKE.)


hmin=min(hearthData, key = lambda t: t[1])[1]
hmax=max(hearthData, key = lambda t: t[1])[1]
#TODO scegli i gradienti in base a hmin e hmax

curDate=datetime.strptime(startPeriod, '%Y-%m-%d')
endDate=datetime.strptime(endPeriod, '%Y-%m-%d')
bpmLast=hearthData[0][1]
sleepLast=sleepData[0][1]
hIndex=0
sIndex=0
while curDate < endDate:
	print("DEBUG: ",curDate)
	curDate= curDate + timedelta(minutes = 5)

#for el in hearthData:
#	print("bpm: ",el[1])
