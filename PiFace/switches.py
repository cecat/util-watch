# testing PiFace to integrate sensors
# this code is following the instructions from the documentation 12/25/2015 here:
# https://media.readthedocs.org/pdf/pifacedigitalio/latest/pifacedigitalio.pdf
#
# CeC (cecatlett@gmail.com)
# December 2015

import pifacedigitalio 

pfio = pifacedigitalio.PiFaceDigital()

blink = 0.1	# seconds

while 1:

	try:
		for n in range (0,4):
			if (pfio.switches[n].value == 1):
				pfio.leds[n].turn_on()

		n = 3
		while (n >= 0):
			if (pfio.switches[n].value == 0):
				pfio.leds[n].turn_off()
			n = n-1

	except KeyboardInterrupt:
		print "keyboard abort"
		n = 7
		while (n > 1):
			pfio.leds[n].turn_off()
			n = n-1
		break


