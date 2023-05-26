#!/usr/bin/env python

import Jetson.GPIO as GPIO
import time
import rospy
from std_msgs.msg import UInt32
from std_msgs.msg import UInt32MultiArray

# set up pin numbers for echo pin and trigger pins:
trigPin1 = 35
echoPin1 = 37
trigPin2 = 38
echoPin2 = 40

# set the modes for the trigger pin and echo pin:
GPIO.setmode(GPIO.BOARD)
GPIO.setup(trigPin1, GPIO.OUT)
GPIO.setup(echoPin1, GPIO.IN)
GPIO.setup(trigPin2, GPIO.OUT)
GPIO.setup(echoPin2, GPIO.IN)                     

try:
    while True:
        # take the trigger pin low to start a pulse:
        GPIO.output(trigPin1, False)
        # delay 2 microseconds:
        time.sleep(0.000002)
        # take the trigger pin high:
        GPIO.output(trigPin1, True)
        # delay 10 microseconds:
        time.sleep(0.00001)
        # take the trigger pin low again to complete the pulse:
        GPIO.output(trigPin1, False)
        # listen for a pulse on the echo pin:
        startTime = time.time()
        stopTime = time.time()
        
        # save start time
        while GPIO.input(echoPin1) == 0:
            startTime = time.time()
        
        # save time of arrival
        while GPIO.input(echoPin1) == 1:
            stopTime = time.time()
        
        # calculate the distance in cm.
        #Sound travels approx.0.0343 microseconds per cm.,
        # and it's going to the target and back (hence the /2):
        duration = stopTime - startTime
        distance = (duration * 34300) / 2
        
        print("Distance: %.1f cm" % distance)
        
        # a short delay between readings:
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()