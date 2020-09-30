#include <Servo.h>

Servo frontright1;//サーボの設定
Servo frontright2;
Servo frontleft1;
Servo frontleft2;
Servo backright1;
Servo backright2;
Servo backleft1;
Servo backleft2;

#define inputpin 5//信号ピン
#define outputpin 6

int frf = 80;//前右の角度
int frn = 45;
int frb = 0;
int fru = 80;
int frd = 40;

int flf = 0;//前左の角度
int fln = 20;
int flb = 65;
int flu = 110;
int fld = 150;

int brf = 180;//後右の角度
int brn = 135;
int brb = 110;
int bru = 60;
int brd = 100;

int blf = 0;//後左の角度
int bln = 45;
int blb = 80;
int blu = 50;
int bld = 0;

void setangle(String servo, int angle) {//サーボへの角度の入力

  if(servo == "frontright1") {
    digitalWrite(2, LOW);
    digitalWrite(3, LOW);
    digitalWrite(4, LOW);
    frontright1.write(angle);
  }else if(servo =="frontright2") {
    digitalWrite(2, HIGH);
    digitalWrite(3, LOW);
    digitalWrite(4, LOW);
    frontright2.write(angle);
  }else if(servo =="fronleft1") {
    digitalWrite(2, LOW);
    digitalWrite(3, LOW);
    digitalWrite(4, HIGH);
    frontleft1.write(angle);
  }else if(servo =="frontleft2") {
    digitalWrite(2, LOW);
    digitalWrite(3, HIGH);
    digitalWrite(4, HIGH);
    frontleft2.write(angle);
  }else if(servo =="backleft1") {
    digitalWrite(2, LOW);
    digitalWrite(3, HIGH);
    digitalWrite(4, LOW);
    backleft1.write(angle);
  }else if(servo =="backleft2") {
    digitalWrite(2, HIGH);
    digitalWrite(3, HIGH);
    digitalWrite(4, LOW);
    backleft2.write(angle);
  }else if(servo =="backright1") {
    digitalWrite(2, LOW);
    digitalWrite(3, HIGH);
    digitalWrite(4, HIGH);
    backright1.write(angle);
  }else if(servo =="backright2") {
    digitalWrite(2, HIGH);
    digitalWrite(3, HIGH);
    digitalWrite(4, HIGH);
    backright2.write(angle);
  }
}


void forward() {//前進

  setangle("backright2", bru);
  setangle("backright1", brf);
  delay(50);
  setangle("backright2", brd);
  
  delay(10);
  
  setangle("frontright2", fru);
  setangle("frontright1", frf);
  delay(50);
  setangle("frontright2", frd);
  
  delay(10);
  
  setangle("frontright1", frn);
  setangle("frontleft1", flb);
  setangle("backright1", brn);
  setangle("backleft1", blb);
  
  delay(50);

  setangle("backleft2", blu);
  setangle("backleft1", blf);
  delay(50);
  setangle("backleft2", bld);

  delay(10);

  setangle("frontleft2", flu);
  setangle("frontleft1", flf);
  delay(50);
  setangle("frontleft2", fld);

  delay(10);

  setangle("frontright1", frb);
  setangle("frontleft1", fln);
  setangle("backright1", brb);
  setangle("backleft1", bln);
  
}


void back() {//後退

  setangle("frontleft2", flu);
  setangle("frontleft1", flb);
  delay(50);
  setangle("frontleft2", fld);
  
  delay(10);
  
  setangle("backleft2", blu);
  setangle("backleft1", blb);
  delay(50);
  setangle("backleft2", bld);
  
  delay(10);
  
  setangle("backleft1", bln);
  setangle("backright1", brf);
  setangle("frontleft1", fln);
  setangle("frontright1", frf);
  
  delay(50);

  setangle("frontright2", fru);
  setangle("frontright1", frb);
  delay(50);
  setangle("frontright2", frd);

  delay(10);

  setangle("backright2", bru);
  setangle("backright1", brb);
  delay(50);
  setangle("backright2", brd);

  delay(10);

  setangle("backleft1", blf);
  setangle("backright1", brn);
  setangle("frontleft1", flf);
  setangle("frontright1", frn);
  
}


void right() {//右回転

  setangle("frontright2", fru);
  setangle("frontright1", frb);
  delay(50);
  setangle("frontright2", frd);

  delay(10);

  setangle("frontleft2", flu);
  setangle("frontleft1", flf);
  delay(50);
  setangle("frontleft2", fld);

  delay(10);

  setangle("backleft2", blu);
  setangle("backleft1", blf);
  delay(50);
  setangle("backleft2", bld);

  delay(10);

  setangle("backright2", bru);
  setangle("backright1", brb);
  delay(50);
  setangle("backright2", brd);

  delay(10);

  setangle("frontright1", frn);
  setangle("frontleft1", fln);
  setangle("backleft1", bln);
  setangle("backright1", brn);
  
}


void left() {//左回転

  setangle("frontright2", fru);
  setangle("frontright1", frf);
  delay(50);
  setangle("frontright2", frd);

  delay(10);

  setangle("frontleft2", flu);
  setangle("frontleft1", flb);
  delay(50);
  setangle("frontleft2", fld);

  delay(10);

  setangle("backleft2", blu);
  setangle("backleft1", blb);
  delay(50);
  setangle("backleft2", bld);

  delay(10);

  setangle("backright2", bru);
  setangle("backright1", brf);
  delay(50);
  setangle("backright2", brd);

  delay(10);

  setangle("frontright1", frn);
  setangle("frontleft1", fln);
  setangle("backleft1", bln);
  setangle("backright1", brn);
  
}



void receive() {

  int htime = pulseIn(inputpin,HIGH);

  if (htime >= 10 && htime <= 20) {//前進
    digitalRead(inputpin);
    while(inputpin == HIGH) {
      forward();
    }
  }

  if (htime > 20 && htime <= 30) {//後退
    digitalRead(inputpin);
    while(inputpin == HIGH) {
      back();
    }
  }

  if (htime > 30 && htime <= 40) {//右
    digitalRead(inputpin);
    while(inputpin == HIGH) {
      right();
    }
  }

  if (htime > 40 && htime <= 50) {//左
    digitalRead(inputpin);
    while(inputpin == HIGH) {
      left();
    }
  }
}





void setup() {
  // put your setup code here, to run once:
  pinMode(inputpin,INPUT);
  frontright1.attach(outputpin);
  frontright2.attach(outputpin);
  frontleft1.attach(outputpin);
  frontleft2.attach(outputpin);
  backright1.attach(outputpin);
  backright2.attach(outputpin);
  backleft1.attach(outputpin);
  backleft2.attach(outputpin);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  receive();
  
}
