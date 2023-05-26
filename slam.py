#!/usr/bin/env python

from flask import Flask, render_template, Response
from threading import Thread
import rospy
from nav_msgs.msg import OccupancyGrid
import numpy as np
import cv2

class Slam:
    
    def __init__(self):
        #rospy.init_node("map_viewer")
        rospy.Subscriber("/map", OccupancyGrid, self.map_callback)
        print("-------SLAM_THREAD-------")
        
        
    def start(self):
        thread = Thread(target=self.gen_frame, args=())
        thread.daemon = True
        thread.start()
        
        
    def map_callback(self, msg):
        global np_data
        np_data = np.array(msg.data, dtype=np.int8).reshape((msg.info.height, msg.info.width))

        np_data = np.interp(np_data, (-1, 100), (255, 0)).astype(np.uint8)
        
        
    def gen_frame(self):
        while True:
            if cv2.waitKey(1) == ord('q'):
                break
            #cv2.imshow("Map", np_data)
            frame = cv2.resize(np_data, (1440, 870))
            ret, jpeg = cv2.imencode(".jpg", frame)
            frame = jpeg.tobytes() # Convert to byte array
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")
            