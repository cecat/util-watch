#python server code that runs on Raspberry Pi to receive a simple comma delimited
#string via xbee radio
#
# interacts with Twine via a shell script to get data from a nearby NOAA station,
# then read the temperature from the resulting file
# 
import serial
import commands
import httplib, urllib
import subprocess
import sys
import datetime

#multiple channels to monitor using ThingSpeak
sump = 1
furnace = 2
water = 3
garage = 4

# xbee radio
myUSBserial = "/dev/ttyUSB0"
myBaud      = 9600

# thingspeak 
compositeKey = "XYG8HDK7ZAD0LRMZ"
sumpKey = "GKKKCXBI6GMVQ2T3"

# sump stats tracking
sumpPtr = 0
sumpDutyString = list('00000000')
for i in range(0,4):
	sumpDutyString.extend(sumpDutyString)
sumpWindow = len(sumpDutyString)
for i in range(0, sumpWindow):
	sumpDutyString[i] = 0;

#shell script to get outside temperature NOAA weather station
homenoaaScript = "/home/pi/python-sensors/homenoaa.sh"
homenoaaTemp = 0
lasthomeNoaa = 0
hnFileName = "/home/pi/python-sensors/outsideTemp.log"

## command line variables #######################################
verboseMode = False
if (len(sys.argv) > 1):		# do we have any arguments at all?
	sys.argv.pop(0) 	#remove the program name, don't need it
	if sys.argv.count("-v"):
		verboseMode = True
	
## Connect to onboard XBee radio ###############################
ser = serial.Serial(myUSBserial, myBaud)
ser.flushInput()

if (verboseMode):
	print "----->starting server at ", datetime.datetime.now()
else:
	print "started"

gotSump = gotHvac = gotWater = False
sumpSensor = garageSensor = waterSensor = hvacSensor = 0
sumpState = garageState = waterState = hvacState = 0
sumpRecent = sumpDuty = 0

## main loop ##################################################

while 1:

	sensorValue = state =  0

	try:
		xbeeOK = True
		xbeeData=ser.readline()
		if xbeeOK:
			try:
				tempString = xbeeData.rstrip()
				comma1 = tempString.find(',')
				channel = tempString[:comma1]
				comma2 = tempString.find(',',comma1+1)
				sensorValue = tempString[comma1+1 : comma2]
				comma3 = tempString.find(',',comma2+1)
				state = tempString[comma2+1 : comma3]
				recent = tempString[comma3+1 : ]
			except:
				print datetime.datetime.now()," ERROR:  collision (packat corrupted) or improper format."
				print "        Data received from Arduino: ", xbeeData
				xbeeOK = False

		if xbeeOK:
			if (verboseMode):
				print datetime.datetime.now(), "->", tempString
	
			try:
	# SUMP
				if int(channel) == sump:
					gotSump = True
					sumpSensor = sensorValue
					sumpState = state
					sumpRecent = recent
					if int(state) == 1:
						sumpDutyString[sumpPtr] = 1
					else:
						sumpDutyString[sumpPtr] = 0
					sumpPtr = (sumpPtr+1) % sumpWindow
					sumpDuty = 100 * float(sumpDutyString.count(1)) / float(sumpWindow)
	
	# HVAC
				if int(channel) == furnace:
					gotHvac = True
					hvacSensor = sensorValue
					hvacState = state
	
	# WATER heater
				if int(channel) == water:
					gotWater = True
					waterSensor = sensorValue
					waterState = state

	# GARAGE heater
				if int(channel) == garage:
					garageSensor = sensorValue
					garageState = state

			except:
				print datetime.datetime.now(), " ERROR: problem matching channel ->", tempString
	
	# if we have everyone...(don't wait for garage)
			if (gotSump and gotHvac and gotWater):
				gotSump = gotHvac = gotWater = False
				# get outside temp from NOAA
				noaaSuccess = True
				lasthomeNoaa = homenoaaTemp
				try:
					subprocess.call([homenoaaScript])
				except:
					logMsg = datetime.datetime.now() + "ERROR: failed shell script execute - " + homenoaaScript
					print logMsg
					noaaSuccess = False
				if (noaaSuccess):
					with open (hnFileName, "r") as f:
						first =f.readline()
						f.seek(-2, 2)
						while f.read(1) != "\n":
							f.seek(-2, 1)
						last = f.readline()
						tpoint1 = last.find('|')
						tpoint2 = last.find('F', tpoint1+1)
						homenoaaTemp = last[tpoint1+1 : tpoint2-1]
					try:
						outsideTemp = float(homenoaaTemp)
					except:
						logMsg = datetime.datetime.now(), " ERROR: failed to convert homenoaaTemp"
						print logMsg
						outsideTemp = 0
				else:
					outsideTemp = 0
				if (verboseMode):
					print datetime.datetime.now(), "outside temperature ->", outsideTemp

				params = urllib.urlencode({'field1': sumpSensor, 'field2': sumpState, 'field3' : hvacSensor, 'field4' : hvacState, 'field5' : waterSensor, 'field6' : waterState, 'field7' : outsideTemp, 'field8' : garageSensor, 'key':compositeKey})

	# report to ThingSpeak.com
				try:
					headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
						# 10/5/14 added timeout param
					conn = httplib.HTTPConnection("api.thingspeak.com:80", timeout=30)
					conn.request("POST", "/update", params, headers)
					response = conn.getresponse()
					if response.status != 200: 
						print response.status, response.reason
					data = response.read()
					conn.close()
				except:
					print datetime.datetime.now(), " ERROR:  Failed to post Composite data to ThingSpeak.com"
					print "        Data received from Arduino: ", xbeeData 


	# now update the sump channel....

				params = urllib.urlencode({'field1': sumpSensor, 'field2': sumpState, 'field3' : sumpRecent, 'field4' : sumpDuty, 'key': sumpKey})
	# report sump to ThingSpeak.com
				try:
					headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
						# 10/5/14 added timeout param
					conn = httplib.HTTPConnection("api.thingspeak.com:80", timeout=30)
					conn.request("POST", "/update", params, headers)
					response = conn.getresponse()
					if response.status != 200: 
						print response.status, response.reason
					data = response.read()
					conn.close()
				except:
					print datetime.datetime.now(), " ERROR:  Failed to post Sump data to ThingSpeak.com"
					print "        Data received from Arduino: ", xbeeData 


	except KeyboardInterrupt:
		print "   TERMINATED from keyboard"
		ser.close()
		break
