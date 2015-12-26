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
#see Arduino code - these are defined there
sump = 1
furnace = 2
water = 3
garage = 4


## STUFF YOU NEED TO CONFIGURE LOCALLY #######################################
# here I'm specifying local path (./) but
# you will want to substitute for hard-coded filenames and fully specified
# paths because I start the script from crontab at boottime

# xbee radio
myUSBserial = "/dev/ttyUSB0"
myBaud      = 9600

# read thingspeak channel from KEY.txt file
keyfile = "./KEY.txt"
with open (keyfile, "r") as f:
	ThingSpeakKey = f.readline().rstrip()
											# ignore comments and empty lines
	hashmark = "#"
	while (hashmark == "#"):
		if len(ThingSpeakKey) == 0:
			ThingSpeakKey = "#"
		hashmark = ThingSpeakKey[0]
		if hashmark == "#":
			ThingSpeakKey = f.readline().rstrip()
	print "sending to ThingSpeak with API ->", ThingSpeakKey

#shell script to get outside temperature NOAA weather station
#again use full pathnames if running from crontab
noaaScript = "./noaa-query.sh"
noaaTemp = 0
lastNoaa = 0
hnFileName = "./outsideTemp.log"

## END STUFF YOU NEED TO CONFIGURE LOCALLY #######################################

# sump stats tracking
sumpPtr = 0
sumpDutyString = list('00000000')
for i in range(0,4):
	sumpDutyString.extend(sumpDutyString)
sumpWindow = len(sumpDutyString)
for i in range(0, sumpWindow):
	sumpDutyString[i] = 0;


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
				lastNoaa = noaaTemp
				try:
					subprocess.call([noaaScript])
				except:
					logMsg = datetime.datetime.now() + "ERROR: failed shell script execute - " + noaaScript
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
						noaaTemp = last[tpoint1+1 : tpoint2-1]
					try:
						outsideTemp = float(noaaTemp)
					except:
						logMsg = datetime.datetime.now(), " ERROR: failed to convert noaaTemp"
						print logMsg
						outsideTemp = 0
				else:
					outsideTemp = 0
				if (verboseMode):
					print datetime.datetime.now(), "outside temperature ->", outsideTemp

# note that the channels in ThingSpeak have individual charts, corresponsing to "field1" through "fieldn" in the call below

				params = urllib.urlencode({'field1': sumpSensor, 'field2': sumpState, 'field3' : hvacSensor, 'field4' : hvacState, 'field5' : waterSensor, 'field6' : waterState, 'field7' : outsideTemp,  'key':ThingSpeakKey})

	# report to ThingSpeak.com
				try:
					headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
						# 10/5/14 added timeout param
					conn = httplib.HTTPConnection("api.thingspeak.com:80", timeout=30)
					conn.request("POST", "/update", params, headers)
					response = conn.getresponse()
					if response.status != 200: 
						print "ThingSpeak !200 response ->", response.status, response.reason
					data = response.read()
					conn.close()
				except:
					print datetime.datetime.now(), " ERROR:  Failed to post to ThingSpeak.com"
					print "        Data received from Arduino: ", xbeeData 


	except KeyboardInterrupt:
		print "   TERMINATED from keyboard"
		ser.close()
		break
