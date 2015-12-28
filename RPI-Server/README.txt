KEY.txt is where you'll put your ThingSpeak API (write) key.  The one
in KEY.txt is a valid write key to a channel you can test with
(see KEY.txt for URL of the channel's page)

NOAACheck.sh is a shell script that goes and checks for the current
temperature at a NOAA site.  This one checks at Chicago O'Hare (KORD)
and there are instructions for finding the one closest to you.

uw-Server.py is the latest python server code to run on the Raspberry Pi,
reading from USB serial to get data from the Arduino.

uwlib.py is a module with a bunch of functions used by uw_Server.py

Note on running this code:
You'll need to create the scratch directory into which the NOAACheck.sh
script writes, and that is read by readNoaa in uwlib.py


