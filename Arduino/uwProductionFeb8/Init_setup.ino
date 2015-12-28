// setup runs just once at the beginning

void setup()  {
  Serial.begin    (BAUDRATE);
  pinMode      (xPin, INPUT);
  pinMode      (yPin, INPUT);
  pinMode      (sPin, INPUT);
  pinMode      (led, OUTPUT);
  for (int k=0; k<HIST; k++) 
    {
       recentSUMP[k] = 0;
       recentHVAC[k] = 0;
       recentWHTR[k] = 0;
     }
}
