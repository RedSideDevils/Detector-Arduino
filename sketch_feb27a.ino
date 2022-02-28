// Include the Servo library 
#include <Servo.h>

int servoPin = 4; 
#define echoPin 2
#define trigPin 3

String inBytes;
Servo Servo1; 

int distanceCalc(){
  long duration;
  int distance;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;
  return distance;
}

void setup() { 
  Servo1.attach(servoPin); 
  Serial.begin(9600);
  pinMode(trigPin,OUTPUT);
  pinMode(echoPin,INPUT);
}
void loop(){ 
  if(Serial.available() > 0){ 
    inBytes = Serial.readStringUntil('\n');
    if(inBytes == "GO"){
      for(int i = 0; i <= 180; i++){
        Servo1.write(i);
        Serial.println(distanceCalc());
        delay(500);
      }
  
      for(int i = 180; i >= 0; i--){
        Servo1.write(i); 
        Serial.println(distanceCalc());
        delay(500);
      }
    }  
  }
}
