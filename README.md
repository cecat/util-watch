#utility-watch
==========

Arduino and python code to watch a furnace, sump pump, etc. using
a Raspberry Pi with arduino/xbee gear.  Also code for monitoring 
temperatures just with a Raspberry Pi.

##1. Arduino

Contains a folder with hardware details and a folder with all of the components of the Arduino sketch.

##2. RPI-Server

This is the python code that runs on the Raspberry Pi, reads messages from the Arduino (via the serial connection), checks a NOAA local weather site to get outdoor temperature, and posts to ThingSpeak.com.

##3. PiFace

This folder has a couple of example python programs for working with the PiFace 2.

##4. Hardware 

Includes a text file that provides the specs for the particular Arduino I am using, including links to the parts.

##5. SoloPi 

Python code and shell scripts for monitoring temperature using a
one-wire temperature sensor on the Pi, querying a Twine for
indoor temperature, and querying NOAA for outside temperature.

