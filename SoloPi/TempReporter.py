#python code to report temperature to Thingspeak.com
# Charlie Catlett (cecatlett@gmail.com)
# January 2014

import datetime
import time
import httplib, urllib
import sys
import subprocess
import syslog
import os
import glob

# import my utility-watch library
import uwlib

## LOCAL CONFIG ###################################################
# temperature file for our sensor - follow instructions below to
# find your device number
#	https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/ds18b20

#tfileName = "/sys/bus/w1/devices/28-000003e3ff85/w1_slave"
tfileName = "./w1_slave"				 # for code testing without a sensor

#	shell scripts and files

twineScript = "./TwineCheck.sh"			# check Twine (inside temperature)
sFileName = "./scratch/laketemp.log"	# output from twineScript
noaaScript = "./NOAACheck.sh"			# check NOAA weather (outside temperature)
nFileName = "./scratch/outsideTemp.log" # output from noaaScript
keyfile = "./KEY.txt"					# ThingSpeak API key

#	delay settings 

myDelay = 10					# seconds between ThingSpeak updates

##	initialize everything to zero

cabinTemp = 0.0
insideTemp = 0.0
newOutsideTemp = 0.0
crawlTemperature = 0.0
insideAge = 0
twineVals = [0,0]

## command line variables #######################################

verboseMode = False
# do we have any arguments at all?
if (len(sys.argv) > 1):
	sys.argv.pop(0) #remove the program name, don't need it
	if sys.argv.count("-v"):
		verboseMode = True

logMsg = str(datetime.datetime.now()) + " TempReporter STARTING"
print logMsg
syslog.syslog(logMsg)

## read thingspeak channel from KEY.txt file ####################

ThingSpeakKey = uwlib.getkey(keyfile)

if (verboseMode):
	print "INFO: sending to ThingSpeak with API ->", ThingSpeakKey

## set up one-wire sensor ####################################

try:
	os.system('modprobe w1-gpio')
	os.system('modprobe w1-therm')
except:
	logMsg = "ERROR: failed to set up sensor"
	print logMsg
	syslog.syslog(logMsg)

## main loop ##################################################

while 1:
	
	time.sleep(myDelay)

	try:

		#----- get crawlspace temp from onboard thermometer -----#

		try:
			tfile = open(tfileName, 'r')
			text = tfile.readlines()
			tfile.close()
		except:
			logMsg = "ERROR: could not open " + tfileName
			print logMsg
			syslog.syslog(logMsg)

		try:
			if text[0].strip()[-3:] == 'YES':   #otherwise leave as is
				equals_pos = text[1].find('t=')
				if equals_pos != -1:
					temp_string = text[1][equals_pos+2:]
					temp_c = float(temp_string) / 1000.0
					crawlTemperature = temp_c * 9.0 / 5.0 + 32.0
		except:
			logMsg = "ERROR: could not parse data from " + tfileName
			print logMsg
			syslog.syslog(logMsg)

		#----- get inside temp from Twine ------------------------#
		
		if (verboseMode):
			logMsg = "INFO: run twineScript"
			print logMsg
			syslog.syslog(logMsg)

		twineSuccess = True
		try:
			subprocess.call([twineScript])
		except:
			logMsg = "ERROR: failed shell script execute - " + twineScript
			print logMsg
			syslog.syslog(logMsg)
			twineSuccess = False

		if (twineSuccess):
			if (verboseMode):
				logMsg = "INFO:     twineScript returned"
				print logMsg
				syslog.syslog(logMsg)
			twineVals = uwlib.readTwine(sFileName)

		if (verboseMode):
			logMsg = ("INFO:     Twine temperature=" + str(twineVals[0]) +
											"; age=" + str(twineVals[1]) )
			print logMsg
			syslog.syslog(logMsg)

			#----- get outside temp from NOAA ---------------------------#

		if (verboseMode):
			logMsg = "INFO: run noaaScript"
			print logMsg
			syslog.syslog(logMsg)

		noaaSuccess = True
		try:
			subprocess.call([noaaScript])
		except:
			logMsg = "ERROR: failed shell script execute - " + noaaScript
			print logMsg
			syslog.syslog(logMsg)
			noaaSuccess = False

		if (noaaSuccess):
			newOutsideTemp = uwlib.readNoaa(nFileName)
			if (newOutsideTemp != -459.67):  # abs zero means error reading file
				outsideTemp = newOutsideTemp

		if (verboseMode):
			logMsg = "INFO:     NOAA temperature=" +  str(outsideTemp)
			print logMsg
			syslog.syslog(logMsg)

		#----- set up the ThingSpeak call -------------------------------------#

		params = urllib.urlencode( {'field1':crawlTemperature,'field2':insideTemp,
									'field3':insideAge,'field4':outsideTemp,
									'key':ThingSpeakKey})

		if (verboseMode):
			logMsg = "INFO: push to ThingSpeak"
			print logMsg
			syslog.syslog(logMsg)
		try:
			headers = ( {"Content-type": "application/x-www-form-urlencoded",
						"Accept": "text/plain"} )
			conn = httplib.HTTPConnection("api.thingspeak.com:80")
			conn.request("POST", "/update", params, headers)
			response = conn.getresponse()
			if response.status != 200: 
				print "POST failed->", response.status, response.reason
			data = response.read()
			conn.close()
		except:
			logMsg = "ERROR: failed to post data to ThingSpeak.com"
			print logMsg
			syslog.syslog(logMsg)
		if (verboseMode):
			logMsg = "INFO:      returned from push ThingSpeak"
			print logMsg
			syslog.syslog(logMsg)

	except KeyboardInterrupt:
		logMsg = "  ABORT (keyboard interrupt)"
		print logMsg
		syslog.syslog(logMsg)
		break
