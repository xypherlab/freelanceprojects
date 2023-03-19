volatile int coins = 0;
volatile int bills = 0;
const int lockerA =  14;
const int lockerB =  15;
void setup()
{ Serial.begin(9600);

pinMode (2,INPUT_PULLUP);
  pinMode (3,INPUT_PULLUP);
  attachInterrupt(0, coinInserted, FALLING);
  attachInterrupt(1, billInserted, FALLING);
  pinMode(lockerA, OUTPUT);
 pinMode(lockerB, OUTPUT);
 Serial.println("Coin and Bill Test");
  //  digitalWrite(lockerA, HIGH);
 // digitalWrite(lockerB, LOW);
 // delay(2000);
 // digitalWrite(lockerA, LOW);
//  digitalWrite(lockerB, HIGH);
//  delay(2000);
}
void coinInserted()
{
  coins = coins + 1;
  Serial.print("Coins: ");Serial.println(coins);
}
void billInserted()
{
  bills = bills + 1;
  Serial.print("Bills: ");Serial.println(bills);
}
void loop()
{
  
}
