
#define DECODE_NEC 1

#include <IRremote.h>

int IR_RECEIVE_PIN = 14;
int flag=0;
void setup() {
   Serial.begin(115200);
    IrReceiver.begin(IR_RECEIVE_PIN, ENABLE_LED_FEEDBACK, USE_DEFAULT_FEEDBACK_LED_PIN);

}

void loop() {

    if (IrReceiver.decode()) {
       
        

       
        Serial.println(IrReceiver.decodedIRData.address);

        IrReceiver.resume(); // Enable receiving of the next value

        if(flag==0)
        {
        if (IrReceiver.decodedIRData.address == 64384) {
            Serial.println("A13");
        }
        
         
        else if (IrReceiver.decodedIRData.address ==64392) {
            // do something else
            Serial.println("A14");
        }
        else if (IrReceiver.decodedIRData.address ==64388) {
            // do something else
            Serial.println("A15");
        }
        else if (IrReceiver.decodedIRData.address ==64396) {
            // do something else
            Serial.println("A16");
        }
        else if (IrReceiver.decodedIRData.address ==64386) {
            // do something else
            Serial.println("A17");
        }
        else if (IrReceiver.decodedIRData.address ==64394) {
            // do something else
            Serial.println("A18");
        }
        else if (IrReceiver.decodedIRData.address ==64390) {
            // do something else
            Serial.println("A19");
        }
        else if (IrReceiver.decodedIRData.address ==64398) {
            // do something else
            Serial.println("A20");
        }
        else if (IrReceiver.decodedIRData.address ==64385) {
            // do something else
            Serial.println("A21");
        }
        else if (IrReceiver.decodedIRData.address ==64393) {
            // do something else
            Serial.println("A22");
        }
        else if (IrReceiver.decodedIRData.address ==64389) {
            // do something else
            Serial.println("A23");
        }
        else if (IrReceiver.decodedIRData.address ==64397) {
            // do something else
            Serial.println("A24");
        }
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
