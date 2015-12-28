
/****************************************************************************
                  SENSOR FUNCTIONS
 ****************************************************************************/

void readSensorData()  {
     // zero out the sensor vals
     motion = sounds = 0;
     
          checkMovement();
          sounds  = checkSound(HVAC);
          checkWaterHeater();
}

/****************************************************************************
                  MOTION (accelerometer)
** using the analog pins (XA, YA) since it provides a nicely stable reading 
** vs the waveform that comes out of the pulse wave modulation
** (PWM - XP, YP) pins which are harder to intepret.
 ****************************************************************************/
void checkMovement() {
  long xBuffer[SAMPLES], yBuffer[SAMPLES];   // samples defined in Quake_monitor
  long xSum = 0;    long xAvg = 0;
  long ySum = 0;    long yAvg = 0;    int i;
  
  // this shouldn't be necessary but better safe...
  for (i=0; i<SAMPLES; i++) {xBuffer[i] = 0; yBuffer[i] = 0;}
  // collect the samples
  for (i=0; i<SAMPLES; i++) {
      delay(10); // gives time for A/D converter to reset on Arduino
      xBuffer[i] = analogRead (xPin);
      xSum += xBuffer[i];
      delay(10);
      yBuffer[i] = analogRead (yPin);
      ySum += yBuffer[i];
  }

  // compute x and y force averages
    xAvg =  (xSum / SAMPLES);
    yAvg =  (ySum / SAMPLES);
    
  // add up the variance and call that our motion value
    for (i=0; i<SAMPLES; i++) {
      motion += (abs(xBuffer[i]-xAvg)  +  abs(yBuffer[i]-yAvg) );
    }
    
  }

/****************************************************************************
                  SOUND (piezo microphone)
** watch a handful of samples to see if there is sound present.  
** values jump all over the place when there is noise but generally 0 when quiet
 ****************************************************************************/
int checkSound(int myChannel) {
  long sBuffer[SAMPLES];   
  long sSum = 0;    long sAvg = 0;   int i;
  int micVal;
  // this shouldn't be necessary but better safe...
  for (i=0; i<SAMPLES; i++) sBuffer[i] = 0; 
  // collect the samples
  
  for (i=0; i<SAMPLES; i++) {
      delay(10); // actually 10ms is enough time for A/D converter to reset on Arduino
      switch (myChannel) {
        case HVAC:
          micVal = analogRead(sPin);
          break;
     //   case <other>:        //in case we add another mic
     //     micVal = analogRead(wPin);
     //     break;
      }
      sBuffer[i] = constrain(abs(micVal - 512)-25,0,512);
      sSum += sBuffer[i];
  }

  // compute average
    sAvg =  (sSum / SAMPLES);
    
   return(sAvg);
   
}

/****************************************************************************
                  Water Heater (temperature/humidity)
** using SHT15 to measure temperature near the chimney outlet of the water heater
** don't really care about humidity but it's available so we'll check it
**
 ****************************************************************************/
void checkWaterHeater() {
  
  tempC    = water.readTemperatureC();
  tempF    = water.readTemperatureF();
  humidity = water.readHumidity    ();
}

