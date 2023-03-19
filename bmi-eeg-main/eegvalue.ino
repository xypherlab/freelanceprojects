#include <SoftwareSerial.h>
const int rxpin = 2;
const int txpin = 3;
float eegA=0;
int eegB=0;
int eegC=0;
SoftwareSerial bluetooth(rxpin, txpin);

void setup() {
 
  Serial.begin(9600);
  bluetooth.begin(9600);
}

void loop() {
  
  eegA = float(analogRead(A0))*float(4.888);
  eegB = analogRead(A1);
  eegC = analogRead(A2);
  bluetooth.print(eegA);bluetooth.print(",");
  bluetooth.print(eegB);bluetooth.print(",");
  bluetooth.print(eegC);bluetooth.println(",&");
  Serial.print(eegA);Serial.print(",");
  Serial.print(eegB);Serial.print(",");
  Serial.print(eegC);Serial.println(",&");
  delay(1000);        
}
