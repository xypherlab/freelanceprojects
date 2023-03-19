#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
RF24 radio(7, 8); // CE, CSN
const byte addresses[][6] = {"00001", "00002"};

#define ANALOG_PIN A0 // Analog pin
#define RESISTANCE 10 // Resistance in thousands of ohms
volatile float PANEL_LENGTH = 127; // Length of solar cell in mm
volatile float PANEL_WIDTH = 76; // Width of solar cell in mm
volatile float Area;
volatile float Power;
volatile float Radiation;


String data;
String dataA;
String dataB;
String dataC;
String dataD;
String dataE;
String dataF;

String timedelay;
void setup() {
Serial.begin(9600);
radio.begin();
radio.openWritingPipe(addresses[1]); // 00002
radio.openReadingPipe(1, addresses[0]); // 00001
radio.setPALevel(RF24_PA_MIN);       //You can set this as minimum or maximum depending on the distance between the transmitter and receiver.
radio.startListening();              //This sets the module as receiver
}
void loop()
{
if (radio.available())              //Looking for the data.
{
char text[32] = "";                 //Saving the incoming data
radio.read(&text, sizeof(text));    //Reading the data
data=String(text);
String response = getValue(data, ',', 0);
//Serial.println(response);
//Serial.println(data);
if (response=="A")
{ dataA=data;
  
}
else if (response=="B")
{ dataB=data;
  
}
else if (response=="C")
{ dataC=data;
  
}
else if (response=="D")
{ dataD=data;
  
}
else if (response=="E")
{ dataE=data;
  
}
else if (response=="F")
{ dataF=data;
  
}  
}
if(Serial.available()) 
  {String flagmode = Serial.readStringUntil(',');
   
  if (flagmode=="R")
{
Area = PANEL_LENGTH * PANEL_WIDTH / (100*100); // we are dividing by 10000 get the area in square meters
Power = pow(analogRead( ANALOG_PIN ), 2) / RESISTANCE ; // Calculating power
Radiation = Power / Area;
Serial.print(Radiation); Serial.print(","); 
Serial.print(dataA);
Serial.print(dataB);
Serial.print(dataC);
Serial.print(dataD);
Serial.print(dataE);
Serial.println(dataF);
dataA="";
dataB="";
dataC="";
dataD="";
dataE="";
dataF="";
}
 else if (flagmode=="ZA")
{timedelay = Serial.readStringUntil(',');
String delaydata="RA,"+timedelay+",";
int delaydata_len = delaydata.length() + 1; 
char text[delaydata_len];
delaydata.toCharArray(text, delaydata_len); 
radio.stopListening();
radio.write(&text, sizeof(text));
delay(5);
  radio.startListening();
}
 else if (flagmode=="ZB")
{timedelay = Serial.readStringUntil(',');
String delaydata="RB,"+timedelay+",";
int delaydata_len = delaydata.length() + 1; 
char text[delaydata_len];
delaydata.toCharArray(text, delaydata_len); 
radio.stopListening();
radio.write(&text, sizeof(text));
delay(5);
  radio.startListening();
}
 else if (flagmode=="ZC")
{timedelay = Serial.readStringUntil(',');
String delaydata="RC,"+timedelay+",";
int delaydata_len = delaydata.length() + 1; 
char text[delaydata_len];
delaydata.toCharArray(text, delaydata_len); 

radio.stopListening();

radio.write(&text, sizeof(text));
delay(5);
  radio.startListening();
}
 else if (flagmode=="ZD")
{timedelay = Serial.readStringUntil(',');
String delaydata= "RD,"+timedelay+",";
int delaydata_len = delaydata.length() + 1; 
char text[delaydata_len];
delaydata.toCharArray(text, delaydata_len); 
radio.stopListening();

radio.write(&text, sizeof(text));
delay(5);
  radio.startListening();
}
 else if (flagmode=="ZE")
{timedelay = Serial.readStringUntil(',');
String delaydata="RE,"+timedelay+",";
int delaydata_len = delaydata.length() + 1; 
char text[delaydata_len];
delaydata.toCharArray(text, delaydata_len); 

radio.stopListening();

radio.write(&text, sizeof(text));
delay(5);
  radio.startListening();
}
 else if (flagmode=="ZF")
{timedelay = Serial.readStringUntil(',');
String delaydata="RF,"+timedelay+",";
int delaydata_len = delaydata.length() + 1; 
char text[delaydata_len];
delaydata.toCharArray(text, delaydata_len); 

radio.stopListening();

radio.write(&text, sizeof(text));
delay(5);
  radio.startListening();
}
///////////////////////////////////////////////////////////////////
else if (flagmode=="YA")
{timedelay = Serial.readStringUntil(',');
String delaydata="QA,"+timedelay+",";
int delaydata_len = delaydata.length() + 1; 
char text[delaydata_len];
delaydata.toCharArray(text, delaydata_len); 
radio.stopListening();
radio.write(&text, sizeof(text));
delay(5);
  radio.startListening();
}
 else if (flagmode=="YB")
{timedelay = Serial.readStringUntil(',');
String delaydata="QB,"+timedelay+",";
int delaydata_len = delaydata.length() + 1; 
char text[delaydata_len];
delaydata.toCharArray(text, delaydata_len); 
radio.stopListening();
radio.write(&text, sizeof(text));
delay(5);
  radio.startListening();
}
 else if (flagmode=="YC")
{timedelay = Serial.readStringUntil(',');
String delaydata="QC,"+timedelay+",";
int delaydata_len = delaydata.length() + 1; 
char text[delaydata_len];
delaydata.toCharArray(text, delaydata_len); 

radio.stopListening();

radio.write(&text, sizeof(text));
delay(5);
  radio.startListening();
}
 else if (flagmode=="YD")
{timedelay = Serial.readStringUntil(',');
String delaydata= "QD,"+timedelay+",";
int delaydata_len = delaydata.length() + 1; 
char text[delaydata_len];
delaydata.toCharArray(text, delaydata_len); 
radio.stopListening();

radio.write(&text, sizeof(text));
delay(5);
  radio.startListening();
}
 else if (flagmode=="YE")
{timedelay = Serial.readStringUntil(',');
String delaydata="QE,"+timedelay+",";
int delaydata_len = delaydata.length() + 1; 
char text[delaydata_len];
delaydata.toCharArray(text, delaydata_len); 

radio.stopListening();

radio.write(&text, sizeof(text));
delay(5);
  radio.startListening();
}
 else if (flagmode=="YF")
{timedelay = Serial.readStringUntil(',');
String delaydata="QF,"+timedelay+",";
int delaydata_len = delaydata.length() + 1; 
char text[delaydata_len];
delaydata.toCharArray(text, delaydata_len); 

radio.stopListening();

radio.write(&text, sizeof(text));
delay(5);
  radio.startListening();
}

  }
delay(5);
} 

String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length()-1;

  for(int i=0; i<=maxIndex && found<=index; i++){
    if(data.charAt(i)==separator || i==maxIndex){
        found++;
        strIndex[0] = strIndex[1]+1;
        strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  }

  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}
