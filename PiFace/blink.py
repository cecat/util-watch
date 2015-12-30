# testing PiFace to integrate sensors
# this code is following the instructions from the documentation 12/25/2015 here:
# https://media.readthedocs.org/pdf/pifacedigitalio/latest/pifacedigitalio.pdf
#
# CeC (cecatlett@gmail.com)
# December 2015

import pifacedigitalio 
import time

pfio = pifacedigitalio.PiFaceDigital()

myDelay = 1	# seconds
blink = 0.1	# seconds

while 1:

	try:
		time.sleep(myDelay)
		for n in range (2,8):
			pfio.leds[n].turn_on()
			time.sleep(blink)

		time.sleep(myDelay)
		n = 7
		while (n > 1):
			pfio.leds[n].turn_off()
			time.sleep(blink)
			n = n-1

	except KeyboardInterrupt:
		print "keyboard abort"
		n = 7
		while (n > 1):
			pfio.leds[n].turn_off()
			n = n-1
		break


