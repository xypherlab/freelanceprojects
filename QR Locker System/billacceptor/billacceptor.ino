volatile int pulses = 0; // counting the pulses sent
int checked = true;


void setup()
{
  Serial.begin(9600); // setup the serial port for communications with the host computer
  attachInterrupt(1, count_pulses, CHANGE);
 }

void count_pulses()
{
  int val = digitalRead(2);
  checked = false;
 if (val == HIGH) 
  {
    pulses += 1;
  }
}

void loop()
{
if(pulses == 4)
{
    "The rest of your code here that will run after a dollar is inserted"
  pulses = 0;
checked = true;
 }
} 
