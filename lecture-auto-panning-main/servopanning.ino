#include <Servo.h>
Servo panning;
void setup() {
Serial.begin(9600);
panning.attach(7);
//panning.write(90);
}

void loop() {
if ( Serial.available()) {
  int dir=Serial.parseInt(); 
  
  if (dir>0)
  {panning.write(dir);
    Serial.println(dir);
  }
    
}
}
