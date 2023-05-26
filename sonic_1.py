#!/usr/bin/env python

from threading import Thread
import Jetson.GPIO as GPIO
import time
import rospy
from std_msgs.msg import UInt32
from std_msgs.msg import UInt32MultiArray

# set up pin numbers for echo pin and trigger pins:
trigPin1 = 35
echoPin1 = 37

# set the modes for the trigger pin and echo pin:
GPIO.setmode(GPIO.BOARD)
GPIO.setup(trigPin1, GPIO.OUT)
GPIO.setup(echoPin1, GPIO.IN)

class Sonic:
    def __init__(self, trigPin1, echoPin1):
        self.trigPin1 = trigPin1
        self.echoPin1 = echoPin1
        
        #self.pub = rospy.Publisher("/distance_array", UInt32MultiArray, queue_size=10)
        
        print("-------Sonic-------")
        print("trigPin1", trigPin1)
          
        thread = Thread(target=self.gen_distance, args=())
        thread.daemon = True
        thread.start()
        
        while True:
            print("a")
            time.sleep(5)
        
        
    def gen_distance(self):
        while not rospy.is_shutdown():
            GPIO.output(self.trigPin1, False)
            time.sleep(0.000002)
            GPIO.output(self.trigPin1, True)
            time.sleep(0.00001)
            GPIO.output(self.trigPin1, False)
            startTime_1 = time.time()
            stopTime_1 = time.time()
            
            while GPIO.input(echoPin1) == 0:
                startTime_1 = time.time()
            
            while GPIO.input(echoPin1) == 1:
                stopTime_1 = time.time()
            
            duration_1 = stopTime_1 - startTime_1
            distance_1 = (duration_1 * 34300) / 2
            
            print("Distance: %.1f cm" % distance_1)
            
            time.sleep(0.1)
           
            ########################################################
            #array_msg = UInt32MultiArray()
            #array_msg.data = [distance_1]
            #self.pub.publish(array_msg)
            #rate.sleep()
            
            
            