unsigned char carrierFreq = 0; //default
unsigned char period = 0; //calculated once for each signal sent in initSoftPWM
unsigned char periodHigh = 0; //calculated once for each signal sent in initSoftPWM
unsigned char periodLow = 0; //calculated once for each signal sent in initSoftPWM



unsigned long sigTime = 0; //used in mark & space functions to keep track of time
unsigned long sigStart = 0; //used to calculate correct length of existing signal, to handle some repeats


#define NEC_BIT_COUNT 32

void setup() {
  Serial.begin(57600);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
}

void loop() {
/*
#2 - IR Receiver 
#3 - Ok
#4 - Ok
#5 - IR Receiver
#6 - IR Receiver
#7 - Ok
#8 - IR Receiver
#9 - Yellow LED
#10 - Ok
#11 - Yellow LED
#12 - Ok
#13 - Ok

*/

/*
#2 - Ok
#3 -
#4 - 
#5 - 
#6 - 
#7 - 
#8 - 
#9 - 
#10 - 
#11 - 
#12 - 
#13 - 

*/

 
  Serial.println(F("Sending NEC_HEX_VALUE @ 38kHz"));
  sendHexNEC(0x00DF22DDUL, NEC_BIT_COUNT, 1, 38,2);
  delay(10);
  Serial.println(F("Sending NEC_HEX_VALUE @ 38kHz"));
  sendHexNEC(0x10DF22DDUL, NEC_BIT_COUNT, 1, 38,3);
  delay(10); 

  Serial.println(F("Sending NEC_HEX_VALUE @ 38kHz"));
  sendHexNEC(0x20DF22DDUL, NEC_BIT_COUNT, 1, 38,4);
  delay(10); 
  Serial.println(F("Sending NEC_HEX_VALUE @ 38kHz"));
  sendHexNEC(0x30DF22DDUL, NEC_BIT_COUNT, 1, 38,5);
  delay(10); 

  Serial.println(F("Sending NEC_HEX_VALUE @ 38kHz"));
  sendHexNEC(0x40DF22DDUL, NEC_BIT_COUNT, 1, 38,6);
  delay(10); 
  Serial.println(F("Sending NEC_HEX_VALUE @ 38kHz"));
  sendHexNEC(0x50DF22DDUL, NEC_BIT_COUNT, 1, 38,7);
  delay(10);

  Serial.println(F("Sending NEC_HEX_VALUE @ 38kHz"));
  sendHexNEC(0x60DF22DDUL, NEC_BIT_COUNT, 1, 38,8);
  delay(10); 
  Serial.println(F("Sending NEC_HEX_VALUE @ 38kHz"));
  sendHexNEC(0x70DF22DDUL, NEC_BIT_COUNT, 1, 38,9);
  delay(10); 

  Serial.println(F("Sending NEC_HEX_VALUE @ 38kHz"));
  sendHexNEC(0x80DF22DDUL, NEC_BIT_COUNT, 1, 38,10);
  delay(10); 
  Serial.println(F("Sending NEC_HEX_VALUE @ 38kHz"));
  sendHexNEC(0x90DF22DDUL, NEC_BIT_COUNT, 1, 38,11);
  delay(10); 

  Serial.println(F("Sending NEC_HEX_VALUE @ 38kHz"));
  sendHexNEC(0xA0DF22DDUL, NEC_BIT_COUNT, 1, 38,12);
  delay(10); 
  Serial.println(F("Sending NEC_HEX_VALUE @ 38kHz"));
  sendHexNEC(0xB0DF22DDUL, NEC_BIT_COUNT, 1, 38,13);
  delay(10); 

}



void sendHexNEC(unsigned long sigCode, byte numBits, unsigned char repeats, unsigned char kHz,int irpintx) {
  /*  A basic 32 bit NEC signal is made up of:
   *  1 x 9000 uSec Header Mark, followed by
   *  1 x 4500 uSec Header Space, followed by
   *  32 x bits uSec ( 1- bit 560 uSec Mark followed by 1690 uSec space; 0 - bit 560 uSec Mark follwed by 560 uSec Space)
   *  1 x 560 uSec Trailer Mark
   *  There can also be a generic repeat signal, which is usually not neccessary & can be replaced by sending multiple signals
   */
#define NEC_HEADER_MARK 9000
#define NEC_HEADER_SPACE 4500
#define NEC_ONE_MARK 560
#define NEC_ZERO_MARK 560
#define NEC_ONE_SPACE 1690
#define NEC_ZERO_SPACE 560
#define NEC_TRAILER_MARK 560

  unsigned long bitMask = (unsigned long) 1 << (numBits - 1); //allows for signal from 1 bit up to 32 bits
  //
  if (carrierFreq != kHz)  initSoftPWM(kHz); //we only need to re-initialise if it has changed from last signal sent

  sigTime = micros(); //keeps rolling track of signal time to avoid impact of loop & code execution delays
  sigStart = sigTime; //remember for calculating first repeat gap (space), must end 108ms after signal starts
  // First send header Mark & Space
  mark(NEC_HEADER_MARK,irpintx);
  space(NEC_HEADER_SPACE);

  while (bitMask) {
    if (bitMask & sigCode) { //its a One bit
      mark(NEC_ONE_MARK,irpintx);
      space(NEC_ONE_SPACE);
    }
    else { // its a Zero bit
      mark(NEC_ZERO_MARK,irpintx);
      space(NEC_ZERO_SPACE);
    }
    bitMask = (unsigned long) bitMask >> 1; // shift the mask bit along until it reaches zero & we exit the while loop
  }
  // Last send NEC Trailer MArk
  mark(NEC_TRAILER_MARK,irpintx);

  //now send the requested number of NEC repeat signals. Repeats can be useful for certain functions like Vol+, Vol- etc
  /*  A repeat signal consists of
   *   A space which ends 108ms after the start of the last signal in this sequence
  *  1 x 9000 uSec Repeat Header Mark, followed by
  *  1 x 2250 uSec Repeat Header Space, followed by
  *  32 x bits uSec ( 1- bit 560 uSec Mark followed by 1690 uSec space; 0 - bit 560 uSec Mark follwed by 560 uSec Space)
  *  1 x 560 uSec repeat Trailer Mark
  */
  //First calcualte length of space for first repeat
  //by getting length of signal to date and subtracting from 108ms

  if (repeats == 0) return; //finished - no repeats
  else if (repeats > 0) { //first repeat must start 108ms after first signal
    space(108000 - (sigTime - sigStart)); //first repeat Header should start 108ms after first signal
    mark(NEC_HEADER_MARK,irpintx);
    space(NEC_HEADER_SPACE / 2); //half the length for repeats
    mark(NEC_TRAILER_MARK,irpintx);
  }

  while (--repeats > 0) { //now send any remaining repeats
    space(108000 - NEC_HEADER_MARK - NEC_HEADER_SPACE / 2 - NEC_TRAILER_MARK); //subsequent repeat Header must start 108ms after previous repeat signal
    mark(NEC_HEADER_MARK,irpintx);
    space(NEC_HEADER_SPACE / 2); //half the length for repeats
    mark(NEC_TRAILER_MARK,irpintx);
  }

}




void initSoftPWM(unsigned char carrierFreq) { // Assumes standard 8-bit Arduino, running at 16Mhz
  //supported values are 30, 33, 36, 38, 40, 56 kHz, any other value defaults to 38kHz
  //we will aim for a  duty cycle of circa 33%

  period =  (1000 + carrierFreq / 2) / carrierFreq;
  periodHigh = (period + 1) / 3;
  periodLow = period - periodHigh;
  //  Serial.println (period);
  //  Serial.println (periodHigh);
  //  Serial.println (periodLow);
  Serial.println (carrierFreq);

  switch (carrierFreq) {
    case 30  : //delivers a carrier frequency of 29.8kHz & duty cycle of 34.52%
      periodHigh -= 6; //Trim it based on measurementt from Oscilloscope
      periodLow  -= 10; //Trim it based on measurementt from Oscilloscope
      break;

    case 33  : //delivers a carrier frequency of 32.7kHz & duty cycle of 34.64%
      periodHigh -= 6; //Trim it based on measurementt from Oscilloscope
      periodLow  -= 10; //Trim it based on measurementt from Oscilloscope
      break;

    case 36  : //delivers a carrier frequency of 36.2kHz & duty cycle of 35.14%
      periodHigh -= 6; //Trim it based on measurementt from Oscilloscope
      periodLow  -= 11; //Trim it based on measurementt from Oscilloscope
      break;

    case 40  : //delivers a carrier frequency of 40.6kHz & duty cycle of 34.96%
      periodHigh -= 6; //Trim it based on measurementt from Oscilloscope
      periodLow  -= 11; //Trim it based on measurementt from Oscilloscope
      break;

    case 56  : //delivers a carrier frequency of 53.8kHz & duty cycle of 40.86%
      periodHigh -= 6; //Trim it based on measurementt from Oscilloscope
      periodLow  -= 12; //Trim it based on measurementt from Oscilloscope
      Serial.println(periodHigh);
      Serial.println(periodLow);

      break;


    case 38  : //delivers a carrier frequency of 37.6kHz & duty cycle of 36.47%
    default :
      periodHigh -= 6; //Trim it based on measurementt from Oscilloscope
      periodLow  -= 11; //Trim it based on measurementt from Oscilloscope
      break;
  }
}

void mark(unsigned int mLen, int irpintx) { //uses sigTime as end parameter
  sigTime += mLen; //mark ends at new sigTime
  unsigned long now = micros();
  unsigned long dur = sigTime - now; //allows for rolling time adjustment due to code execution delays
  if (dur == 0) return;
  while ((micros() - now) < dur) { //just wait here until time is up
    digitalWrite(irpintx, HIGH);
    if (periodHigh) delayMicroseconds(periodHigh);
    digitalWrite(irpintx, LOW);
    if (periodLow)  delayMicroseconds(periodLow);
  }
}

void space(unsigned int sLen) { //uses sigTime as end parameter
  sigTime += sLen; //space ends at new sigTime
  unsigned long now = micros();
  unsigned long dur = sigTime - now; //allows for rolling time adjustment due to code execution delays
  if (dur == 0) return;
  while ((micros() - now) < dur) ; //just wait here until time is up
}
