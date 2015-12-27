This folder has code for just using the Raspberry Pi to monitor temperature
in three ways:
(1) using a one-wire thermometer directly attached to the Pi (I use to monitor crawlspace temperature)
(2) using a Twine from (http://supermechanical.com/twine/) (I use to monitor indoor temperature)
	TwineCheck.sh does this - note you have to plug in your Twine credentials, etc.
(3) using a NOAA site to get outdoor temperature
	NOAACheck.sh does this - note you have to update it to your nearest NOAA station

The scripts and Python code use a ./scratch directory to keep various temp and log files 

As with the other Python code, you'll have to mess with pathnames if you run from Cron as root.


CeC
cecatlett@gmail.com
December 2015
