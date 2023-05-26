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

#define cameraStep 4
int xState = 90;
int yState = 90;
#define xMax 180
#define xMin 0
#define yMax 180
#define yMin 0


void setup() {
  servoX.attach(Camera_1);
  servoY.attach(Camera_2);
}

void loop() {

  servoX.write(90);
  delayMicroseconds(500);
}
