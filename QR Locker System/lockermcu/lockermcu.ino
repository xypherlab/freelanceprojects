const int lockerA =  7;
const int lockerB =  6;
void setup() {
  pinMode(lockerA, OUTPUT);
  pinMode(lockerB, OUTPUT);

}

void loop() {
  digitalWrite(lockerA, HIGH);
  digitalWrite(lockerB, LOW);
  delay(2000);
  digitalWrite(lockerA, LOW);
  digitalWrite(lockerB, HIGH);
  delay(2000);
}
