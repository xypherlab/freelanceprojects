#include <SoftwareSerial.h>
#include <OneWire.h>
#define RX 4
#define TX 3
String AP = "viva";
String PASS = "mapuauniv";
String HOST = "192.168.43.214";
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
//Heart Rate
int pulsePin = A1;                 
volatile int BPM;                   
volatile int Signal;                
volatile int IBI = 600;              
volatile boolean Pulse = false;      
volatile boolean QS = false;        
static boolean serialVisual = true;   // Set to 'false' by Default.  Re-set to 'true' to see Arduino Serial Monitor ASCII Visual Pulse 

volatile int rate[10];                    
volatile unsigned long sampleCounter = 0; 
volatile unsigned long lastBeatTime = 0;  
volatile int P = 512;                     
volatile int T = 512;                     
volatile int thresh = 525;                
volatile int amp = 100;                   
volatile boolean firstBeat = true;        
volatile boolean secondBeat = false;
//int blinkPin = 13; 
//
void setup() {
    interruptSetup();
  //pinMode(blinkPin,OUTPUT); 

  Serial.begin(9600);
  esp8266.begin(115200);
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

  
  sendCommand("AT", 5, "OK");
  sendCommand("AT+CWMODE=3", 5, "OK");
  sendCommand("AT+CWJAP=\"" + AP + "\",\"" + PASS + "\"", 20, "OK");
  sendCommand("AT+CIPMUX=1", 5, "OK");
  sendCommand("AT+CIPSTART=0,\"TCP\",\"" + HOST + "\"," + PORT, 15, "OK");
  T1 = millis();
}
//Interrupt//
void interruptSetup()
{     
  // Initializes Timer2 to throw an interrupt every 2mS.
  TCCR2A = 0x02;     // DISABLE PWM ON DIGITAL PINS 3 AND 11, AND GO INTO CTC MODE
  TCCR2B = 0x06;     // DON'T FORCE COMPARE, 256 PRESCALER 
  OCR2A = 0X7C;      // SET THE TOP OF THE COUNT TO 124 FOR 500Hz SAMPLE RATE
  TIMSK2 = 0x02;     // ENABLE INTERRUPT ON MATCH BETWEEN TIMER2 AND OCR2A
  sei();             // MAKE SURE GLOBAL INTERRUPTS ARE ENABLED      
} 



ISR(TIMER2_COMPA_vect) //triggered when Timer2 counts to 124
{  
  cli();                                      // disable interrupts while we do this
  Signal = analogRead(pulsePin);              // read the Pulse Sensor 
  sampleCounter += 2;                         // keep track of the time in mS with this variable
  int N = sampleCounter - lastBeatTime;       // monitor the time since the last beat to avoid noise
                                              //  find the peak and trough of the pulse wave
  if(Signal < thresh && N > (IBI/5)*3) // avoid dichrotic noise by waiting 3/5 of last IBI
    {      
      if (Signal < T) // T is the trough
      {                        
        T = Signal; // keep track of lowest point in pulse wave 
      }
    }

  if(Signal > thresh && Signal > P)
    {          // thresh condition helps avoid noise
     
      P = Signal;                             // P is the peak
    }                                        // keep track of highest point in pulse wave

  //  NOW IT'S TIME TO LOOK FOR THE HEART BEAT
  // signal surges up in value every time there is a pulse
  if (N > 250)
  {                                   // avoid high frequency noise
    if ( (Signal > thresh) && (Pulse == false) && (N > (IBI/5)*3) )
      { //digitalWrite(blinkPin,HIGH);       
        Pulse = true;                               // set the Pulse flag when we think there is a pulse
        IBI = sampleCounter - lastBeatTime;         // measure time between beats in mS
        lastBeatTime = sampleCounter;               // keep track of time for next pulse
  
        if(secondBeat)
        {                        // if this is the second beat, if secondBeat == TRUE
          secondBeat = false;                  // clear secondBeat flag
          for(int i=0; i<=9; i++) // seed the running total to get a realisitic BPM at startup
          {             
            rate[i] = IBI;                      
          }
        }
  
        if(firstBeat) // if it's the first time we found a beat, if firstBeat == TRUE
        {                         
          firstBeat = false;                   // clear firstBeat flag
          secondBeat = true;                   // set the second beat flag
          sei();                               // enable interrupts again
          return;                              // IBI value is unreliable so discard it
        }   
      // keep a running total of the last 10 IBI values
      word runningTotal = 0;                  // clear the runningTotal variable    

      for(int i=0; i<=8; i++)
        {                // shift data in the rate array
          rate[i] = rate[i+1];                  // and drop the oldest IBI value 
          runningTotal += rate[i];              // add up the 9 oldest IBI values
        }

      rate[9] = IBI;                          // add the latest IBI to the rate array
      runningTotal += rate[9];                // add the latest IBI to runningTotal
      runningTotal /= 10;                     // average the last 10 IBI values 
      BPM = 60000/runningTotal;               // how many beats can fit into a minute? that's BPM!
      QS = true;                              // set Quantified Self flag 
      // QS FLAG IS NOT CLEARED INSIDE THIS ISR
    }                       
  }

  if (Signal < thresh && Pulse == true)
    {   // when the values are going down, the beat is over
      //digitalWrite(blinkPin,LOW);
      Pulse = false;                         // reset the Pulse flag so we can do it again
      amp = P - T;                           // get amplitude of the pulse wave
      thresh = amp/2 + T;                    // set thresh at 50% of the amplitude
      P = thresh;                            // reset these for next time
      T = thresh;
    }

  if (N > 2500)
    {                           // if 2.5 seconds go by without a beat
      thresh = 512;                          // set thresh default
      P = 512;                               // set P default
      T = 512;                               // set T default
      lastBeatTime = sampleCounter;          // bring the lastBeatTime up to date        
      firstBeat = true;                      // set these to avoid noise
      secondBeat = false;                    // when we get the heartbeat back
    }

  sei();                                   // enable interrupts when youre done!
}// end isr




/////////////
void loop() {
  float temperature = getTemp();
  Serial.println(temperature);
  unsigned long a = 0;
  digitalWrite(ledDpin, HIGH);
  //while (a>100 || a<10)
  //{
  i=0;
  while (i!=5)
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
   digitalWrite(ledBpin, HIGH);
   if (QS == true) 
    {             
     Serial.print("BPM: ");
     Serial.println(BPM);
     
      b=BPM; 
      QS = false; 
    }
     
  delay(20);
  //b=60;
 
/*if (a<10 or a>22 and b<80 or b>120 or temperature<37.2)
{
  
  digitalWrite(buzzerpin, HIGH);

}*/
digitalWrite(ledCpin, HIGH);

delay(2000);
digitalWrite(ledBpin, LOW);
digitalWrite(ledCpin, LOW);
digitalWrite(ledDpin, LOW);

if (a<10 or a>22)
{
digitalWrite(ledBpin, HIGH);
digitalWrite(buzzerpin, HIGH);
rrwarn=1;  
}
if (b<80 or b>120)
{
digitalWrite(ledCpin, HIGH);  
digitalWrite(buzzerpin, HIGH);
hrwarn=1;
}
if (temperature>37.2)
{
digitalWrite(ledDpin, HIGH);
digitalWrite(buzzerpin, HIGH);
tmpwarn=1;  
}
delay(3000);
digitalWrite(buzzerpin, LOW);
digitalWrite(ledBpin, LOW);
digitalWrite(ledCpin, LOW); 
digitalWrite(ledDpin, LOW);

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
