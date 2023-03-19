#include <TinyGPS++.h>
#include <SoftwareSerial.h>

static const int RXPin = 4, TXPin = 3;
static const uint32_t GPSBaud = 9600;

// The TinyGPS++ object
TinyGPSPlus gps;

// The serial connection to the GPS device
SoftwareSerial ss(RXPin, TXPin);
SoftwareSerial xbee(6, 7);
void setup(){
  Serial.begin(9600);
  ss.begin(GPSBaud);
  xbee.begin(9600);
}

void loop(){
  // This sketch displays information every time a new sentence is correctly encoded.x
  ss.listen();
  while (ss.available() > 0){
    ss.listen();
    gps.encode(ss.read());
    if (gps.location.isUpdated()){
      Serial.print("Latitude= "); 
      Serial.print(gps.location.lat(), 6);
      Serial.print(" Longitude= "); 
      Serial.println(gps.location.lng(), 6);

       xbee.listen(); 
    xbee.print("Z,");
      xbee.print(gps.location.lat(), 6);
      xbee.print(","); 
      xbee.print(gps.location.lng(), 6);
       xbee.println(",");
       ss.listen();
    }
  }
}
