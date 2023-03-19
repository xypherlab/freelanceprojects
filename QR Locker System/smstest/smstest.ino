#include <SoftwareSerial.h>
SoftwareSerial sim(10, 11);
int _timeout;
String _buffer;
String  number;
void setup() {
  delay(7000); 
  Serial.begin(9600);
  _buffer.reserve(50);
  sim.begin(9600);
  delay(1000);
}
void loop() {
  number = "09062795780";
  SendMessage();
  delay(30000);
}
void SendMessage()
{
  sim.println("AT+CMGF=1");  
  delay(1000);
  Serial.println ("Set SMS Number");
  sim.println("AT+CMGS=\"" + number + "\"\r"); 
  delay(1000);
  String SMS = "Thank you for using our service. You have 1 hour left on your rented locker.";
  sim.println(SMS);
  delay(100);
  sim.println((char)26);
  delay(1000);
  _buffer = _readSerial();
}
String _readSerial() {
  _timeout = 0;
  while  (!sim.available() && _timeout < 12000  )
  {
    delay(13);
    _timeout++;
  }
  if (sim.available()) {
    return sim.readString();
  }
}
