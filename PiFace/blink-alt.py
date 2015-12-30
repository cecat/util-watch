# testing PiFace 
# using code from here:
# http://www.element14.com/community/thread/39390/l/piface-digital-2--setup-and-use
#
# CeC (cecatlett@gmail.com)
# December 2015

import pifacedigitalio as pfio
import time

myDelay = 1	# seconds
blink = 0.1	# seconds

#initialize piface
pfio.init()

while 1:

	try:
		time.sleep(myDelay)
		for n in range (2,8,2):
			pfio.digital_write(n, 1)
			time.sleep(blink)

		time.sleep(myDelay)
		n = 7
		while (n > 1):
			pfio.digital_write(n, 0)
			time.sleep(blink)
			n = n-1

	except KeyboardInterrupt:
		print "keyboard abort"
		break


