import DBaccess as db
from datetime import datetime, timedelta
import json 
import numpy
import math
import statistics
from PIL import Image
from colour import Color

startPeriod="2020-05-26"#"2020-05-15"
endPeriod="2021-05-26"#"2021-06-07"
sampleMinutes=5
samplePercentile=99

curDate=datetime.strptime(startPeriod, '%Y-%m-%d')
endDate=datetime.strptime(endPeriod, '%Y-%m-%d')
daysComputed=abs((curDate - endDate).days)
dailySamples=math.ceil(24*60/sampleMinutes)

hearthData=db.executeSql("SELECT time,bpm FROM health_Heart WHERE time BETWEEN '"+startPeriod+"' and '"+endPeriod+"' order by time")
sleepData=db.executeSql("SELECT start,end,type,durationMinutes FROM health_Sleep WHERE start BETWEEN '"+startPeriod+"' and '"+endPeriod+"' and durationMinutes between 1 and 400 order by start,end")
#WAKE NOON SHALLOW DREAM DEEP (NOON è pisolino. Tutto il resto è sonnno. La veglia c'è quando il periodo non è compreso fra start e end. O quando c'è WAKE.)

hmin=min(hearthData, key = lambda t: t[1])[1]
hmax=max(hearthData, key = lambda t: t[1])[1]
phmax=round(numpy.percentile([row[1] for row in hearthData],samplePercentile))
phmin=-round(numpy.percentile([-row[1] for row in hearthData],samplePercentile))
#variance=statistics.variance([row[1] for row in hearthData])
print("Heart is between ",hmin," and", hmax,". With percentile (",phmin,",",phmax,") Days computed ",daysComputed," with a sample size of ",sampleMinutes)
#scegli i gradienti in base a hmin e hmax (diverso sveglia/sonno)
sleepGradient = list(Color("#00eaff").range_to(Color("#3800ff"),phmax-phmin))
awakeLowGradient = list(Color("#00FF00").range_to(Color("#00DD00"),1+phmin-hmin))
awakeMidGradient = list(Color("#00DD00").range_to(Color("#DD0000"),phmax-phmin))
awakeHighGradient = list(Color("#FF0000").range_to(Color("#DD0000"),1+hmax-phmax))
i=hmin
sleepColors=[0,0,0] * (hmax+1)
awakeColors=[0,0,0] * (hmax+1)
while i <= hmax:
	if i < phmin:
		sleepColors.insert(i,[round(el * 255) for el in sleepGradient[0].rgb])
		awakeColors.insert(i,[round(el * 255) for el in awakeLowGradient[i-hmin].rgb])
	elif i>= phmax:
		sleepColors.insert(i,[round(el * 255) for el in sleepGradient[phmax-phmin-1].rgb])
		awakeColors.insert(i,[round(el * 255) for el in awakeHighGradient[i-phmax].rgb])
	else:
		sleepColors.insert(i,[round(el * 255) for el in sleepGradient[i-phmin].rgb])
		awakeColors.insert(i,[round(el * 255) for el in awakeMidGradient[i-phmin].rgb])
	i=i+1
pixel = numpy.zeros( (daysComputed,dailySamples,3), dtype=numpy.uint8 )
x=0
y=0

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
	while sIndex<len(sleepData)-1 and sleepData[sIndex][1] <= curDate:
		sIndex+=1
		#print("	",sleepData[sIndex])
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
	while hIndex<len(hearthData) and hearthData[hIndex][0]<= curDate:
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
		energy+=(1/(8*60/sampleMinutes)) # in 8 ore, la somma deve fare 1
	else:
		energy-=(1/(16*60/sampleMinutes)) # in 16 ore, la somma deve fare 1
	#evitiamo overflow e underflow
	if energy> 1.4:
		energy=1.4
	if energy<0.2:
		energy=0.2
	print("curDate: ",curDate,"isSleeping: ",isSleeping,"BPM: ",BPM,"energy",energy,"x",x,"y",y)
	#fill the pixels of the image
	if isSleeping:
		pixel[y][x]=[min(255,round(el * energy)) for el in sleepColors[BPM]]
	else:
		pixel[y][x]=[min(255,round(el * energy)) for el in awakeColors[BPM]]
	x+=1
	if x>=dailySamples:
		x=0
		y+=1
	curDate= curDate + timedelta(minutes = sampleMinutes)
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