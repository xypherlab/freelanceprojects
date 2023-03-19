#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
RF24 radio(7, 8); // CE, CSN         
const byte addresses[][6] = {"00002", "00001"};
String data;  

const int sensorPin = A0; //Defines the pin that the anemometer output is connected to
int sensorValue = 0; //Variable stores the value direct from the analog pin
float sensorVoltage = 0; //Variable that stores the voltage (in Volts) from the anemometer being sent to the analog pin
float windSpeed = 0; // Wind speed in meters per second (m/s)
 
float voltageConversionConstant = .004882814; //This constant maps the value provided from the analog read function, which ranges from 0 to 1023, to actual voltage, which ranges from 0V to 5V
int sensorDelay = 1000; //Delay between sensor readings, measured in milliseconds (ms)
 
//Anemometer Technical Variables
//The following variables correspond to the anemometer sold by Adafruit, but could be modified to fit other anemometers.
 
float voltageMin = .4; // Mininum output voltage from anemometer in mV.
float windSpeedMin = 0; // Wind speed in meters/sec corresponding to minimum voltage
 
float voltageMax = 2.0; // Maximum output voltage from anemometer in mV.
float windSpeedMax = 32; // Wind speed in meters/sec corresponding to maximum voltage
 

void setup() {
  Serial.begin(9600);
 radio.begin();
  radio.openWritingPipe(addresses[1]); // 00002
radio.openReadingPipe(1, addresses[0]); // 00001
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();
  pinMode(3, OUTPUT);
pinMode(4, OUTPUT);
pinMode(5, OUTPUT);
pinMode(6, OUTPUT);
pinMode(9, OUTPUT);
pinMode(10, OUTPUT);

digitalWrite(3, LOW);
digitalWrite(4, LOW);
digitalWrite(5, LOW);
digitalWrite(6, LOW);
digitalWrite(9, LOW);
digitalWrite(10, LOW);
}
void loop()
{


if (radio.available())           
{
char text[32] = "";                 
radio.read(&text, sizeof(text));    
data=String(text);
String response = getValue(data, ',', 0);
Serial.println(data);
String delaytime = getValue(data, ',', 1);

int timedelay=delaytime.toInt();
Serial.println(timedelay);
if (response=="RA")
{ 
digitalWrite(3, HIGH);
  Serial.println("Relay A On");
}
else if (response=="RB")
{ 
  digitalWrite(4, HIGH);
  Serial.println("Relay B On");
}
else if (response=="RC")
{ 
  digitalWrite(5, HIGH);
  Serial.println("Relay C On");
}
else if (response=="RD")
{ 
  digitalWrite(6, HIGH);
  Serial.println("Relay D On");
}
else if (response=="RE")
{ 
  digitalWrite(9, HIGH);
  Serial.println("Relay E On");
}
else if (response=="RF")
{ 
  digitalWrite(10, HIGH);
  Serial.println("Relay F On");
}
else if (response=="QA")
{ 
digitalWrite(3, LOW);
  Serial.println("Relay A Off");
}
else if (response=="QB")
{ 
  digitalWrite(4, LOW);
  Serial.println("Relay B Off");
}
else if (response=="QC")
{ 
  digitalWrite(5, LOW);
  Serial.println("Relay C Off");
}
else if (response=="QD")
{ 
  digitalWrite(6, LOW);
  Serial.println("Relay D Off");
}
else if (response=="QE")
{ 
  digitalWrite(9, LOW);
  Serial.println("Relay E Off");
}
else if (response=="QF")
{ 
  digitalWrite(10, LOW);
  Serial.println("Relay F Off");
}
 
}

sensorValue = analogRead(sensorPin); //Get a value between 0 and 1023 from the analog pin connected to the anemometer
 
sensorVoltage = sensorValue * voltageConversionConstant; //Convert sensor value to actual voltage
 
//Convert voltage value to wind speed using range of max and min voltages and wind speed for the anemometer
if (sensorVoltage <= voltageMin){
 windSpeed = 0; //Check if voltage is below minimum value. If so, set wind speed to zero.
}else {
  windSpeed = (sensorVoltage - voltageMin)*windSpeedMax/(voltageMax - voltageMin); //For voltages above minimum value, use the linear relationship to calculate wind speed.
}
 
 //Print voltage and windspeed to serial
  Serial.print("Voltage: ");
  Serial.print(sensorVoltage);
  Serial.print("\t"); 
  Serial.print("Wind speed: ");
  Serial.println(windSpeed); 

  
String delaydata="F,"+String(windSpeed)+",";
int delaydata_len = delaydata.length() + 1; 
char text[delaydata_len];
delaydata.toCharArray(text, delaydata_len); 

radio.stopListening();
radio.write(&text, sizeof(text));
delay(5);
radio.startListening();
  
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
