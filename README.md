util-watch
==========

Arduino and python code to watch a furnace, sump pump, etc. using arduino/xbee gear.

1.  uMProductionFeb8
This folder contains the Arduino sketch, which includes pin assignments but assumes you have
a working serial connection (in my case using a pair of XBee radios) between the Arduino and the Pi.
Note that this code assumes your Arduino setup includes the string library (see the Main.ino file)
and the SHT1x library.

2. uW-RPI.py
This is the python code that runs on the Raspberry Pi, reads reports from the Arduino
(via the serial connection), and posts to ThingSpeak.com.

3. KEY.txt
This is the config file for uW-RPI.py where you edit and replace the current demo key
with your API write key for your ThingSpeak channel.

4. hardware folder
Includes a text file that provides the specs for the particular Arduino I am using,
including links to the parts.
