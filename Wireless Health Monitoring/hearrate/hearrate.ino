int Pulse = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  while (analogRead(Pulse) >= 282);
  while (analogRead(Pulse) <= 262);
  int T1 = millis();
  while (analogRead(Pulse) >= 282);
  while (analogRead(Pulse) <= 262);
  int T2 = millis();
  int Time = T2-T1;
  unsigned long HeartRate = 60000L;
  HeartRate = HeartRate/Time; 
  Serial.print("BPM = ");
  Serial.println(HeartRate);
//  delay(1000); 
} 

