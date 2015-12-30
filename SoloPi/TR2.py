# Temperature Reporter
# python code to report temperature to Thingspeak.com
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

## CONFIG ###################################################
# temperature file for our sensor - follow instructions below to
# find your device number
#	https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/ds18b20

#	shell scripts and files

#tfileName = "/sys/bus/w1/devices/28-000003e3ff85/w1_slave"
#for testing instead of above:
tfileName = "./w1_slave"
twineScript = "./TwineCheck.sh"		# check Twine (inside temperature)
sFileName = "./scratch/laketemp.log"	# output from twineScript
noaaScript = "./NOAACheck.sh"		# check NOAA weather (outside temperature)
nFileName = "./scratch/outsideTemp.log" # output from noaaScript

#	delay settings 

myDelay = 10					# seconds between ThingSpeak updates

##	initialize everything to zero

cabintemp = 0.0
insideTemp = 0.0
noaaTemp = 0.0
crawlTemperature = 0.0
insideAge = 0

## command line variables #######################################

verboseMode = False
# do we have any arguments at all?
if (len(sys.argv) > 1):
	sys.argv.pop(0) #remove the program name, don't need it
	if sys.argv.count("-v"):
		verboseMode = True

logMsg = "START"
print logMsg
syslog.syslog(logMsg)

## read thingspeak channel from KEY.txt file ####################

keyfile = "./KEY.txt"
with open (keyfile, "r") as f:
	ThingSpeakKey = f.readline().rstrip()
	hashmark = "#"
	while (hashmark == "#"):	 # ignore comments and empty lines
		if len(ThingSpeakKey) == 0:
			ThingSpeakKey = "#"
		hashmark = ThingSpeakKey[0]
		if hashmark == "#":
			ThingSpeakKey = f.readline().rstrip()
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
			with open (sFileName, "r") as f:
				first =f.readline()
				f.seek(-2, 2)
				while f.read(1) != "\n":
					f.seek(-2, 1)
				last = f.readline()
				tpoint1 = last.find('|')
				tpoint2 = last.find('|', tpoint1+1)
				cabintemp = last[tpoint1+1 : tpoint2]
				age = last[tpoint2+1 : ]
			try:
				insideTemp = int(cabintemp)
				insideAge = int(age)
			except:
				logMsg = "ERROR: failed to convert cabintemp or age"
				syslog.syslog(logMsg)

		if (verboseMode):
			logMsg = "INFO:     Twine temperature=" + cabintemp + "; age=" +  age
			print logMsg
			syslog.syslog(logMsg)

			#----- get outside temp from NOAA ---------------------------#

		if (verboseMode):
			logMsg = "INFO: run noaaScript"
			print logMsg
			syslog.syslog(logMsg)

		noaaSuccess = True
		lastNoaa = noaaTemp
		try:
			subprocess.call([noaaScript])
		except:
			logMsg = "ERROR: failed shell script execute - " + noaaScript
			print logMsg
			syslog.syslog(logMsg)
			noaaSuccess = False

		if (noaaSuccess):
			if (verboseMode):
				logMsg = "INFO:     noaaScript returned"
				print logMsg
				syslog.syslog(logMsg)
			with open (nFileName, "r") as f:
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
				logMsg = "ERROR: failed to convert noaaTemp"
				syslog.syslog(logMsg)
				outsideTemp = float(lastNoaa)
		if (verboseMode):
			logMsg = "INFO:     NOAA temperature=" +  noaaTemp
			print logMsg
			syslog.syslog(logMsg)

		#----- set up the ThingSpeak call -------------------------------------#

		params = urllib.urlencode({'field1':crawlTemperature,'field2':insideTemp,'field3':insideAge,'field4':outsideTemp,'key':ThingSpeakKey})

		if (verboseMode):
			logMsg = "INFO: push to ThingSpeak"
			print logMsg
			syslog.syslog(logMsg)
		try:
			headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
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
		logMsg = "ABORT (keyboard interrupt)"
		print logMsg
		syslog.syslog(logMsg)
		break
