#!/usr/bin/python
# Filename: uwlib.py

##### error return values #####
ZERO_K = -459.67	# absolute zero

##### extract a ThingSpeak key from a file #####

def getkey(keyfile):

	with open (keyfile, "r") as f:

		key = f.readline().rstrip()
		column1 = "#"				# ignore comments and empty lines
	   	while (column1 == "#"):
			if len(key) == 0:		# empty line
				key = "#"
			column1 = key[0]
			if column1 == "#":		# empty or first char is "#"
				key = f.readline().rstrip()

	return key


##### parse a packet received via serial, #####
# of the form "a, b, c, d", put into a list and return

def parser(xbeeData):

	payload = []		# create an empty list

	try:
		tempString = xbeeData.rstrip()
		c1 = tempString.find(',')
		payload.append(tempString[:c1])
		c2 = tempString.find(',',c1+1)
		payload.append(tempString[c1+1 : c2])
		c3 = tempString.find(',',c2+1)
		payload.append(tempString[c2+1 : c3])
		payload.append(tempString[c3+1 : ])
	except:
		print datetime.datetime.now()," ERROR:  collision (packat corrupted) or improper format."
		print "        Data received from Arduino: ", xbeeData
		xbeeOK = False

	return payload


##### read temperature from end of the NOAA script log file #####
# get-to-the-last-line-in-the-file code from Latty@stackoverflow 2/7/12 at 23:59

def readNoaa (noaaFile):

	last = None
	with open (noaaFile, "r") as f:
		for line in f:
			last = line
		tpoint1 = last.find('|')
		tpoint2 = last.find('F', tpoint1+1)
		tempStr = last[tpoint1+1 : tpoint2-1]

	try:
		temperature = float(tempStr)
	except:
		temperature = ZERO_K	#set to absolute zero to signal failure

	return temperature


##### read temperature from end of the Twine script log file #####
# get-to-the-last-line-in-the-file code from Latty@stackoverflow 2/7/12 at 23:59

def readTwine (twineFile):
	twineVals = [1, 1]		# empty list to use to return temp and age

	last = None
	with open (twineFile, "r") as f:
		for line in f:
			last = line
	tpoint1 = last.find('|')
	tpoint2 = last.find('|', tpoint1+1)
	temperature = last[tpoint1+1 : tpoint2]	
	age = last[tpoint2+1 : ]				# seconds since last updated

	try:
		if tpoint2 == (tpoint1+2):	
			twineVals[0] = ZERO_K
		else:
			twineVals[0] = int(temperature)
	except:
		twineVals[0] = ZERO_K	#set to absolute zero to signal failure
	try:
		twineVals[1] = int(age)
	except:
		twineVals[1] = float(3601)		# more than an hour...

	return twineVals

version = '0.1'

# End of uwlib.py
