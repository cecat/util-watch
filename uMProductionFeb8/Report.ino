        void ReportOut() {
           // report sump
              sumpFreq = lastWindowCount(SUMP);
              Serial.print  (SUMP);     Serial.print(",");
              Serial.print  (motion);   Serial.print(",");
              Serial.print  (SumpON);   Serial.print(",");
              Serial.println  (sumpFreq); 

           // report hvac
              hvacFreq = lastWindowCount(HVAC);
              Serial.print  (HVAC);      Serial.print(",");
              Serial.print  (sounds);    Serial.print(",");
              Serial.print  (HvacON); Serial.print(",");
              Serial.println  (hvacFreq); 

           // report water heater
              whtrFreq = lastWindowCount(WHTR);
              Serial.print  (WHTR);      Serial.print(",");
              Serial.print  (tempF);    Serial.print(",");
              Serial.print  (WhtrON); Serial.print(",");
              Serial.println  (whtrFreq); 
        }
