#include <Servo.h>

#define inputpin1 1;
#define inputpin2 2;
#define inputpin3 3;
#define inputpin4 4;
#define outputpin 0;



void setup() {
  // put your setup code here, to run once:
  pinMode(inputpin1, INPUT);
  pinMode(inputpin2, INPUT);
  pinMode(inputpin3, INPUT);
  pinMode(inputpin4, INPUT);
  pinMode(outputpin, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:

  if(inputpin1 == HIGH) {
    digitalWrite(outputpin, HIGH);
    delay(15);
    digitalWrite(outputpin, LOW);
    delay(5);
    digitalWrite(outputpin, HIGH);
  }else if(inputpin2 == HIGH) {
    digitalWrite(outputpin, HIGH);
    delay(25);
    digitalWrite(outputpin, LOW);
    delay(5);
    digitalWrite(outputpin, HIGH);
  }else if(inputpin3 == HIGH) {
    digitalWrite(outputpin, HIGH);
    delay(35);
    digitalWrite(outputpin, LOW);
    delay(5);
    digitalWrite(outputpin, HIGH);
  }else if(inputpin4 == HIGH) {
    digitalWrite(outputpin, HIGH);
    delay(45);
    digitalWrite(outputpin, LOW);
    delay(5);
    digitalWrite(outputpin, HIGH);
  }

}
