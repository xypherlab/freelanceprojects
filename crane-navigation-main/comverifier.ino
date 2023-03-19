#include <SoftwareSerial.h>//Library for software serial communication
String data; //Variable data for computer interface
int minimumdistance=40; //minimum distance for brake(relay)/LED to trigger
SoftwareSerial cranecom(2, 3); //Assigned pin for software serial communication
void setup() {
//Serial Communication Baud Rates
  Serial.begin(9600);
  cranecom.begin(9600);
  //Pin assigned for relay/LED
  pinMode(13, OUTPUT);
}

void loop() {
//Serial Communication transmission to computer for RFID interface received from Zigbee connected to software serial communication
if (cranecom.available() > 0)
  { 
    String indicator  = cranecom.readStringUntil(',');
    if (indicator=="D")
    {
      int A = cranecom.parseInt();
      int B = cranecom.parseInt();
      int C = cranecom.parseInt();
      int D = cranecom.parseInt();
      int E = cranecom.parseInt();
      int F = cranecom.parseInt();
      if (A<=minimumdistance || B<=minimumdistance || C<=minimumdistance || D<=minimumdistance || E<=minimumdistance)
      {
        digitalWrite(13, HIGH);
      }
      else
      {
        digitalWrite(13, LOW);
      }
      String cardid = cranecom.readStringUntil(',');
      String temp = cranecom.readStringUntil(',');
      String flag = cranecom.readStringUntil(',');
      data+=String(A);
      data+=",";
      data+=String(B);
      data+=",";
      data+=String(C);
      data+=",";
      data+=String(D);
      data+=",";
      data+=String(E);
      data+=",";
      data+=String(F);
      data+=",";
      data+=cardid;
      data+=",";
      data+=temp;
      data+=",";
      data+=flag;
      data+=",";
      Serial.println(data);
      data="";
    
  }
  }
}


