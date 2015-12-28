#
# utility watch for Raspberry Pi (uW-RPI)
# CeC (cecatlett@gmail.com)
#
# python server code that runs on Raspberry Pi to receive a simple comma delimited
# string via xbee radio
#
# uses a shell script (noaa-query.sh) to get data from a nearby NOAA station,
# then reads the (F) temperature from the resulting file and logs to a logfile
# 

## import libraries
import serial
import commands
import httplib, urllib
import subprocess
import sys
import datetime

# import my library
import uwlib


## STUFF YOU NEED TO CONFIGURE LOCALLY #######################################
# here I'm specifying local path (./) but
# you will want to substitute for hard-coded filenames and fully specified
# paths because I start the script from crontab at boottime

# xbee radio (plugged into UBS using an Xbee Explorer breakout board
myUSBserial = "/dev/ttyUSB0"
myBaud      = 9600

# read thingspeak channel from KEY.txt file
keyfile = "./KEY.txt"

#shell script to get outside temperature NOAA weather station
#again use full pathnames if running from crontab
# noaaScript = "./noaa-query.sh"
noaaScript = "./NOAACheck.sh"
hnFileName = "./scratch/outsideTemp.log"

## END STUFF YOU NEED TO CONFIGURE LOCALLY #######################################

# multiple channels to monitor using ThingSpeak
# see Arduino code in uMProductionFeb8 folder - these are defined in uMProductionFeb8.ino (main tab)
sump = 1
furnace = 2
water = 3
garage = 4
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
	
## get the ThingSpeak API key from keyfile #######################################
ThingSpeakKey = uwlib.getkey(keyfile)
if (verboseMode):
	print "sending to ThingSpeak with API ->", ThingSpeakKey

## Connect to onboard XBee radio ###############################
ser = serial.Serial(myUSBserial, myBaud)
ser.flushInput()

if (verboseMode):
	print "----->starting server at ", datetime.datetime.now()
else:
	print "started"

## initialize variables ##############################
gotSump = gotHvac = gotWater = False
sumpSensor = garageSensor = waterSensor = hvacSensor = 0
sumpState = garageState = waterState = hvacState = 0
sumpRecent = sumpDuty = 0
outsideTemp = 0

## main loop ##################################################

while 1:

	sensorValue = state =  0

	try:
		xbeeOK = True
		payload = []
		xbeeData=ser.readline()
		if xbeeOK:
			try:
				payload = uwlib.parser(xbeeData)
			except:
				print datetime.datetime.now(), " ERROR: problem parsing xBee data ->", xbeeData
				xbeeOK = False

	# assuming everything is ok with the data from Arduino, look at the channel and prep for reporting to ThingSpeak

		if xbeeOK:
			if (verboseMode):
				print datetime.datetime.now(), "->", payload
	
			try:
				channel = payload[0]
				sensorValue = payload[1]
				state = payload[2]
				recent = payload[3]

				if int(channel) == sump:					 # SUMP
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
	
				if int(channel) == furnace:					 # HVAC
					gotHvac = True
					hvacSensor = sensorValue
					hvacState = state
	
				if int(channel) == water:					 # WATER heater
					gotWater = True
					waterSensor = sensorValue
					waterState = state

				if int(channel) == garage:					 # GARAGE heater
					garageSensor = sensorValue
					garageState = state

			except:
				print datetime.datetime.now(), " ERROR: problem matching channel ->", payload
	
	# if we have everyone...(don't wait for garage)... grab outside temp and report to ThingSpeak

			if (gotSump and gotHvac and gotWater):
				gotSump = gotHvac = gotWater = False
				# get outside temp from NOAA
				noaaSuccess = True
				try:
					subprocess.call([noaaScript])
				except:
					logMsg = datetime.datetime.now() + "ERROR: failed shell script execute - " + noaaScript
					print logMsg
					noaaSuccess = False
				if (noaaSuccess):
					NewOutsideTemp = uwlib.readNoaa(hnFileName)
					if (NewOutsideTemp != -459.67):	 #absolute zero means something went wrong reading hnFileName
						outsideTemp = NewOutsideTemp
						
				if (verboseMode):
					print datetime.datetime.now(), "outside temperature ->", outsideTemp

# note that the channels in ThingSpeak have individual charts, corresponding
# to "field1" through "fieldn" in the call below

				params = urllib.urlencode({'field1' : sumpSensor,  'field2' : sumpState,
										   'field3' : hvacSensor,  'field4' : hvacState,
										   'field5' : waterSensor, 'field6' : waterState,
										   'field7' : outsideTemp, 'key'    : ThingSpeakKey})

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
