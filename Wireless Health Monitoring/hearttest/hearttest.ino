unsigned long b=0;
void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
}

void loop() {
  

 while (analogRead(A0) < 600);
  while (analogRead(A0) >= 600);
  int T1 = millis();
  while (analogRead(A0) > 600);
  while (analogRead(A0) <= 600);
  int T2 = millis();
  int Time = T2-T1;
  unsigned long HeartRate = 60000L;
  HeartRate = HeartRate/Time; 
  Serial.print("BPM = ");
  Serial.println(HeartRate);
  b=HeartRate;


  // put your main code here, to run repeatedly:

}
