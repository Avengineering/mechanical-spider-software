#include <QueueList.h>

QueueList<String> jobQueue;

int RmotorPulsePin = 3;
int RmotorDirPin = 2;
int LmotorPulsePin = 9;
int LmotorDirPin = 8;
int sleepPin = 7;

float lastTimeExec=0;
const float commandInterval = 0;

float LlastTime=0;
float RlastTime=0;
float LmotorFreq=0;
float RmotorFreq=0;
bool LmotorPinState = LOW;
bool RmotorPinState = LOW;

bool checkCommunication();
void executeCommand();

void setup() {
  pinMode(LmotorPulsePin, OUTPUT);
  pinMode(LmotorDirPin, OUTPUT);
  pinMode(RmotorPulsePin, OUTPUT);
  pinMode(RmotorPulsePin, OUTPUT);
  pinMode(sleepPin, OUTPUT);
  digitalWrite(LmotorDirPin, LOW);
  digitalWrite(RmotorDirPin, HIGH);
  digitalWrite(sleepPin, HIGH);
  Serial.begin(9600);
  Serial.setTimeout(50);
  RlastTime = millis();
  LlastTime = millis();
  lastTimeExec = millis();
}

void loop() {
  checkCommunication();
  executeCommand();
}

bool checkCommunication(){
  if(Serial.available()){
    String str = Serial.readStringUntil('\n');
    jobQueue.push(str);
    return true;
  }else{
    return false;
  } 
}

void executeCommand(){
  if(jobQueue.count() > 0){
    float currentTime = millis();
    float interval = currentTime-lastTimeExec;
    if(interval > commandInterval){
      String command = jobQueue.pop();
      
      if(command=="sl")
      {
        digitalWrite(sleepPin, LOW);
      }
      else if(command=="st"){
        digitalWrite(sleepPin,HIGH);
      }
      else{
        digitalWrite(sleepPin, HIGH);
        float Lfreq = 60.0*((int)command[0]);
        float Rfreq = 60.0*((int)command[1]);
        if(Lfreq > -1000 && Lfreq < 1000 && Rfreq > -1000 && Rfreq < 1000){
          if(Lfreq < 0){
            digitalWrite(LmotorDirPin, HIGH);
            Lfreq = -Lfreq;
          }else{
            digitalWrite(LmotorDirPin, LOW);
          } 
          if(Rfreq < 0){
            digitalWrite(RmotorDirPin, LOW);
            Rfreq = -Rfreq;
          }else{
            digitalWrite(RmotorDirPin, HIGH);
          }
          LmotorFreq = Lfreq;
          RmotorFreq = Rfreq;
          Serial.print(LmotorFreq);
          Serial.print(" ");
          Serial.println(RmotorFreq);
          
        }
      }
      
      lastTimeExec=currentTime;
    }
  }
  
  
  float currentTime = millis();
  if (LmotorFreq != 0 && currentTime - LlastTime > (1/LmotorFreq*1000)/2){
    LmotorPinState = !LmotorPinState;
    digitalWrite(LmotorPulsePin, LmotorPinState);
    LlastTime = currentTime;
  }
  if (RmotorFreq != 0 && currentTime - RlastTime > (1/RmotorFreq*1000)/2){
    RmotorPinState = !RmotorPinState;
    digitalWrite(RmotorPulsePin, RmotorPinState);
    RlastTime = currentTime;
  }
}


