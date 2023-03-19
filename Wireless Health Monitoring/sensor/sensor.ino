#include <OneWire.h>

int valSensor = 1;
int Pulse = A0;
int flag=0;
unsigned long T1;
unsigned long T2;
unsigned long Time;
unsigned long a;
unsigned long b;

int DS18S20_Pin = 5;
OneWire ds(DS18S20_Pin);
const int pbpin = 13;
const int buzzerpin =  16;
const int ledApin = 9;
const int ledBpin =  10;
const int ledCpin = 11;
const int ledDpin =  12;
int pbstate = 0;
int i;
int hrwarn=0;
int rrwarn=0;
int tmpwarn=0;
void setup() {
  Serial.begin(9600);
  pinMode(ledApin, OUTPUT);
  pinMode(ledBpin, OUTPUT);
  pinMode(ledCpin, OUTPUT);
  pinMode(ledDpin, OUTPUT);
  pinMode(pbpin, INPUT_PULLUP);
  pinMode(buzzerpin, OUTPUT);
  digitalWrite(ledApin, HIGH);
  digitalWrite(ledBpin, HIGH);
  digitalWrite(ledCpin, HIGH);
  digitalWrite(ledDpin, HIGH);
  digitalWrite(buzzerpin, HIGH);
  delay(3000);
  //digitalWrite(ledApin, LOW);
  digitalWrite(ledBpin, LOW);
  digitalWrite(ledCpin, LOW);
  digitalWrite(ledDpin, LOW);
  digitalWrite(buzzerpin, LOW);

  T1 = millis();
}

void loop() {
  float temperature = getTemp();
  Serial.println(temperature);
  unsigned long a = 0;
  //while (a>100 || a<10)
  //{
  i=0;
  while (i!=1)
  {
  while (a == 0)
  {
    Serial.println(analogRead(A0));
    if (analogRead(A0) <560 and flag == 0)
    {Serial.print("Low: "); Serial.println(analogRead(A0));
      flag = 1;
      
    }
     else if (analogRead(A0) >=570 and flag == 1)
    {Serial.print("High: "); Serial.println(analogRead(A0));
       T1 = millis();
      flag = 2;
      
    }
    else if (analogRead(A0) < 560 and flag == 2)
    { Serial.print("Low: "); Serial.println(analogRead(A0));
     
      flag = 3;
    }
    else if (analogRead(A0) >= 570 and flag == 3)
    { Serial.print("High: "); Serial.println(analogRead(A0));
      T2 = millis();
      Time = T2 - T1;
      unsigned long respRate = 60000L;
      respRate = respRate / Time;
      Serial.print("RR = ");
      Serial.println(respRate);
      flag = 0;

      a = respRate;
      //delay(3000);

    }
  }
  i=i+1;
  }
  i=0;
 while (i!=1)
  {
  while (digitalRead(Pulse) == HIGH);
  while (digitalRead(Pulse) == LOW);
  int T1 = millis();
while (digitalRead(Pulse) == HIGH);
  while (digitalRead(Pulse) == LOW);
  int T2 = millis();
  int Time = T2 - T1;
  unsigned long HeartRate = 60000L;
  HeartRate = HeartRate / Time;
  Serial.print("BPM = ");
  Serial.println(HeartRate);
  b = HeartRate;
  i=i+1;
  }
  
  //b=60;
 


if (a<10 or a>22)
{
digitalWrite(ledBpin, HIGH);
digitalWrite(buzzerpin, HIGH);
rrwarn=1;
Serial.println("###########################RR");  
}
if (b<80 or b>120)
{
digitalWrite(ledCpin, HIGH);  
digitalWrite(buzzerpin, HIGH);
hrwarn=1;
Serial.println("###########################HR");
}
if (temperature>37.2)
{
digitalWrite(ledDpin, HIGH);
digitalWrite(buzzerpin, HIGH);
tmpwarn=1;
cSerial.println("###########################Temp");  
}
pbstate = digitalRead(pbpin);
if (pbstate==HIGH)
{ digitalWrite(buzzerpin, LOW);

  digitalWrite(ledBpin, LOW);
  digitalWrite(ledCpin, LOW); 
  digitalWrite(ledDpin, LOW);
}
 String getData = "0," + String(a) + "," + String(temperature) + "," + String(b) + ","+ String(rrwarn) + ","+ String(hrwarn) + ","+ String(tmpwarn) + ",";
 hrwarn=0;
 rrwarn=0;
 tmpwarn=0;
  Serial.print("Data: ");
  Serial.println(getData);

}





float getTemp() {
  //returns the temperature from one DS18S20 in DEG Celsius

  byte data[12];
  byte addr[8];

  if ( !ds.search(addr)) {
    //no more sensors on chain, reset search
    ds.reset_search();
    return -1000;
  }

  if ( OneWire::crc8( addr, 7) != addr[7]) {
    Serial.println("CRC is not valid!");
    return -1000;
  }

  if ( addr[0] != 0x10 && addr[0] != 0x28) {
    Serial.print("Device is not recognized");
    return -1000;
  }

  ds.reset();
  ds.select(addr);
  ds.write(0x44, 1); // start conversion, with parasite power on at the end

  byte present = ds.reset();
  ds.select(addr);
  ds.write(0xBE); // Read Scratchpad


  for (int i = 0; i < 9; i++) { // we need 9 bytes
    data[i] = ds.read();
  }

  ds.reset_search();

  byte MSB = data[1];
  byte LSB = data[0];

  float tempRead = ((MSB << 8) | LSB); //using two's compliment
  float TemperatureSum = tempRead / 16;

  return TemperatureSum;

}
