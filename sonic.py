#!/usr/bin/env python

from threading import Thread
import Jetson.GPIO as GPIO
import time
import rospy
from std_msgs.msg import UInt32
from std_msgs.msg import UInt32MultiArray

GPIO.setmode(GPIO.BOARD)

class Sonic:
    def __init__(self, trigPin1 = None, echoPin1 = None, trigPin2 = None, echoPin2 = None, trigPin3 = None, echoPin3 = None):
        if trigPin1 != None:
            self.trigPin1 = trigPin1
            self.echoPin1 = echoPin1
            GPIO.setup(self.trigPin1, GPIO.OUT)
            GPIO.setup(self.echoPin1, GPIO.IN)
            print("-------Sonic1 ON-------")
        else:
            self.trigPin1 = None
            self.echoPin1 = None
            print("-------Sonic1 OFF!!!-------")
            
        if trigPin2 != None:
            self.trigPin2 = trigPin2
            self.echoPin2 = echoPin2
            GPIO.setup(self.trigPin2, GPIO.OUT)
            GPIO.setup(self.echoPin2, GPIO.IN)
            print("-------Sonic2 ON-------")
        else:
            self.trigPin2 = None
            self.echoPin2 = None
            print("-------Sonic2 OFF!!!-------")
            
        if trigPin3 != None:
            self.trigPin3 = trigPin3
            self.echoPin3 = echoPin3
            GPIO.setup(self.trigPin3, GPIO.OUT)
            GPIO.setup(self.echoPin3, GPIO.IN)
            print("-------Sonic3 ON-------")
        else:
            self.trigPin3 = None
            self.echoPin3 = None
            print("-------Sonic3 OFF!!!-------")
        
        
        self.pub = rospy.Publisher("/distance_array", UInt32MultiArray, queue_size=10)
        
    def start(self):
        thread = Thread(target=self.pub_distance, args=())
        thread.daemon = True
        thread.start()
        
        
    def gen_distance(self, trigPin, echoPin):
        GPIO.output(trigPin, False)
        time.sleep(0.000002)
        GPIO.output(trigPin, True)
        time.sleep(0.00001)
        GPIO.output(trigPin, False)
        startTime = time.time()
        stopTime = time.time()
            
        while GPIO.input(echoPin) == 0:
            startTime = time.time()
            
        while GPIO.input(echoPin) == 1:
            stopTime = time.time()
            
        duration = stopTime - startTime
        distance = (duration * 34300) / 2
        
        #time.sleep(0.1)
            
        return int(distance)
            
    def pub_distance(self):
        while not rospy.is_shutdown():
            if self.trigPin1 != None:
                result1 = self.gen_distance(self.trigPin1, self.echoPin1)
                print(result1)
            else:
                result1 = 0
                
            if self.trigPin2 != None:
                result2 = self.gen_distance(self.trigPin2, self.echoPin2)
            else:
                result2 = 0
                
            if self.trigPin3 != None:
                result3 = self.gen_distance(self.trigPin3, self.echoPin3)
            else:
                result3 = 0
            
            array_msg = UInt32MultiArray()
            array_msg.data = [int(result1), int(result2), int(result3)]
            #print(array_msg.data)
            self.pub.publish(array_msg)
            #print(array_msg)
            rate = rospy.Rate(2)
            rate.sleep()
        
