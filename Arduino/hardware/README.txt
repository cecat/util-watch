The specific hardware I am using is below, with some notes on what I might do
differently if starting from scratch.

Note the sensors all have power and ground, which will be connected to the
Arduino pins.  There is a nice labeled diagram of the Fio here:

	https://learn.sparkfun.com/tutorials/pro-micro--fio-v3-hookup-guide/hardware-overview-fio-v3

Where you'll see that your sensors will get their power (labeled VCC on most
breakout boards) from the "3V3" pin in upper right, and ground (GND) from
either of the GND pins.


1. Arduino Fio
I used a Fio here because I'm using Xbee radios and the Fio is
specifically designed for these radios.

		https://www.sparkfun.com/products/10116

	The Fio has both a USB (for power only) and battery socket, so I keep it
	plugged into wall power via a standard USB power adapter and have a LiPo
	battery plugged in ffor backup in case of power outage.  Of course if
	power goes out the Raspberry Pi is dead, so for now the battery backup
	is pointless.

	Note you should be familiar with programming an Arduino, so as you know 
	you'll need an FTDI adapter to program the Fio.  



2. A pair of XBee radios

I used the Xbee Pro (most powerful ones) but you could probably get by with
the regulars.

	https://www.sparkfun.com/products/8742

	These are 802.15.4 (2.4 GHz so same range as your wifi... and
	microwave oven) They are also tricky to configure - here are some
	instructions -
	http://examples.digi.com/get-started/configuring-xbee-radios-with-x-ctu/



3. Make a shield

To wire up the sensors the easiest thing to do is to just solder them
to the Arduino pins, skipping the shield.  But I used a stripboard to
create a board that would plug into the Arduino, called a "shield" in
Arduiono vocabulary.  This allows me to easily (without a soldering iron)
swap out the Arduino if I needed to do so, and to add or swap sensors
later by just modifying the shield.

I used a stripboard to create the shield. A stripboard is like a
a plain old solderable breadboard except that on one side
the holes are connected in rows by a strip of copper, eliminating
the need to add jumpers to connect things together on the board.
Where you want to break the connection you scratch off the copper (I
used a Dremmel tool to grind it off but you could use a sharp knife,
being careful in either case).

	stripboard: http://www.amazon.com/gp/product/B008CI5WNC/ref=s9_hps_bw_g328_i3

If you wanted to use a standard breadboard and jumpers you could do this
by putting female headers on the Fio (thus using male-to-male jumpers).

Normally for a shield you would use female headers on the Arduino and
stackable headers (male-to-female) on the shield, where the top of the
shield has female headers and the male headers plug into the female 
headers on the Arduino.  But I wanted to be able to plug the FTDI in without
removing the shield, so I put male headers on the Fio
and stackable headers on my shield.  The stackable headers
have longer pins, so their male pins stick up through the shield
allowing you to plug in the FTDI, for instance.
(stackable headers, e.g. https://www.sparkfun.com/products/11417)
(male headers, e.g. https://www.sparkfun.com/products/10158)



4. Wires from sensors to shield

I used standard telephone wire (nice 4-wire bundles) to get from the
sensors to the shield, and have had no trouble with lengths of about 6 feet.
I don't think you'd want to go much longer than that, but it depends on the
sensor you are using.


5. SENSORS


5.1. Accelerometer for motion sensing.

I used a 2-axis but I am not sure where to find them these days.
My code uses the analog outputs XA and YA and I have these connected to
pins A0 and A1 on the Fio.

The code won't work with a 3-axis such as below...  So you'll need to get
the appropriate library for these, and it will be similar to the way the
code works for the SHT15 temperature/humidity sensors.  

		https://www.sparkfun.com/products/9836
	or	https://www.sparkfun.com/products/12756

Code for these -
		https://github.com/sparkfun/SparkFun_MMA8452Q_Arduino_Library/tree/V_1.1.0


5.2.  Simple microphone for detecting HVAC (fan) action.

I have the data output connected to (analog) pin A4 on the Fio.  This sensor
does not require any fancy code- it just has power, ground, and signal that
you read (see the Arduino code itself)

		https://www.sparkfun.com/products/9964

	
5.3.	Temperature/Humidity for sensing water heater activity.

Like the new accelerometers, you need a library for this sensor and you 
will see it's got a clock pin and data pins.  See the Arduino code.
I have the data line connected to pin 10 and the clock line connected
to pin 11 on the Fio.  I did not need the humidity, so this sensor
is overkill but it's the one I had handy when I put this together,
and the code works, so I'm including it here:

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


