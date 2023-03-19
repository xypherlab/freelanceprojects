int Pulse = A0;
int counter=0;
void setup() {
  Serial.begin(9600);
}

void loop() {
  while (analogRead(Pulse) >=450);
  //Serial.println(analogRead(Pulse));
  while (analogRead(Pulse) <=400);
  //Serial.println(analogRead(Pulse));
  int T1 = millis();
  while (analogRead(Pulse) >=450);
  //Serial.println(analogRead(Pulse));
  while (analogRead(Pulse) <=400);
  //Serial.println(analogRead(Pulse));
  int T2 = millis();
  int Time = T2-T1;
  unsigned long lightrate = 60000L;
  lightrate = lightrate/Time;
  counter=counter+1; 
  Serial.print("PPM = ");
  Serial.println(lightrate);
  Serial.println(counter);
//delay(1000); 
} 
