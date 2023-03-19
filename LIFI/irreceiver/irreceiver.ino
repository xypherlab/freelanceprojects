
#define DECODE_NEC 1

#include <IRremote.h>

int IR_RECEIVE_PIN = 14;
int flag=0;
void setup() {
   Serial.begin(9600);
    IrReceiver.begin(IR_RECEIVE_PIN, ENABLE_LED_FEEDBACK, USE_DEFAULT_FEEDBACK_LED_PIN);

}

void loop() {

    if (IrReceiver.decode()) {
       
        

       
        //Serial.print(IrReceiver.decodedIRData.address);

        IrReceiver.resume(); // Enable receiving of the next value

        if(flag==0)
        {
        if (IrReceiver.decodedIRData.address == 64256) {
            Serial.println("A1,");
        }
        
         
        else if (IrReceiver.decodedIRData.address ==64264) {
            // do something else
            Serial.println("A2,");
        }
        else if (IrReceiver.decodedIRData.address ==4) {
            // do something else
            Serial.println("A3,");
        }
        else if (IrReceiver.decodedIRData.address ==64268) {
            // do something else
            Serial.println("A4,");
        }
        else if (IrReceiver.decodedIRData.address ==64258) {
            // do something else
            Serial.println("A5,");
        }
        else if (IrReceiver.decodedIRData.address ==64266) {
            // do something else
            Serial.println("A6,");
        }
        else if (IrReceiver.decodedIRData.address ==64262) {
            // do something else
            Serial.println("A7,");
        }
        else if (IrReceiver.decodedIRData.address ==64270) {
            // do something else
            Serial.println("A8,");
        }
        else if (IrReceiver.decodedIRData.address ==64257) {
            // do something else
            Serial.println("A9,");
        }
        else if (IrReceiver.decodedIRData.address ==64265) {
            // do something else
            Serial.println("A10,");
        }
        else if (IrReceiver.decodedIRData.address ==64261) {
            // do something else
            Serial.println("A11,");
        }
        else if (IrReceiver.decodedIRData.address ==64269) {
            // do something else
            Serial.println("A12,");
        }
        else if (IrReceiver.decodedIRData.address == 64384) {
            Serial.println("A13,");
        }
        
         
        else if (IrReceiver.decodedIRData.address ==64392) {
            // do something else
            Serial.println("A14,");
        }
        else if (IrReceiver.decodedIRData.address ==64388) {
            // do something else
            Serial.println("A15,");
        }
        else if (IrReceiver.decodedIRData.address ==64396) {
            // do something else
            Serial.println("A16,");
        }
        else if (IrReceiver.decodedIRData.address ==64386) {
            // do something else
            Serial.println("A17,");
        }
        else if (IrReceiver.decodedIRData.address ==64394) {
            // do something else
            Serial.println("A18,");
        }
        else if (IrReceiver.decodedIRData.address ==64390) {
            // do something else
            Serial.println("A19,");
        }
        else if (IrReceiver.decodedIRData.address ==64398) {
            // do something else
            Serial.println("A20,");
        }
        else if (IrReceiver.decodedIRData.address ==64385) {
            // do something else
            Serial.println("A21,");
        }
        else if (IrReceiver.decodedIRData.address ==64393) {
            // do something else
            Serial.println("A22,");
        }
        else if (IrReceiver.decodedIRData.address ==64389) {
            // do something else
            Serial.println("A23,");
        }
        else if (IrReceiver.decodedIRData.address ==64397) {
            // do something else
            Serial.println("A24,");
        }
        ;
        delay(100);
        }
        if(flag==0)
        {
          flag=1;
        }
        else if(flag==1)
        {
          flag=0;
        }
    }
}
