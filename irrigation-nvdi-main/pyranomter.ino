#define ANALOG_PIN A0 // Analog pin
#define RESISTANCE 10 // Resistance in thousands of ohms
volatile float PANEL_LENGTH = 127; // Length of solar cell in mm
volatile float PANEL_WIDTH = 76; // Width of solar cell in mm
volatile float Area;
volatile float Power;
volatile float Radiation;
/*
* Main Setup function
*/
void setup() {
// Begin serial communication
Serial.begin(9600);
Serial.println("Test");
}
/*
* Main Setup function
*/
void loop() {
Area = PANEL_LENGTH * PANEL_WIDTH / (100*100); // we are dividing by 10000 get the area in square meters
Power = pow(analogRead( ANALOG_PIN ), 2) / RESISTANCE ; // Calculating power
Radiation = Power / Area;
Serial.println(Area);
Serial.println(Power);
Serial.println(Radiation);
Serial.println();
delay(1000);
}
