
/****************************************************************************
 Utility Monitor
 See Zreadme.ino
 *******************************************************************************
 This version is running in production as of 11pm 2/19/14
 ****************************************************************************/

#include <string.h>
#include <SHT1x.h>

//arduino pin assignments and modem setup
int led =                  13;
#define xPin                0          // x pin on 2-axis accelerometer
#define yPin                1          // y pin on 2-axis accelerometer
#define sPin               A4          // furnace sound pin - piezo mic pin (analog 4)
#define wDataPin           10          // data pin on SHT15 temp/humidity sensor
#define wClockPin          11          // clock pin on SHT15
#define BAUDRATE         9600          // baud rate of modem

// channels - used to tell the Python script which appliance we are talking about
#define SUMP                1                      
#define HVAC                2
#define WHTR                3

// misc constants
#define UPLOAD_INTERVAL 15000          // how often to update ThingSpeak (in ms)
#define SUMPWINDOW    1200000          // ~30m sliding window for sump duty cycle
#define HVACWINDOW    9600000          // ~4h sliding window for HVAC duty cycle
#define WHTRWINDOW    9600000          // ~4h sliding window for water heater duty cycle
#define SAMPLES             8          // number of samples read to determine sensor value                               
#define HIST               30          // max expected runs per WINDOW (sets circular buffer size)

// thesholds to decide whether the appliance is active or not
#define VIBES             100          // sump motion
#define RESTING            50      
#define BLOWING            50          // hvac sound
#define NOTBLOWING         20   
#define HEATING           120          // water heater chimney temperature
#define NOT_HEATING       100
#define DAMP                3          // for HVAC, look at multiple consecutive readings to ignore outliers

// SHT15 temp/humidity sensor
SHT1x water(wDataPin, wClockPin);

// set sensor values and arrays to zero at startup
long motion =               0;       long sounds =                0;
float tempC =               0;      float tempF  =                0;
float humidity =            0;
//HVAC use multiple consecutive readings to ignore outliers
long soundHist        [DAMP];        int shPtr =                  0;
boolean reallyQuiet;
// time
unsigned long             now;      unsigned long last_report =   0;
unsigned long lastOnSump =  0;      unsigned long lastOnHvac  =   0;
unsigned long lastOnWhtr =  0;
// run count
int sumpFreq;                        int hvacFreq;                    
int whtrFreq;
int Sptr =                  0;       int Hptr =                   0;     
int Wptr = 0;
unsigned long recentSUMP[HIST];      unsigned long recentHVAC[HIST];       
unsigned long recentWHTR[HIST];
//state
boolean SumpON =       false;        boolean HvacON =         false;
boolean WhtrON =       false;





