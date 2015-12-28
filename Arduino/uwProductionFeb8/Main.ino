void loop()  {
  
    //read the sensors (and use LED as a visual heartbeat)
            digitalWrite(led, HIGH);
          readSensorData();
            delay(500);   digitalWrite(led, LOW);     delay(500);
        now = millis();
     
     //decide if we've turned on or off
     // SUMP
        if ((motion > VIBES) &! SumpON) {            // detect leading edge
          SumpON = true;
          lastOnSump = now;
          recentSUMP[Sptr] = now;
          Sptr = (Sptr+1) % HIST;
        }
        if ((motion < RESTING) && SumpON) {         // detect trailing edge
          SumpON = false;
        }
        
     // HVAC
       soundHist[shPtr] = sounds;                  // look at several recent
       shPtr = (shPtr+1) % DAMP;                   // to ignore outliers
       reallyQuiet = false;
       for (int k=0; k<DAMP; k++) if (soundHist[k] < BLOWING) reallyQuiet = true;
       if (!reallyQuiet &! HvacON) {               // detect leading edge
          HvacON = true;
          lastOnHvac = now;
          recentHVAC[Hptr] = now;
          Hptr = (Hptr+1) % HIST;
        }

       reallyQuiet = true;
       for (int k=0; k<DAMP; k++) if (soundHist[k] > NOTBLOWING) reallyQuiet = false;
        if (reallyQuiet && HvacON) {              // detect trailing edge
          HvacON = false;
       }
                
       // WHTR
        if ((tempF > HEATING) &! WhtrON) {            // detect leading edge
          WhtrON = true;
          lastOnWhtr = now;
          recentWHTR[Wptr] = now;
          Wptr = (Wptr+1) % HIST;
        }
        if ((tempF < NOT_HEATING) && WhtrON) {         // detect trailing edge
          WhtrON = false;
        }
              
	//Report in at regular intervals
	  if(millis() - last_report > UPLOAD_INTERVAL)  
            {
	      last_report = millis();             // reset last-updated to current clock
              ReportOut();
            }
}
