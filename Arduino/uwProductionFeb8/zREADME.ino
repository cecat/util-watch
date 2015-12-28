/*

Simple data logger for sending sensor data via XBEE radio in AT mode to a
Mac with Internet access sending the data to Pachube.com via a python program.
CeC (cecatlett@gmail.com)
January 2012

Dec 2013
Changed from Pachube to Thingspeak.  Modified motion sensor with thresholds
to detect sump pump activity.  Added piezo microphone with thresholds
to detect HVAC fan activty.

Sends a simple line of text every UPLOAD_INTERVAL with the following format:
<channel>,<sensor_value>,<state>,<history>

where:
<channel> identifies the unit being monitored (1=sump, 2=hvac)
<value>   is the latest reading from the sensor
<state>   is ON (1) or OFF (0) where ON means during one or more sampling
          periods (multiple happen between updates) the activity
          threshold was exceeded, indicating activity
<history> is the number of times the unit has been activated in the past WINDOW


*/

