#include <SoftwareSerial.h>
int valSensor = 1;

static const int RXPin = 2, TXPin = 3;
static const uint32_t GPSBaud = 9600;


SoftwareSerial ss(RXPin, TXPin);
int flag=0;
unsigned long time_now = 0;
SoftwareSerial wifiSerial(8, 9);      
String apiKey = "6Z8OK3E65MBF1QUG"; 
String ssid="hayahay";   
String password ="qwerty13";  
bool DEBUG = true;  
int responseTime = 200; 
const unsigned int TRIG_PINA=14;
const unsigned int ECHO_PINA=4;
const unsigned int TRIG_PINB=10;
const unsigned int ECHO_PINB=11;
float intervalA; 
float intervalB;
int vibA;
int vibB;  
int ledStateA = LOW;
int ledStateB = LOW;
  
String latitude;
String longitude;
void showResponse(int waitTime){
    long t=millis();
    char c;
    while (t+waitTime>millis()){
      if (wifiSerial.available()){
        c=wifiSerial.read();
        if (DEBUG) Serial.print(c);
      }
    }
                   
}

boolean thingSpeakWrite(float value1, float value2){
  String cmd = "AT+CIPSTART=\"TCP\",\"";                  // TCP connection
  cmd += "184.106.153.149";                               // api.thingspeak.com
  cmd += "\",80";
  wifiSerial.println(cmd);
  if (DEBUG) Serial.println(cmd);
  if(wifiSerial.find("Error")){
    if (DEBUG) Serial.println("AT+CIPSTART error");
    return false;
  }
  
  
  String getStr = "GET /update?api_key=";   // prepare GET string
  getStr += apiKey;
  
  getStr +="&field1=";
  getStr += String(value1);
  getStr +="&field2=";
  getStr += String(value2);
  // getStr +="&field3=";
  // getStr += String(value3);
  // ...
  getStr += "\r\n\r\n";

  // send data length
  cmd = "AT+CIPSEND=";
  cmd += String(getStr.length());
  Serial.println(cmd);
  wifiSerial.println(cmd);
  if (DEBUG)  Serial.println(cmd);
  
  delay(100);
  if(wifiSerial.find(">")){
    wifiSerial.print(getStr);
    if (DEBUG)  Serial.print(getStr);
  }
  else{
    wifiSerial.println("AT+CIPCLOSE");
    // alert user
    if (DEBUG)   Serial.println("AT+CIPCLOSE");
    return false;
  }
  return true;
}


void setup()
{
pinMode(TRIG_PINA, OUTPUT);
  pinMode(ECHO_PINA, INPUT);
   pinMode(TRIG_PINB, OUTPUT);
  pinMode(ECHO_PINB, INPUT);

  Serial.begin(115200);
  ss.begin(GPSBaud);
  wifiSerial.begin(115200);
  wifiSerial.listen();
  wifiSerial.println("AT+CWMODE=1");   // set esp8266 as client
  showResponse(1000);

  wifiSerial.println("AT+CWJAP=\""+ssid+"\",\""+password+"\"");  // set your home router SSID and password
  showResponse(5000);

   if (DEBUG)  Serial.println("Setup completed");
   
  
 

}


void loop()
{
 
  digitalWrite(TRIG_PINA, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PINA, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PINA, LOW);
  

 const unsigned long durationA= pulseIn(ECHO_PINA, HIGH);
 int distanceA= durationA/29/2;
 Serial.print("distanceA: ");
 Serial.println(distanceA);
 
 digitalWrite(TRIG_PINB, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PINB, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PINB, LOW);
  

 const unsigned long durationB= pulseIn(ECHO_PINB, HIGH);
 int distanceB= durationB/29/2;
 Serial.print("distanceB: ");
 Serial.println(distanceB);
if (distanceA<400)
{
  vibA=(float(400-distanceA)/float(400))*255;
  Serial.println(vibA);
  analogWrite(6,vibA);
}
else if (distanceA>=400)
{
  analogWrite(6,0);
}

if (distanceB<400)
{
  vibB=(float(400-distanceB)/float(400))*255;
  Serial.println(vibB);
  analogWrite(5,vibB);
}
else if (distanceB>=400)
{
  intervalB=0;
  analogWrite(5,intervalB);
}
  
 ss.listen();
 delay(1000);
  while (ss.available() > 0 && flag==0){
  String dump=ss.readStringUntil(',');
  latitude = ss.readStringUntil(',');
  longitude = ss.readStringUntil(',');
 
  Serial.println(latitude);
  Serial.println(longitude);
  flag=1;

}
float latitudes=latitude.toFloat();
float longitudes=longitude.toFloat();
wifiSerial.listen(); 

if(millis() > time_now + 15000){
        time_now = millis();
        thingSpeakWrite(latitudes,longitudes);    
    }


    
flag=0;
}





int getSensorData(){
  return random(1000); // Replace with 
}



