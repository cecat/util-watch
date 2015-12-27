#!/bin/bash

curl -s http://weather.noaa.gov/pub/data/observations/metar/decoded/KORD.TXT > ./scratch/currentWeather.txt

now=$(date +%T)
TEMP=`awk -F': ' '/Temperature/ {print $2}' ./scratch/currentWeather.txt`

echo $now "|" $TEMP  >> ./scratch/outsideTemp.log

