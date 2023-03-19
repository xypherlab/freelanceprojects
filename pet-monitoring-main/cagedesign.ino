int conveyorpinA1 =  7;
int conveyorpinA2 =  8;
int conveyorpinB1 =  9;
int conveyorpinB2 =  10;
void setup() {
    Serial.begin(9600);
    pinMode(conveyorpinA1, OUTPUT);
    pinMode(conveyorpinA2, OUTPUT);
     pinMode(conveyorpinB1, OUTPUT);
    pinMode(conveyorpinB2, OUTPUT);
    digitalWrite(conveyorpinA1, LOW);
    digitalWrite(conveyorpinA2, LOW);
    digitalWrite(conveyorpinB1, LOW);
    digitalWrite(conveyorpinB2, LOW);
}

void loop() {
        String conveyorstatus = Serial.readStringUntil(',');
        
        if(conveyorstatus == "A")
        { Serial.println("Forward");
          digitalWrite(conveyorpinA1, HIGH);
          digitalWrite(conveyorpinA2, HIGH);
          digitalWrite(conveyorpinB1, LOW);
          digitalWrite(conveyorpinB2, LOW);
          
        }
        else if(conveyorstatus == "B")
{Serial.println("Stop");
  digitalWrite(conveyorpinA1, LOW);
          digitalWrite(conveyorpinA2, LOW);
          digitalWrite(conveyorpinB1, LOW);
          digitalWrite(conveyorpinB2, LOW);
}
else if(conveyorstatus == "C")
{Serial.println("Reverse");
  digitalWrite(conveyorpinA1, LOW);
          digitalWrite(conveyorpinA2, LOW);
          digitalWrite(conveyorpinB1, HIGH);
          digitalWrite(conveyorpinB2, HIGH);
}
          
        }


