#include <Esplora.h>
#include <math.h>

const int x_center = 12;
const int y_center = 2;
const int numOfSpeeds = 8;

int lastLmotor = 0;
int lastRmotor = 0;

float lastTimeSendCommand = 0;
float commandInterval = 100;

void setup() {
  Serial1.begin(9600);
}

void loop() {
  int jcorX = x_center-Esplora.readJoystickX();
  int jcorY = y_center-Esplora.readJoystickY();
  float length = sqrt(pow(jcorX,2)+pow(jcorY,2));
  length = length > 512 ? 512 : length;
  length = length < -512 ? -512 : length;
  float angle = atan2f((float)jcorY,(float)jcorX); //angle from x-axis
  angle = angle>=0 ? angle : angle + 2*PI;
  angle = angle/3.14*180;
  int Lmotor(0), Rmotor(0);
  
  bool symmetry = false;
  if(angle > 180){
    symmetry = true;
    angle = angle - 180;
  }
  
  if(angle > 350 || angle <= 10){
    Lmotor=length/512*numOfSpeeds;
    Rmotor=-length/512*numOfSpeeds;
  }else if(angle > 10 && angle <= 30){
    Lmotor=length/512*numOfSpeeds;
    Rmotor=length/512*numOfSpeeds/4;
  }else if(angle > 30 && angle <= 45){
    Lmotor=length/512*numOfSpeeds;
    Rmotor=length/512*numOfSpeeds/2;
  }else if(angle > 45 && angle <= 80){
    Lmotor=length/512*numOfSpeeds;
    Rmotor=length/512*numOfSpeeds*3/4;
  }else if(angle > 80 && angle <= 100){
    Lmotor=length/512*numOfSpeeds;
    Rmotor=length/512*numOfSpeeds;
  }else if(angle > 100 && angle <= 135){
    Lmotor=length/512*numOfSpeeds*3/4;
    Rmotor=length/512*numOfSpeeds;
  }else if(angle > 135 && angle <= 150){
    Lmotor=length/512*numOfSpeeds/2;
    Rmotor=length/512*numOfSpeeds;
  }else if(angle > 150 && angle < 170){
    Lmotor=length/512*numOfSpeeds/4;
    Rmotor=length/512*numOfSpeeds;
  }
  
  if(symmetry){
    Lmotor = -Lmotor;
    Rmotor = -Rmotor;
    if(angle > 10 && angle < 170){
      float tmp = Lmotor;
      Lmotor = Rmotor;
      Rmotor = tmp;
    }
  }
  
  float currentTime = millis();
  if(Lmotor != lastLmotor || Rmotor != lastRmotor
    || currentTime-lastTimeSendCommand >= commandInterval){
    Serial1.write((char)Lmotor);
    Serial1.write((char)Rmotor);
    Serial1.write('\n');
    lastLmotor = Lmotor;
    lastRmotor = Rmotor; 
    lastTimeSendCommand = currentTime;
  }
  
  /*if(Esplora.readButton(SWITCH_1)==LOW){
    Serial1.println("st");
  }
  if(Esplora.readButton(SWITCH_3)==LOW){
    Serial1.println("sl");
  }*/
  
}
