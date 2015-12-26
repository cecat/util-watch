#!/bin/bash
# change to hardcoded pathname if you from crontab
# also note you will want to substitute here the closest weather station to your location.
# to find your station, go here: http://weather.noaa.gov and then look at the "XYZ.html" code in the URL, and
# substitute it for the "KORD" (fyi ORD = O'Hare Int'l Airport) below.

#curl -s http://weather.noaa.gov/pub/data/observations/metar/decoded/KORD.TXT > /home/pi/python-sensors/currentWeather.txt
curl -s http://weather.noaa.gov/pub/data/observations/metar/decoded/KORD.TXT > ./currentWeather.txt

now=$(date +%T)
TEMP=`awk -F': ' '/Temperature/ {print $2}' ./currentWeather.txt`

echo $now "|" $TEMP  >> ./outsideTemp.log

