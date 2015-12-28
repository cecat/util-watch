The specific hardware I am using is below, with some notes on what I might do
differently if starting from scratch.

Note the sensors all have power and ground, which will be connected to the
Arduino pins.  There is a nice labeled diagram of the FIo here:

	https://learn.sparkfun.com/tutorials/pro-micro--fio-v3-hookup-guide/hardware-overview-fio-v3

Where you'll see that your sensors will get their power (labeled VCC on most
breakout boards) from the "3V3" pin in upper right, and ground (GND) from
either of the GND pins.


1. Arduino Fio is used here because I'm using Xbee radios and this model is
specifically designed for these radios.

		https://www.sparkfun.com/products/10116

The fio has both a USB (for power only) and battery socket, so I keep it
plugged into wall power via a standard USB power adapter and have a LiPo
battery plugged in ffor backup in case of power outage.  Of course if
power goes out the Raspberry Pi is dead, so for now the battery backup
is pointless.

Note you should be familiar with programming an Arduino, so as you know 
you'll need an FTDI adapter to program the Fio.  


2. A pair of XBee radios - I used the Xbee Pro (most powerful ones) but you
could probably get by with the regulars.

		https://www.sparkfun.com/products/8742

		These are 802.15.4 (2.4 GHz so same range as your wifi... and
		microwave oven) They are also tricky to configure - here are some
		instructions -
		http://examples.digi.com/get-started/configuring-xbee-radios-with-x-ctu/



----- to wire up the sensors the easiest thing to do is to just solder them
		to the Arduino pins.  But I used a stripboard to create a board that
		would plug into the Arduino, called a "shield" in Arduiono vocabulary,
		so that I could swap out the Arduino if I needed to do so, and so
		that I could add or swap sensors later by just modifying the shield.

		Normally you'd put female headers on the Arduino and male pins on
		the shield.  But I wanted to be able to plug the FTDI in without
		removing the shield, so I put male headers on the Fio
		and stackable headers on my shield.  The stackable headers
		have longer pins, so their male pins stick up through the shield
		allowing you to plug in the FTDI, for instance.
		(stackable headers, e.g. https://www.sparkfun.com/products/11417)
		(male headers, e.g. https://www.sparkfun.com/products/10158)


3. While the Fio has headers for the Xbee radio you'll want to add headers
for the other pins

		https://www.sparkfun.com/products/115


4. I used a stripboard to mount the sensor wires, along with header pins to
plug into the Arduino Fio A stripboard is like a breadboard but on one side
the holes are connected in rows by a strip of copper.  Where you want to
break the connection you scratch off the copper (I used a Dremmel tool to
grind it off but you could use a sharp knife, carefully in either case).
If you just have a standard breadboard you will just need to solder a
jumper from your wires over to the pins on the Fio's headers.

		stripboard: http://www.amazon.com/gp/product/B008CI5WNC/ref=s9_hps_bw_g328_i3


5. I used standard telephone wire (nice 4-wire bundles) to get from the
sensors to the shield, and have had no trouble with lengths of about 6 feet.
I don't think you'd want to go much longer than that, but it depends on the
sensor you are using.


6. Accelerometer for motion sensing.  I used a 2-axis but I am not sure where
to find them these days.  My code uses the analog outputs XA and YA and
I have these connected to pins A0 and A1 on the Fio.

The code should work fine with a 3-axis such as:

		https://www.sparkfun.com/products/9836
	or	https://www.sparkfun.com/products/12756



7.  Simple microphone for detecting HVAC (fan) action.  I have the data
output connected to (analog) pin A4 on the Fio.

		https://www.sparkfun.com/products/9964

	
8.	Temperature/Humidity for sensing water heater activity.  I have the
data line connected to pin 10 and the clock line connected to pin 11 on the
Fio.  I really did not need the humidity, so this sensor is overkill but
it's the one I used so I'm including it here:

		https://www.sparkfun.com/products/13683

This sensor requires the Arduino library (see the #include lines atop the
uMProductionFeb8.ino file) that can be found here:
	http://playground.arduino.cc/Code/Sensirion
	or
	https://github.com/lstoll/arduino-libraries/blob/master/SHT/SHT.h

	If I were designing today I would instead use this temperature sensor
		at 1/10th the cost:

		https://www.sparkfun.com/products/10988

	In which case you'd want to use the code and instructions such as you
		can find here:

		https://learn.adafruit.com/tmp36-temperature-sensor/using-a-temp-sensor

