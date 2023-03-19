/*
e-Gizmo Heart Rate Motor

This sample codes use to measured 
the BPM @ 90% accuracy.

e-Gizmo Mechatronix Central
http://www.e-gizmo.com
February 18, 2015

See your target Heart rate.
http://www.nscsd.org/webpages/rbrown/resources.cfm?subpage=44108
*/

int Pulse = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  while (digitalRead(Pulse) == HIGH);
  while (digitalRead(Pulse) == LOW);
  int T1 = millis();
  while (digitalRead(Pulse) == HIGH);
  while (digitalRead(Pulse) == LOW);
  int T2 = millis();
  int Time = T2-T1;
  unsigned long HeartRate = 60000L;
  HeartRate = HeartRate/Time; 
  Serial.print("BPM = ");
  Serial.println(HeartRate);
//  delay(1000); 
} 
