util-watch
==========

arduino and python code to watch a furnace, sump pump, etc. using arduino/xbee gear

uMProductionFeb8 is the Arduino sketch, which includes pin assignments but assumes you have
a working serial connection (in my case using a pair of XBee radios) between the Arduino and the Pi.

uW-RPI is the python code that reads reports from the Arduino and posts to ThingSpeak.com.  It must
be configured with your API keys for ThingSpeak.
