#define LED_PIN 13
#define LDR_PIN A0
#define THRESHOLD 490
#define PERIOD 1

bool previous_state;
bool current_state;
int reading = analogRead(LDR_PIN);
void setup() 
{
    Serial.begin(9600);
    pinMode(LED_PIN, OUTPUT);
}

void loop() 
{
  current_state = get_ldr();
  if(!current_state && previous_state)
  {
    print_byte(get_byte());
  }
  previous_state = current_state;
  reading = analogRead(LDR_PIN);
  Serial.println(reading);
}

bool get_ldr()
{
  int voltage = analogRead(LDR_PIN);
  return voltage > THRESHOLD ? true : false;
}

char get_byte()
{
  char ret = 0;
  delay(PERIOD*1.5);
  for(int i = 0; i < 8; i++)
  {
   ret = ret | get_ldr() << i; 
   delay(PERIOD);
  }
  return ret;
}
void print_byte(char my_byte)
{
  char buff[2];
  sprintf(buff, "%c", my_byte);
  Serial.print(buff);
}
