#!/bin/bash
# go grab timestamp and temperature from Twine; print it to screen
# NOTE: make sure this file is executable (chmod +x <filename>)

# NOTE on first wget: you must replace "MyEmail@foo.org" with your Twine login
#	email and replace "mypassword" with your Twine password

wget --timeout=60 -o ./scratch/log.txt --quiet -O ./scratch/temp.txt --keep-session-cookies --save-cookies ./scratch/cookies.txt --no-check-certificate --post-data="email=MyEmail@foo.org&password=mypassword" https://twine.cc/login

# AND on this next wget: you must replace "Specific-Device" with your
#	device info from Twine

wget --timeout=60 -o ./scratch/log.txt --quiet -O ./scratch/temp.txt --load-cookies ./scratch/cookies.txt --no-check-certificate https://twine.cc/Specific-Device/rt?cached=1

DATE=`date`

TEMP=`cat ./scratch/temp.txt | awk -F"," '{print $7}' | awk -F"]" '{print $1}' | tr -d ' '`

TEMP=${TEMP:0:2}

AGE=`cat ./scratch/temp.txt | awk -F"," '{print $2}' | awk -F":" '{print $2}' | tr -d ' ' | awk -F"." '{print $1}'`

echo "$DATE |$TEMP |$AGE" >> ./scratch/laketemp.log
echo " " >> ./scratch/lakelog.txt
cat ./scratch/temp.txt >> ./scratch/lakelog.txt
