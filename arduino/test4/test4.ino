#include <ros.h>
#include <std_msgs/UInt32MultiArray.h>
#include <Servo.h>
Servo servoX;
Servo servoY;

ros::NodeHandle nh;

char seekBarL = 50;
char seekBarR = 50;
char buttonL = 1;
char buttonR = 1;
char stopButton = 0;
int xPos = 1;
int yPos = 1;

//Start_Relay
#define Relay 23
//Dc_forward_Left)1
#define Dc_Farward_Left_Dir 40
#define Dc_Farward_Left_PWM 12
//Dc_forward_Right)3
#define Dc_Farward_Right_Dir 42
#define Dc_Farward_Right_PWM 10
//Dc_backward_Left)2
#define Dc_Backward_Left_Dir 41
#define Dc_Backward_Left_PWM 13
//Dc_backward_Right)4
#define Dc_Backward_Right_Dir 43
#define Dc_Backward_Right_PWM 11
//Step_Left
#define dirPinLeft 37
#define stepPinLeft 34
#define enPinLeft 35
//Step_Right
#define dirPinRight 38
#define stepPinRight 39
#define enPinRight 36
//Camera_1
#define Camera_1 32
//Camera_2
#define Camera_2 28

#define stepDelay 500

void MotorData(const std_msgs::UInt32MultiArray& msg) {
  seekBarL = msg.data[0];
  seekBarR = msg.data[1];
  buttonL = msg.data[2];
  buttonR = msg.data[3];
  xPos = msg.data[4];
  yPos = msg.data[5];
  stopButton = msg.data[6];
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


ros::Subscriber<std_msgs::UInt32MultiArray> motordata("/motordata", &MotorData);

void setup() {
  // 9600, 19200, 38400, 57600, 74880, 115200, 230400, 250000, 500000, 1000000, 2000000
  nh.getHardware()->setBaud(115200);
  nh.initNode();
  nh.subscribe(motordata);
  pinMode(Relay, HIGH);
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
  pinMode(enPinLeft, LOW);
  pinMode(dirPinRight, OUTPUT);
  pinMode(stepPinRight, OUTPUT);
  pinMode(enPinRight, LOW);
  servoX.attach(Camera_1);
  servoY.attach(Camera_2);
  servoX.write(90);
  servoY.write(90);
}

void loop() {
  int motorLeftSpeed = 0;
  int motorRightSpeed = 0;
  
  nh.spinOnce();
  
  /////////////////////////////////////////////////// Emergency Stop
  if (stopButton == 1){
    digitalWrite(Relay, LOW);
  }
  else{
    digitalWrite(Relay, HIGH);
  }

  /////////////////////////////////////////////////// seekBarL
  if (seekBarL >= 50){
    digitalWrite(Dc_Farward_Left_Dir, HIGH);
    digitalWrite(Dc_Backward_Left_Dir, HIGH);
    motorLeftSpeed = abs(map(seekBarL, 50, 100, 0, 255));
  } else{
    digitalWrite(Dc_Farward_Left_Dir, LOW);
    digitalWrite(Dc_Backward_Left_Dir, LOW);
    motorLeftSpeed = abs(map(seekBarL, 0, 49, 255, 1));
  }

  /////////////////////////////////////////////////// seekbarR
  if (seekBarR >= 50){
    digitalWrite(Dc_Farward_Right_Dir, HIGH);
    digitalWrite(Dc_Backward_Right_Dir, HIGH);
    motorRightSpeed = abs(map(seekBarR, 50, 100, 0, 255));
  } else{
    digitalWrite(Dc_Farward_Right_Dir, LOW);
    digitalWrite(Dc_Backward_Right_Dir, LOW);
    motorRightSpeed = abs(map(seekBarR, 0, 49, 255, 1));
  }

  /////////////////////////////////////////////////// Step
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

  /////////////////////////////////////////////////// Cam 1

  servoX.write(xPos);
  delayMicroseconds(500);

  /////////////////////////////////////////////////// Cam 2

  servoY.write(yPos);
  delayMicroseconds(500);

  
  analogWrite(Dc_Farward_Left_PWM, motorLeftSpeed);
  analogWrite(Dc_Farward_Right_PWM, motorRightSpeed);
  analogWrite(Dc_Backward_Left_PWM, motorLeftSpeed);
  analogWrite(Dc_Backward_Right_PWM, motorRightSpeed);
}
