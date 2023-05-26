#!/usr/bin/env python

import Jetson.GPIO as GPIO
from flask import Flask, render_template, session, request, Response
from std_msgs.msg import UInt32MultiArray
from std_msgs.msg import UInt32
from threading import Thread
import Jetson.GPIO as GPIO
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import camera
import slam
import sonic
#import yolov5_detect
import time
import serial

time.sleep(5)

# Flask_server
app = Flask(__name__)
bridge = CvBridge()

global count
count = 0

#camera
camera.Camera(0).start() ##RGB_Cam
#cameras.append(yolov5_detect.Fire_Camera(0).start()) ##Thermal_Cam



print("--------------------------")
    

def callback_rosdata(msg):
    global count
    rosdata = msg.data
    #print(msg.data)
    if count == 0:
        #sonic
        sonic.Sonic(35, 37).start()
        count = 1

@app.route("/")
def index():
    return render_template("index.html")
    #return render_template("index_slam.html") # Render the web page template

#RGB_camera
@app.route('/RGB_video_feed')
def RGB_video_feed():
    return Response(camera.Camera(0).gen_frame(), mimetype="multipart/x-mixed-replace; boundary=frame") # video stream response

#Fire_camera
#@app.route('/Fire_video_feed')
#def Fire_video_feed():
#    return Response(yolov5_detect.Fire_Camera(0).run(), mimetype="multipart/x-mixed-replace; boundary=frame") # video stream response

#Slam
#@app.route('/Slam_feed')
#def Slam_feed():
#    return Response(slam.Slam().gen_frame(), mimetype="multipart/x-mixed-replace; boundary=frame") # video stream response


if __name__ == '__main__':
    try:
        rospy.init_node('ros_python_arduino', anonymous=True)
        rospy.Subscriber('/motordata', UInt32MultiArray, callback_rosdata)
        #app.run(host="192.168.0.141", port=8080, debug=True)
        app.run(host="192.168.70.200", port=8080, debug=True)
        pass
                
    except:
        print("error")
        GPIO.cleanup()
        
