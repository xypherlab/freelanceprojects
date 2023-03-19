volatile int coins = 0;
volatile int bills = 0;
volatile int credit = 0;
const int lockerA =  14;
const int lockerB =  15;
#include <SoftwareSerial.h>
SoftwareSerial sim(8, 9);
int _timeout;
String _buffer;
String number;
String lockerid;
String contactno;
void setup()
{ Serial.begin(9600);

pinMode (2,INPUT_PULLUP);
  pinMode (3,INPUT_PULLUP);

   //delay(7000); 
  Serial.begin(9600);
  _buffer.reserve(50);
  sim.begin(9600);
  delay(1000);
 pinMode(lockerA, OUTPUT);
  pinMode(lockerB, OUTPUT);
    digitalWrite(lockerA, HIGH);
  digitalWrite(lockerB, HIGH);
}



void loop()
{String flagmode = Serial.readStringUntil(',');
 
  if (flagmode=="A")
{
  digitalWrite(lockerA, LOW);
  delay(15000);
  digitalWrite(lockerA, HIGH);
}
  else if (flagmode=="B")
  {digitalWrite(lockerB, LOW);
  delay(15000);
  digitalWrite(lockerB, HIGH);
    
  }
else if (flagmode=="C")
  {
  bills=0;
  coins=0;
  }
else if (flagmode=="D")
  {  
 number = Serial.readStringUntil(',');
 //Serial.println(number);
  SendMessage();
  delay(3000);
   bills=0;
  coins=0;   
  }
  else if (flagmode=="G")
  {  
 number = Serial.readStringUntil(',');
 //Serial.println(number);
  SendMessageA();
  delay(3000);
   bills=0;
  coins=0;
  digitalWrite(lockerA, LOW);
  delay(15000);
  digitalWrite(lockerA, HIGH);   
  }
   else if (flagmode=="H")
  {  
 number = Serial.readStringUntil(',');
 //Serial.println(number);
  SendMessageA();
  delay(3000);
   bills=0;
  coins=0;
  digitalWrite(lockerB, LOW);
  delay(15000);
  digitalWrite(lockerB, HIGH);   
  }
 else if (flagmode=="F")
  {  
 number = Serial.readStringUntil(',');
 //Serial.println(number);
  lockerid = Serial.readStringUntil(',');
 //Serial.println(lockerid);
  contactno = Serial.readStringUntil(',');
 //Serial.println(contactno);
  SendMessageB();
  delay(3000);
   bills=0;
  coins=0;   
  }
 credit=bills+coins;
 Serial.print(credit);
 Serial.println(","); 

}
void SendMessageB()
{
  sim.println("AT+CMGF=1");  
  delay(1000);
  sim.println("AT+CMGS=\"" + number + "\"\r"); 
  delay(1000);
  String SMS = lockerid+" exceed its availed service. Phone Number: "+contactno;
  sim.println(SMS);
  delay(100);
  sim.println((char)26);
  delay(1000);
  _buffer = _readSerial();
}

void SendMessage()
{
  sim.println("AT+CMGF=1");  
  delay(1000);
  sim.println("AT+CMGS=\"" + number + "\"\r"); 
  delay(1000);
  String SMS = "Thank you for using our service. You have 1 hour left on your rented locker.";
  sim.println(SMS);
  delay(100);
  sim.println((char)26);
  delay(1000);
  _buffer = _readSerial();
}

void SendMessageA()
{
  sim.println("AT+CMGF=1");  
  delay(1000);
  sim.println("AT+CMGS=\"" + number + "\"\r"); 
  delay(1000);
  String SMS = "We are not liable for any loss or damage on your item.";
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
