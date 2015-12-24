/*
 Keep track of the number of times we've seen the unit
 go on in the past Window ms
 */

int lastWindowCount(int channel) {
  int myCount               = 0;
  unsigned long totalActive = 0;
  int myWindow;now   = millis();
    
  for (int i=0; i<HIST; i++) {
    switch (channel) {
      case SUMP:
        if (recentSUMP[i] > 0 && (now - recentSUMP[i]) < SUMPWINDOW) {
            myCount++;    
        }
        break;
      case HVAC:
        if (recentHVAC[i] > 0 && (now - recentHVAC[i]) < HVACWINDOW) {
            myCount++;     
        }
        break;
        case WHTR:
        if (recentWHTR[i] > 0 && (now - recentWHTR[i]) < WHTRWINDOW) {
            myCount++;     
        }
        break;
    }
  }
  return(myCount);
}

