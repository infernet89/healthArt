import DBaccess as db
from datetime import datetime, timedelta
import json 
import numpy
from PIL import Image

startPeriod="2020-05-26"
endPeriod="2021-05-26"

hearthData=db.executeSql("SELECT time,bpm FROM health_Heart WHERE time BETWEEN '"+startPeriod+"' and '"+endPeriod+"' order by time")
sleepData=db.executeSql("SELECT start,end,type,durationMinutes FROM health_Sleep WHERE start BETWEEN '"+startPeriod+"' and '"+endPeriod+"' and durationMinutes between 1 and 400 order by start,end")
#WAKE NOON SHALLOW DREAM DEEP (NOON è pisolino. Tutto il resto è sonnno. La veglia c'è quando il periodo non è compreso fra start e end. O quando c'è WAKE.)


hmin=min(hearthData, key = lambda t: t[1])[1]
hmax=max(hearthData, key = lambda t: t[1])[1]
print("Heart is between ",hmin," and", hmax)
#TODO scegli i gradienti in base a hmin e hmax
pixel = numpy.zeros( (365,288,3), dtype=numpy.uint8 )
x=0
y=0

curDate=datetime.strptime(startPeriod, '%Y-%m-%d')
endDate=datetime.strptime(endPeriod, '%Y-%m-%d')
bpmLast=hearthData[0][1]
sleepLast=sleepData[0][1]
hIndex=0
sIndex=0
isSleeping=0
BPM=0
energy=1
while curDate < endDate:
	# for each sample, you can be:
	# sleeping OR awake (0 - awake, 1 - that value, * - last found values)
	while sleepData[sIndex][1] <= curDate:
		sIndex+=1
		isSleeping=0
		if sleepData[sIndex][0] <= curDate <= sleepData[sIndex][1]:
			sleepLast=sleepData[sIndex][2]
			if sleepLast!='WAKE':
				isSleeping=1
			else:
				isSleeping=0
	# bpm (0 - last value, 1- that value, * - average from found values)
	nSample=0
	sumBpmSample=0
	while hearthData[hIndex][0]<= curDate:
		nSample+=1
		sumBpmSample+=hearthData[hIndex][1]
		bpmLast=hearthData[hIndex][1]
		hIndex+=1
	if nSample>0:
		BPM=round(sumBpmSample/nSample)
	else:
		BPM=bpmLast
	#l'energia viene ricaricata dormendo, e consumata da sveglio
	if isSleeping:
		energy+=(1/96) # in 8 ore, la somma deve fare 1
	else:
		energy-=(1/192) # in 16 ore, la somma deve fare 1
	#evitiamo overflow e underflow
	if energy> 1.2:
		energy=1.2
	if energy<0.1:
		energy=0.1
	print("curDate: ",curDate,"isSleeping: ",isSleeping,"BPM: ",BPM,"energy",energy,"x",x,"y",y)
	#fill the pixels of the image
	if isSleeping:
		pixel[y][x]=[0,0,0]
	else:
		#pixel[y][x]=[255,255,255]
		pixel[y][x]=[round(255*energy),round(255*energy),round(255*energy)]
	x+=1
	if x>=288:
		x=0
		y+=1
	curDate= curDate + timedelta(minutes = 5)
#save the result
img = Image.fromarray(pixel)
img.show()                      # View in default viewer
img.save('test.png')
#for el in hearthData:
#	print("bpm: ",el[1])


# Create a 1024x1024x3 array of 8 bit unsigned integers
#data = numpy.zeros( (1024,1024,3), dtype=numpy.uint8 )

#data[512,512] = [254,0,0]       # Makes the middle pixel red
#data[512,513] = [0,0,255]       # Makes the next pixel blue

#img = Image.fromarray(data)       # Create a PIL image
#img.show()                      # View in default viewer
#img.save('test.png')