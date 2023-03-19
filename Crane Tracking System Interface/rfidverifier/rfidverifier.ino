#define  STX 2 //Start of character of RFID
#define  ETX 3 //End of character of RFID
#define  SERIALSTX 0 //Serial transmission of STX
#define  SERIALETX 1 //Serial transmission of ETX
#define  SERIALRDY 2 //Serial transmission indicator
#include "cactus_io_DHT22.h" //Temperature library
 String card_enrolled;  //Variable flag of rfid cards
 String  card_addr;     //Variable address of rfid cards 
 String  card_type;     //Variable type of rfid cards
 String  card_number;   //Variable id number of rfid cards
 
//Ultrasonic trigger and echo pin 
const int trigPinA = 2;
const int echoPinA = 3;
const int trigPinB = 4;
const int echoPinB = 5;
const int trigPinC = 6;
const int echoPinC = 7;
const int trigPinD = 8;
const int echoPinD = 9;
const int trigPinE = 10;
const int echoPinE = 11;
const int trigPinF = 12;
const int echoPinF = 13;
//Variables for time and distance
long durationA;
float distanceA;
float distanceA1=0;
long durationB;
float distanceB;
float distanceB1=0;
long durationC;
float distanceC;
float distanceC1=0;
long durationD;
float distanceD;
float distanceD1=0;
long durationE;
float distanceE;
float distanceE1=0;
long durationF;
float distanceF;
float distanceF1=0;

byte  serial_state; //Variable flag for serial of RFID
String serialinput; //Variable data for serial transmission of rfid interface
boolean  carddetected=false; //Flag if card is detected
int flagstatus=0; //Flag status for state of pick and drop
String datacargo; //Variable data for serial transmission of rfid sql database  
#define DHT22_PIN 24 //Pin assignment for temperature sensor
DHT22 dht(DHT22_PIN); //Execution of temperature sensor function
const int dhtPin =  25; //Pin assignement Supply of temperature sensor
void setup() {
     pinMode(dhtPin, OUTPUT); //Supply of temperature sensor is assigned as output digital pin
  digitalWrite(dhtPin, HIGH);  //Turn on supply of temperature sensor
    dht.begin(); //Start temperature sensor operation
//Assigned trigger pin of ultrasonic as output and echo pin as input	
  pinMode(trigPinA, OUTPUT); 
pinMode(echoPinA, INPUT);
pinMode(trigPinB, OUTPUT); 
pinMode(echoPinB, INPUT); 
pinMode(trigPinC, OUTPUT); 
pinMode(echoPinC, INPUT); 
pinMode(trigPinD, OUTPUT); 
pinMode(echoPinD, INPUT); 
pinMode(trigPinE, OUTPUT); 
pinMode(echoPinE, INPUT); 
pinMode(trigPinF, OUTPUT); 
pinMode(echoPinF, INPUT);
//Serial baud rate of all serial communication where zigbee is connected 
  Serial.begin(9600);
  Serial1.begin(9600);
  Serial2.begin(9600);
  serialinput="";
 //RFID check state
  serial_state=SERIALSTX;
  
  check_RFID();
  
}

void loop() {
    dht.readHumidity(); //Extract humidity data (not used)
  dht.readTemperature();//Extract temperature data
float temp=dht.temperature_C; //Extracted data assigned to temp variable
float c = 331.3 + 0.606*temp/100; //Temperature compensation for speed of sound


//Operation state of echo feedback from trigger signal transmission    
digitalWrite(trigPinA, LOW);
delayMicroseconds(2);
digitalWrite(trigPinA, HIGH);
delayMicroseconds(10);
digitalWrite(trigPinA, LOW);
durationA = pulseIn(echoPinA, HIGH);
distanceA= durationA*c/20000;
digitalWrite(trigPinB, LOW);
delayMicroseconds(2);
digitalWrite(trigPinB, HIGH);
delayMicroseconds(10);
digitalWrite(trigPinB, LOW);
durationB = pulseIn(echoPinB, HIGH);
distanceB= durationB*c/20000;
digitalWrite(trigPinC, LOW);
delayMicroseconds(2);
digitalWrite(trigPinC, HIGH);
delayMicroseconds(10);
digitalWrite(trigPinC, LOW);
durationC = pulseIn(echoPinC, HIGH);
distanceC= durationC*c/20000;
digitalWrite(trigPinD, LOW);
delayMicroseconds(2);
digitalWrite(trigPinD, HIGH);
delayMicroseconds(10);
digitalWrite(trigPinD, LOW);
durationD = pulseIn(echoPinD, HIGH);
distanceD= durationD*c/20000;
digitalWrite(trigPinE, LOW);
delayMicroseconds(2);
digitalWrite(trigPinE, HIGH);
delayMicroseconds(10);
digitalWrite(trigPinE, LOW);
durationE = pulseIn(echoPinE, HIGH);
distanceE= durationE*c/20000;
digitalWrite(trigPinF, LOW);
delayMicroseconds(2);
digitalWrite(trigPinF, HIGH);
delayMicroseconds(10);
digitalWrite(trigPinF, LOW);
durationF = pulseIn(echoPinF, HIGH);
distanceF= durationF*c/20000;

//Conditional statement for bug removal
if (distanceA>=3000)
{
distanceA=distanceA1;
 
}
if (distanceB>=3000)
{
distanceB=distanceB1;
 
}
if (distanceC>=3000)
{
distanceC=distanceC1;
 
}
if (distanceD>=3000)
{
distanceD=distanceD1;
 
}
if (distanceE>=3000)
{
distanceE=distanceE1;
 
}
if (distanceF>=3000)
{
distanceF=distanceF1;
 
}
/*
 Serial.print("Distance A: ");
Serial.println(distanceA);
 Serial.print("Distance B: ");
Serial.println(distanceB);
 Serial.print("Distance C: ");
Serial.println(distanceC);
 Serial.print("Distance D: ");
Serial.println(distanceD);
 Serial.print("Distance E: ");
Serial.println(distanceE);
 Serial.print("Distance F: ");
Serial.println(distanceF);*/

distanceA1=distanceA;
distanceB1=distanceB;
distanceC1=distanceC;
distanceD1=distanceD;
distanceE1=distanceE;
distanceF1=distanceF;

//RFID detection and card id extraction
  if(check_RFID()==true && flagstatus==0){
    flagstatus=1;
    Serial.println(card_number);

  }
  if (distanceA>=70 && flagstatus==2)
  {
    flagstatus=3;
  }
 
  //check_RFID();
  //Serial.println(card_number);
//Data for serial transmission to rfid interface  
datacargo+="D,";
datacargo+=String(distanceB);
datacargo+=",";
datacargo+=String(distanceC);
datacargo+=",";
datacargo+=String(distanceD);
datacargo+=",";
datacargo+=String(distanceE);
datacargo+=",";
datacargo+=String(distanceF);
datacargo+=",";
datacargo+=String(distanceA);
datacargo+=",";
    datacargo+=card_number;
datacargo+=",";    
datacargo+=String(temp);    
      datacargo+=",0,";
Serial2.print(datacargo);
datacargo="";
//RFID serial transmission to RFID sql database
if (Serial1.available() > 0)
  { 
    String response  = Serial1.readStringUntil(',');
    if (response=="A")
    {
      //Serial1.print(card_number);
      
       if (flagstatus==1)
  {datacargo+="A,";
  
datacargo+=distanceB;
datacargo+=",";
datacargo+=distanceC;
datacargo+=",";
datacargo+=distanceD;
datacargo+=",";
datacargo+=distanceE;
datacargo+=",";
datacargo+=distanceF;
datacargo+=",";
datacargo+=distanceA;
datacargo+=",";
    datacargo+=card_number;
      datacargo+=",1,";
    flagstatus=2;
  }
       else if (flagstatus==3)
  {datacargo+="A,";
  
datacargo+=distanceB;
datacargo+=",";
datacargo+=distanceC;
datacargo+=",";
datacargo+=distanceD;
datacargo+=",";
datacargo+=distanceE;
datacargo+=",";
datacargo+=distanceF;
datacargo+=",";
datacargo+=distanceA;
datacargo+=",";
    datacargo+=card_number;
      datacargo+=",2,";
      flagstatus=0;
      card_number="";
  }
  else
  { datacargo+="A,";
datacargo+=distanceB;
datacargo+=",";
datacargo+=distanceC;
datacargo+=",";
datacargo+=distanceD;
datacargo+=",";
datacargo+=distanceE;
datacargo+=",";
datacargo+=distanceF;
datacargo+=",";
datacargo+=distanceA;
datacargo+=",";
    datacargo+=card_number;
      datacargo+=",0,";
    
  }
  Serial1.print(datacargo);
      delay(100);
      datacargo="";
    }
  
  
}
}


//RFID Functions  
boolean check_RFID(void){

  int  strindex;
  int  strindexe;

     if(serial_state==SERIALRDY){
  
      strindex=serialinput.indexOf(",");
      card_enrolled=serialinput.substring(0,strindex);

      strindex++;
      strindexe=serialinput.indexOf(",",strindex);
      card_addr=serialinput.substring(strindex,strindexe);

      strindex=strindexe+1;
      strindexe=serialinput.indexOf(",",strindex);
      card_type=serialinput.substring(strindex,strindexe);

      strindex=strindexe+1;
      strindexe=serialinput.indexOf(",",strindex);
      card_number=serialinput.substring(strindex,strindexe);

     serialinput="";
     serial_state=SERIALSTX;
     return(true);
   }
   return(false);  
}


void serialEvent() {
  while (Serial.available()) {

    char inChar = (char)Serial.read();
  
    if(serial_state==SERIALSTX){
      if(inChar==STX){
        serial_state=SERIALETX;  
        return;
        }
    }
    

    if(serial_state==SERIALETX){
      if(inChar!=ETX){
        serialinput += inChar;
        return;
        }
    }
  
      serial_state=SERIALRDY;
      
    }
  }
