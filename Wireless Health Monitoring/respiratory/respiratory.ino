int flag=0;
unsigned long a;
unsigned long T1;
unsigned long T2;
int rrpin = 15; 

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
pinMode(rrpin, INPUT_PULLUP);
}

void loop() {
  // put your main code here, to run repeatedly:
/*  a=0;
while (a == 0)
  {
    Serial.println(analogRead(A0));
    if (analogRead(A0) <590 and flag == 0)
    {Serial.print("Low: "); Serial.println(analogRead(A0));
      flag = 1;
      
    }
     else if (analogRead(A0) >=610 and flag == 1)
    {Serial.print("High: "); Serial.println(analogRead(A0));
      T1 = millis();
      flag = 2;
      
    }
    else if (analogRead(A0) < 590 and flag == 2)
    { Serial.print("Low: "); Serial.println(analogRead(A0));
     
      flag = 3;
    }
    else if (analogRead(A0) >= 610 and flag == 3)
    { Serial.print("High: "); Serial.println(analogRead(A0));
      T2 = millis();
      unsigned long Time = T2 - T1;
      unsigned long respRate = 60000L;
      respRate = respRate / Time;
      Serial.print("RR = ");
      Serial.println(respRate);
      flag = 0;

      a = respRate;
      delay(3000);

    }
  }*/
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
      a = respRate;
      //delay(3000);

    }  
}
