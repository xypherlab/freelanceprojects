
#include <SparkFunTSL2561.h>
#include <Wire.h>

SFE_TSL2561 light;

boolean gain;     
unsigned int ms;
unsigned char time = 2;  

//12 13 14 15 16 17
int redpinA = 10; 
int greenpinA = 11; 
int bluepinA = 9 ;
int redpinB = 7; 
int greenpinB = 8; 
int bluepinB = 6;
int redpinC = 5; 
int greenpinC =4 ; 
int bluepinC = 3;

int redA=255;
int greenA=0;
int blueA=0;
int redB=0;
int greenB=255;
int blueB=0;
int redC=0;
int greenC=0;
int blueC=255;
double luxA;   
double luxB;   
double luxC;   
double luxD;   
double luxE;   
double luxF;   
void setup () {
  pinMode (redpinA, OUTPUT);
  pinMode (bluepinA, OUTPUT);
  pinMode (greenpinA, OUTPUT);
   pinMode (redpinB, OUTPUT);
  pinMode (bluepinB, OUTPUT);
  pinMode (greenpinB, OUTPUT);
   pinMode (redpinC, OUTPUT);
  pinMode (bluepinC, OUTPUT);
  pinMode (greenpinC, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
  pinMode(14, OUTPUT);
  pinMode(15, OUTPUT);
  pinMode(16, OUTPUT);
  pinMode(17, OUTPUT);
  digitalWrite(12, HIGH);
  digitalWrite(13, HIGH);
  digitalWrite(14, HIGH);
  digitalWrite(15, HIGH);
  digitalWrite(16, HIGH);
  digitalWrite(17, HIGH);
  Serial.begin (9600);
  analogWrite (11, greenA);
    analogWrite (10, redA);
    analogWrite (9, blueA);
    analogWrite (8, greenB);
    analogWrite (7, redB);
    analogWrite (6, blueB);
    analogWrite (5, greenC);
    analogWrite (4, redC);
    analogWrite (3, blueC);
    
    gain = 0;
  
}
void loop ()
{
    while (Serial.available()>0) 
  { String flagmode = Serial.readStringUntil(',');
    if (flagmode=="B")
    {   
    redA=Serial.parseInt();
    greenA=Serial.parseInt();
    blueA=Serial.parseInt();
    redB=Serial.parseInt();
    greenB=Serial.parseInt();
    blueB=Serial.parseInt();
    redC=Serial.parseInt();
    greenC=Serial.parseInt();
    blueC=Serial.parseInt();
    digitalWrite(11, LOW); 
    digitalWrite(10, LOW); 
    digitalWrite(9, LOW);
    digitalWrite(8, LOW); 
    digitalWrite(7, LOW); 
    digitalWrite(6, LOW);
    digitalWrite(5, LOW); 
    digitalWrite(4, LOW); 
    digitalWrite(3, LOW);
    delay(1);
    analogWrite (11, greenA);
    analogWrite (10, redA);
    analogWrite (9, blueA);
    analogWrite (8, greenB);
    analogWrite (7, redB);
    analogWrite (6, blueB);
    analogWrite (5, greenC);
    analogWrite (4, redC);
    analogWrite (3, blueC);
  }  
 else if (flagmode=="A")
 { 
/////////////////////////////////////////  
  digitalWrite(12, LOW);
  digitalWrite(13, HIGH);
  digitalWrite(14, HIGH);
  digitalWrite(15, HIGH);
  digitalWrite(16, HIGH);
  digitalWrite(17, HIGH);  
light.begin();
light.setTiming(gain,time,ms);
light.setPowerUp();
delay(ms);

  unsigned int data0, data1;
  
  if (light.getData(data0,data1))
  {
  
   
    
    boolean good; 
   
    good = light.getLux(gain,ms,data0,data1,luxA);
   
    
    
  }
/////////////////////////////////////////  
  digitalWrite(12, HIGH);
  digitalWrite(13, LOW);
  digitalWrite(14, HIGH);
  digitalWrite(15, HIGH);
  digitalWrite(16, HIGH);
  digitalWrite(17, HIGH);  
light.begin();
light.setTiming(gain,time,ms);
light.setPowerUp();
delay(ms);

  data0, data1;
  
  if (light.getData(data0,data1))
  {
  
   
    
    boolean good; 
   
    good = light.getLux(gain,ms,data0,data1,luxB);
   
    
    
  }
/////////////////////////////////////////  
  digitalWrite(12, HIGH);
  digitalWrite(13, HIGH);
  digitalWrite(14, LOW);
  digitalWrite(15, HIGH);
  digitalWrite(16, HIGH);
  digitalWrite(17, HIGH);  
light.begin();
light.setTiming(gain,time,ms);
light.setPowerUp();
delay(ms);

  data0, data1;
  
  if (light.getData(data0,data1))
  {
  
   
    
    boolean good; 
   
    good = light.getLux(gain,ms,data0,data1,luxC);
   
    
    
  }
/////////////////////////////////////////  
  digitalWrite(12, HIGH);
  digitalWrite(13, HIGH);
  digitalWrite(14, HIGH);
  digitalWrite(15, LOW);
  digitalWrite(16, HIGH);
  digitalWrite(17, HIGH);  
light.begin();
light.setTiming(gain,time,ms);
light.setPowerUp();
delay(ms);

  data0, data1;
  
  if (light.getData(data0,data1))
  {
  
   
   
    boolean good; 
   
    good = light.getLux(gain,ms,data0,data1,luxD);
   
    
    
  }
/////////////////////////////////////////  
  digitalWrite(12, HIGH);
  digitalWrite(13, HIGH);
  digitalWrite(14, HIGH);
  digitalWrite(15, HIGH);
  digitalWrite(16, LOW);
  digitalWrite(17, HIGH);  
light.begin();
light.setTiming(gain,time,ms);
light.setPowerUp();
delay(ms);

  data0, data1;
  
  if (light.getData(data0,data1))
  {
  
   
    
    boolean good; 
   
    good = light.getLux(gain,ms,data0,data1,luxE);
   
    
    
  }
/////////////////////////////////////////  
  digitalWrite(12, HIGH);
  digitalWrite(13, HIGH);
  digitalWrite(14, HIGH);
  digitalWrite(15, HIGH);
  digitalWrite(16, HIGH);
  digitalWrite(17, LOW);  
light.begin();
light.setTiming(gain,time,ms);
light.setPowerUp();
delay(ms);

  data0, data1;
  
  if (light.getData(data0,data1))
  {
  
   
    boolean good; 
   
    good = light.getLux(gain,ms,data0,data1,luxF);
   
    
    
  }
///////////////////////////////////////
Serial.print(luxA);  
 Serial.print(",");
 Serial.print(luxB);  
 Serial.print(",");
 Serial.print(luxC);  
 Serial.print(",");   
 Serial.print(luxD);  
 Serial.print(",");   
 Serial.print(luxE);  
 Serial.print(",");   
 Serial.print(luxF);  
 Serial.println(","); 
  }
 }
}
