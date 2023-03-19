#define USE_ARDUINO_INTERRUPTS true    // Set-up low-level interrupts for most acurate BPM math.
#include <PulseSensorPlayground.h>     // Includes the PulseSensorPlayground Library.   

//  Variables
const int PulseWire = 0;       // PulseSensor PURPLE WIRE connected to ANALOG PIN 0
const int LED13 = 17;          // The on-board Arduino LED, close to PIN 13.
int Threshold = 550;           // Determine which Signal to "count as a beat" and which to ignore.
                               // Use the "Gettting Started Project" to fine-tune Threshold Value beyond default setting.
                               // Otherwise leave the default "550" value. 
                               
PulseSensorPlayground pulseSensor;  // Creates an instance of the PulseSensorPlayground object called "pulseSensor"

#include <SoftwareSerial.h>
#include <OneWire.h>
#define RX 4
#define TX 3
String AP = "viva";
String PASS = "mapuauniv";
String HOST = "192.168.43.53";//.53
String PORT = "80";
int countTrueCommand;
int countTimeCommand;
boolean found = false;
int valSensor = 1;
SoftwareSerial esp8266(RX, TX);
int flag=0;
unsigned long T1;
unsigned long T2;
unsigned long Time;
unsigned long a;
unsigned long b;
#include <OneWire.h>
int rrpin = 15; 

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
  Serial.begin(115200);
  
  // Configure the PulseSensor object, by assigning our variables to it. 
  pulseSensor.analogInput(PulseWire);   
  pulseSensor.blinkOnPulse(LED13);       //auto-magically blink Arduino's LED with heartbeat.
  pulseSensor.setThreshold(Threshold);   

  // Double-check the "pulseSensor" object was created and "began" seeing a signal. 
   if (pulseSensor.begin()) {
    Serial.println("");  //This prints one time at Arduino power-up,  or on Arduino reset.  
  }
  esp8266.begin(115200);
  pinMode(ledApin, OUTPUT);
  pinMode(ledBpin, OUTPUT);
  pinMode(ledCpin, OUTPUT);
  pinMode(ledDpin, OUTPUT);
  pinMode(pbpin, INPUT_PULLUP);
  pinMode(rrpin, INPUT_PULLUP);

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

  
  sendCommand("AT", 5, "OK");
  sendCommand("AT+CWMODE=3", 5, "OK");
  sendCommand("AT+CWJAP=\"" + AP + "\",\"" + PASS + "\"", 20, "OK");
  sendCommand("AT+CIPMUX=1", 5, "OK");
  sendCommand("AT+CIPSTART=0,\"TCP\",\"" + HOST + "\"," + PORT, 15, "OK");
  T1 = millis();
}

void loop() {
  float temperature = getTemp();
  Serial.println(temperature);
  unsigned long a = 0;
while (a==0)
{  
int sensorVal = digitalRead(rrpin);
if (sensorVal == LOW and flag == 0)
    {Serial.print("Low: "); Serial.println(analogRead(A0));
      flag = 1;
      delay(20);
    }
     else if (sensorVal == HIGH and flag == 1)
    {Serial.print("High: "); Serial.println(analogRead(A0));
      T1 = millis();
      flag = 2;
      delay(20);
      
    }
    else if (sensorVal == LOW and flag == 2)
    { Serial.print("Low: "); Serial.println(analogRead(A0));
     
      flag = 3;
      delay(20);
    }
    else if (sensorVal == HIGH and flag == 3)
    { Serial.print("High: "); Serial.println(analogRead(A0));
      T2 = millis();
      unsigned long Time = T2 - T1;
      unsigned long respRate = 60000L;
      respRate = respRate / Time;
      Serial.print("RR = ");
      Serial.println(respRate);
      flag = 0;
      delay(20);
      a = respRate*2;
      //delay(3000);

    }
}   
  /*i=0;
 while (i!=5)
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
  }*/
  
  //b=60;
int myBPM = pulseSensor.getBeatsPerMinute();  // Calls function on our pulseSensor object that returns BPM as an "int".
                                               // "myBPM" hold this BPM value now. 

if (pulseSensor.sawStartOfBeat()) {            // Constantly test to see if "a beat happened". 
 Serial.println(myBPM);                        // Print the value inside of myBPM.
 b=myBPM; 
}

  delay(20);                    // considered best practice in a simple sketch.


if (a<10 or a>25)
{
digitalWrite(ledBpin, HIGH);
digitalWrite(buzzerpin, HIGH);
delay(3000);
digitalWrite(buzzerpin, LOW);
digitalWrite(ledBpin, LOW);
rrwarn=1;  
}
if (b<70 or b>120)
{
digitalWrite(ledCpin, HIGH);  
digitalWrite(buzzerpin, HIGH);
delay(3000);
digitalWrite(buzzerpin, LOW);
digitalWrite(ledCpin, LOW);
hrwarn=1;
}
if (temperature>37.2)
{
digitalWrite(ledDpin, HIGH);
digitalWrite(buzzerpin, HIGH);
delay(3000);
digitalWrite(buzzerpin, LOW);
digitalWrite(ledDpin, LOW);
tmpwarn=1;  
}
pbstate = digitalRead(pbpin);
if (pbstate==LOW)
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

  //sendCommand("AT+CIPSTART=0,\"TCP\",\""+ HOST +"\","+ PORT,15,"OK");

  sendCommand("AT+CIPSEND=0," + String(getData.length() + 4), 4, ">");
  esp8266.println(getData); delay(1500); countTrueCommand++;
  //sendCommand("AT+CIPCLOSE=0",5,"OK");
}




void sendCommand(String command, int maxTime, char readReplay[]) {
  Serial.print(countTrueCommand);
  Serial.print(". at command => ");
  Serial.print(command);
  Serial.print(" ");
  while (countTimeCommand < (maxTime * 1))
  {
    esp8266.println(command);//at+cipsend
    if (esp8266.find(readReplay)) //ok
    {
      found = true;
      break;
    }

    countTimeCommand++;
  }

  if (found == true)
  {
    Serial.println("OK");
    countTrueCommand++;
    countTimeCommand = 0;
  }

  if (found == false)
  {
    Serial.println("Fail");
    countTrueCommand = 0;
    countTimeCommand = 0;
  }

  found = false;
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
