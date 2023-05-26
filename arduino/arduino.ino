#include <ros.h>
#include <std_msgs/Int32MultiArray.h>
#include <Stepper.h>


ros::NodeHandle nh;

char data;
int left_value;
int right_value;
int motorLeftSpeed = 0;
int motorRightSpeed = 0;
int seekBarL = 50;
int seekBarR = 50;
int buttonL = 1;
int buttonR = 1;
int motorSw = 0;
int stopButton = 0;

int cameraStep = 4;
int xPos = 1;
int yPos = 1;
int xState = 500;
int xMax = 1000;
int xMin = 0;
int yState = 500;
int yMax = 1000;
int yMin = 0;

//Start_Relay
const int Relay = 52;
//Gyro_sensor
const char Gyro_SCL = A0;
const char Gyro_SDA = A1;
const int Gyro_INT = 2;
//Camera_1
const int Camera_1_A = 3;
const int Camera_1_Aa = 4;
const int Camera_1_B = 5;
const int Camera_1_Bb = 6;
//Camera_2
const int Camera_2_A = 8;
const int Camera_2_Aa = 9;
const int Camera_2_B = 10;
const int Camera_2_Bb = 11;
//Dc_forward_Left
const int Dc_Farward_Left_Dir = 42;
const int Dc_Farward_Left_PWM = 43;
//Dc_forward_Right
const int Dc_Farward_Right_Dir = 40;
const int Dc_Farward_Right_PWM = 13;
//Dc_backward_Left
const int Dc_Backward_Left_Dir = 38;
const int Dc_Backward_Left_PWM = 39;
//Dc_backward_Right
const int Dc_Backward_Right_Dir = 36;
const int Dc_Backward_Right_PWM = 37;
//Step_Left
const int dirPinLeft = 34;
const int stepPinLeft = 35;
const int enPinLeft = 32;
//Step_Right
const int dirPinRight = 33;
const int stepPinRight = 30;
const int enPinRight = 31;
//Ultra_Sonic_Sensor1
const int Sonic_1_Trig = 50;
const int Sonic_1_Echo = 51;
//Ultra_Sonic_Sensor2
const int Sonic_2_Trig = 48;
const int Sonic_2_Echo = 48;
//Ultra_Sonic_Sensor3
const int Sonic_3_Trig = 46;
const int Sonic_3_Echo = 47;
//Ultra_Sonic_Sensor4
const int Sonic_4_Trig = 44;
const int Sonic_4_Echo = 45;


const unsigned long stepDelay = 500;
unsigned long prevStepTimeLeft = 0;
unsigned long currentTimeLeft = 0;
unsigned long prevStepTimeRight = 0;
unsigned long currentTimeRight = 0;

void MotorData(const std_msgs::Int32MultiArray& msg) {
  seekBarL = msg.data[0];
  seekBarR = msg.data[1];
  buttonL = msg.data[2];
  buttonR = msg.data[3];
  motorSw = msg.data[4];
  stopButton = msg.data[5];
  xPos = msg.data[6];
  yPos = msg.data[7];
}

void StepForeward(int dir, int steppin){
  digitalWrite(dir, HIGH);
  digitalWrite(steppin, HIGH);
  delayMicroseconds(stepDelay); 
  digitalWrite(steppin, LOW);
  delayMicroseconds(stepDelay);
}

void StepStop(int dir, int steppin){
  digitalWrite(dir, LOW);
  digitalWrite(steppin, HIGH);
}

void StepBackward(int dir, int steppin){
  digitalWrite(dir, LOW);
  digitalWrite(steppin, HIGH);
  delayMicroseconds(stepDelay); 
  digitalWrite(steppin, LOW);
  delayMicroseconds(stepDelay);
}

Stepper Camera_1(200, Camera_1_A, Camera_1_Aa, Camera_1_B, Camera_1_Bb);
Stepper Camera_2(200, Camera_2_A, Camera_2_Aa, Camera_2_B, Camera_2_Bb);


ros::Subscriber<std_msgs::Int32MultiArray> motordata("/motordata", &MotorData);


void setup() {
  // 9600, 19200, 38400, 57600, 74880, 115200, 230400, 250000, 500000, 1000000, 2000000
  nh.getHardware()->setBaud(115200);
  //nh.getHardware()->setBaud(9600);
  nh.initNode();
  nh.subscribe(motordata);
  pinMode(Relay, HIGH);
  pinMode(13, OUTPUT);
  pinMode(Gyro_SCL, OUTPUT);
  pinMode(Gyro_SDA, OUTPUT);
  pinMode(Gyro_INT, OUTPUT);
  pinMode(Camera_1_A, OUTPUT);
  pinMode(Camera_1_Aa, OUTPUT);
  pinMode(Camera_1_B, OUTPUT);
  pinMode(Camera_1_Bb, OUTPUT);
  pinMode(Camera_2_A, OUTPUT);
  pinMode(Camera_2_Aa, OUTPUT);
  pinMode(Camera_2_B, OUTPUT);
  pinMode(Camera_2_Bb, OUTPUT);
  pinMode(Dc_Farward_Left_Dir, OUTPUT);
  pinMode(Dc_Farward_Left_PWM, OUTPUT);
  pinMode(Dc_Farward_Right_Dir, OUTPUT);
  pinMode(Dc_Farward_Right_PWM, OUTPUT);
  pinMode(Dc_Backward_Left_Dir, OUTPUT);
  pinMode(Dc_Backward_Left_PWM, OUTPUT);
  pinMode(Dc_Backward_Right_Dir, OUTPUT);
  pinMode(Dc_Backward_Right_PWM, OUTPUT);
  pinMode(dirPinLeft, OUTPUT);
  pinMode(stepPinLeft, OUTPUT);
  pinMode(enPinLeft, OUTPUT);
  pinMode(dirPinRight, OUTPUT);
  pinMode(stepPinRight, OUTPUT);
  pinMode(enPinRight, OUTPUT);
  pinMode(Sonic_1_Trig, OUTPUT);
  pinMode(Sonic_1_Echo, OUTPUT);
  pinMode(Sonic_2_Trig, OUTPUT);
  pinMode(Sonic_2_Echo, OUTPUT);
  pinMode(Sonic_3_Trig, OUTPUT);
  pinMode(Sonic_3_Echo, OUTPUT);
  pinMode(Sonic_4_Trig, OUTPUT);
  pinMode(Sonic_4_Echo, OUTPUT);
  Camera_1.setSpeed(30);
  Camera_2.setSpeed(30);
}


void loop() {
  nh.spinOnce();

  /////////////////////////////////////////////////// Emergency Stop
  if (stopButton == 1){
    digitalWrite(Relay, LOW);
  }

  /////////////////////////////////////////////////// seekBarL
  if (seekBarL >= 50){
    digitalWrite(Dc_Farward_Left_Dir, HIGH);
    digitalWrite(Dc_Backward_Left_Dir, HIGH);
    left_value = map(seekBarL, 50, 100, 0, 255);
    motorLeftSpeed = abs(left_value);
  } else{
    digitalWrite(Dc_Farward_Left_Dir, LOW);
    digitalWrite(Dc_Backward_Left_Dir, LOW);
    left_value = map(seekBarL, 0, 49, 255, 1);
    motorLeftSpeed = abs(left_value);
  }

  /////////////////////////////////////////////////// seekbarR
  if (seekBarR >= 50){
    digitalWrite(Dc_Farward_Right_Dir, HIGH);
    digitalWrite(Dc_Backward_Right_Dir, HIGH);
    right_value = map(seekBarR, 50, 100, 0, 255);
    motorRightSpeed = abs(right_value);
  } else{
    digitalWrite(Dc_Farward_Right_Dir, LOW);
    digitalWrite(Dc_Backward_Right_Dir, LOW);
    right_value = map(seekBarR, 0, 49, 255, 1);
    motorRightSpeed = abs(right_value);
  }

  /////////////////////////////////////////////////// DcMotrSw = 1
  if (motorSw = 1){    
    if (buttonR == 2){
      StepForeward(dirPinLeft, stepPinLeft);
      StepForeward(dirPinRight, stepPinRight);
    } else if(buttonR == 0){
      StepBackward(dirPinLeft, stepPinLeft);
      StepBackward(dirPinRight, stepPinRight);
    } else if(buttonR == 1){
      StepStop(dirPinLeft, stepPinLeft);
      StepStop(dirPinRight, stepPinRight);     
    } else {
      StepStop(dirPinLeft, stepPinLeft);
      StepStop(dirPinRight, stepPinRight);
    }
  }

  /////////////////////////////////////////////////// DcMotrSw = 0
  else{
    
    if (buttonL == 2){
      StepForeward(dirPinLeft, stepPinLeft);
    } else if(buttonL == 0){
      StepBackward(dirPinLeft, stepPinLeft);
    } else if(buttonL == 1){
      StepStop(dirPinLeft, stepPinLeft); 
    } else {
      StepStop(dirPinLeft, stepPinLeft);
    }
    
    if (buttonR == 2){
      StepForeward(dirPinRight, stepPinRight);
    } else if(buttonR == 0){
      StepBackward(dirPinRight, stepPinRight);
    } else if(buttonR == 1){
      StepStop(dirPinRight, stepPinRight);      
    } else {
      StepStop(dirPinRight, stepPinRight);
    }
  }

  /////////////////////////////////////////////////// Cam 1

  if (xPos == 2 and xState < xMax){
    Camera_1.step(cameraStep);
    delayMicroseconds(stepDelay);
    xState =+ cameraStep;
  }
  else if (xPos == 0 and xState > xMin){
    Camera_1.step(-cameraStep);
    delayMicroseconds(stepDelay);
    xState =- cameraStep;
  }

  /////////////////////////////////////////////////// Cam 2

  if (yPos == 2 and yState < xMax){
    Camera_2.step(cameraStep);
    delayMicroseconds(stepDelay);
    yState =+ cameraStep;
  }
  else if (yPos == 0 and yState > yMin){
    Camera_2.step(-cameraStep);
    delayMicroseconds(stepDelay);
    yState =- cameraStep;
  }
  
  //analogWrite(Dc_Farward_Left_PWM, motorLeftSpeed);
  //analogWrite(Dc_Farward_Right_PWM, 255);
  //analogWrite(Dc_Farward_Right_PWM, motorRightSpeed);
  
  //analogWrite(Dc_Backward_Left_PWM, motorLeftSpeed);
  //analogWrite(Dc_Backward_Right_PWM, motorRightSpeed);
  analogWrite(13, b);

}
