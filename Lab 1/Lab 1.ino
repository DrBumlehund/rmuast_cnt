/** 
 *  Copyright 2018 Chris Bang Sørensen, Niels Hvid, Thomas Lemqvist  
 *  
 *  Permission is hereby granted, free of charge, to any person obtaining a copy 
 *  of this software and associated documentation files (the "Software"), to deal 
 *  in the Software without restriction, including without limitation the rights 
 *  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
 *  of the Software, and to permit persons to whom the Software is furnished to do so, 
 *  subject to the following conditions:
 *  
 *  The above copyright notice and this permission notice shall be included in all 
 *  copies or substantial portions of the Software.
 *  
 *  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
 *  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
 *  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
 *  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
 *  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
 *  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *
 */

#include <TimerOne.h>

const int rcPin = 9;
String input;
boolean armed = false;

int lower;
int upper;

void setup(void)
{
  Timer1.initialize(20000); // Initialize with 20 ms period for RC signal
  setBounds(1,2); // Set the pulsewidth range to 1ms for 0% and 2ms for 100%
  
  Serial.begin(9600);
  Serial.setTimeout(30);
  
  pinMode(rcPin, OUTPUT);
}

void setPW(int _throttle) // Get a throttle percentage and set pulsewidth accordingly
{
  if(!armed) { // Make sure we're armed before sending values
    Serial.println("Not armed"); 
    return; 
  }
  
  int throttle = map(_throttle, 0, 100, lower, upper);
  Serial.println(throttle);
  Timer1.pwm(rcPin, throttle);
}

void setBounds (float _lower, float _upper){ // Input: pulsewidth ranges in ms
  lower = (int)((float)_lower/20*1023);
  upper = (int)((float)_upper/20*1023);
}

void calibrate(){
  Serial.println("Calbrating");
  Timer1.pwm(rcPin, upper);
  delay(500);
  Timer1.pwm(rcPin, lower);
  delay(500);
}

void arm(){
  armed = true;
  setPW(0);
}

void disarm(){
  setPW(0);
  armed = false;
}

void loop(void)
{

  if (Serial.available()) {
    input = Serial.readString();
    Serial.print("Received ");
    Serial.println(input);
  }

  if (input == "arm"){
    arm();
  } else if (input == "disarm"){
    disarm();
  } else if (input == "calibrate"){
    calibrate();
  } else if (input == "pw"){
    Serial.setTimeout(3000);
    int throttle = Serial.parseInt();
    Serial.setTimeout(30);
    setPW(throttle);
    
  }
  input = " ";

}
