#!/usr/bin/env python

import os
import argparse
import cv2
import numpy as np
import sys
import time
from threading import Thread
import importlib.util
import datetime
from queue import Queue
import rospy
from sensor_msg.msg import CompressedImage
# Define VideoStream class to handle streaming of video from webcam in separate processing thread
# Source - Adrian Rosebrock, PyImageSearch: https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/
class VideoStream:
    """Camera object that controls video streaming from the Picamera"""
    def __init__(self,cam_num,resolution=(640,480),framerate=30):
        # Initialize the PiCamera and the camera image stream
        self.stream = cv2.VideoCapture(cam_num)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3,resolution[0])
        ret = self.stream.set(4,resolution[1])
            
        # Read first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()

	# Variable to control when the camera is stopped
        self.stopped = False

    def start(self):
	# Start the thread that reads frames from the video stream
        thread = Thread(target=self.update, args=())
        thread.daemon = True
        thread.start()
        return self
    
    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return

            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
	# Return the most recent frame
        return self.frame

    def stop(self):
	# Indicate that the camera and thread should be stopped
        self.stopped = True

MODEL_NAME = 'Sample_TFLite_model'
GRAPH_NAME = 'F.tflite'
LABELMAP_NAME = 'labels.txt'
min_conf_threshold = float(0.6)
resW, resH = '1280', '720'
imW, imH = int(resW), int(resH)
#use_TPU = ''
use_TPU = 'store_true'

# Import TensorFlow libraries
# If tflite_runtime is installed, import interpreter from tflite_runtime, else import from regular tensorflow
# If using Coral Edge TPU, import the load_delegate library
pkg = importlib.util.find_spec('tflite_runtime')
if pkg:
    from tflite_runtime.interpreter import Interpreter
    if use_TPU:
        from tflite_runtime.interpreter import load_delegate
else:
    from tensorflow.lite.python.interpreter import Interpreter
    if use_TPU:
        from tensorflow.lite.python.interpreter import load_delegate

# If using Edge TPU, assign filename for Edge TPU model
#if use_TPU:
    # If user has specified the name of the .tflite file, use that name, otherwise use default 'edgetpu.tflite'
    #GRAPH_NAME = 'F_edgetpu.tflite'
    #GRAPH_NAME = 'detect.tflite'

# Get path to current working directory
CWD_PATH = os.getcwd()

# Path to .tflite file, which contains the model that is used for object detection
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,GRAPH_NAME)

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_NAME,LABELMAP_NAME)

# Load the label map
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Have to do a weird fix for label map if using the COCO "starter model" from
# https://www.tensorflow.org/lite/models/object_detection/overview
# First label is '???', which has to be removed.
if labels[0] == '???':
    del(labels[0])

# Load the Tensorflow Lite model.
# If using Edge TPU, use special load_delegate argument

if use_TPU:
    GRAPH_NAME = 'F_edgetpu.tflite'
    interpreter = Interpreter(model_path=PATH_TO_CKPT,
                              experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
    print(PATH_TO_CKPT)
else:
    interpreter = Interpreter(model_path=PATH_TO_CKPT)

interpreter.allocate_tensors()

# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

floating_model = (input_details[0]['dtype'] == np.float32)

input_mean = 127.5
input_std = 127.5


# Initialize video stream
#videostream = VideoStream(resolution=(imW,imH),framerate=30).start()

class DetectCam:
    #for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
    def __init__(self, num, fps, state=True):
        self.videostream = VideoStream(num, resolution=(imW,imH),framerate=fps).start()
        
        frame = cv2.imread("./static/cameraload.png")
        buffer = cv2.imencode('.png', frame)
        self.loadimg = buffer[1].tobytes()
        
        self.q = Queue()
        self.state = state
        print("-------DetectCamera-------")
        print("DetectCamera", num)
    
    def start(self):
        thread = Thread(target=self.gen_frames, args=())
        thread.daemon = True
        thread.start()
        return self
    
    def gen_frames(self):
        #for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
        while True:

            # Grab frame from video stream
            frame = self.videostream.read()
            
            #input_data change to GRAY
            frame_GRAY = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_rgb = cv2.cvtColor(frame_GRAY, cv2.COLOR_GRAY2RGB)
            frame_resized = cv2.resize(frame, (width, height))
            input_data = np.expand_dims(frame_resized, axis=0)

            # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
            if floating_model:
                input_data = (np.float32(input_data) - input_mean) / input_std

            # Perform the actual detection by running the model with the image as input
            interpreter.set_tensor(input_details[0]['index'],input_data)
            interpreter.invoke()

            # Retrieve detection results
            boxes = interpreter.get_tensor(output_details[1]['index'])[0] # Bounding box coordinates of detected objects
            classes = interpreter.get_tensor(output_details[3]['index'])[0] # Class index of detected objects
            scores = interpreter.get_tensor(output_details[0]['index'])[0] # Confidence of detected objects
            num = interpreter.get_tensor(output_details[2]['index'])[0]  # Total number of detected objects (inaccurate and not needed)
         
            # Loop over all detections and draw detection box if confidence izs above minimum threshold
            for i in range(len(scores)):
                if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):
                    
                    if labels[int(classes[i])] == 'person':
                        imH_1 = imH /720 * 120
                        imW_1 = imW /1280 * 160
                        
                        ymin = int(max(1,(boxes[i][0] * imH_1)))
                        xmin = int(max(1,(boxes[i][1] * imW_1)))
                        ymax = int(min(imH,(boxes[i][2] * imH_1)))
                        xmax = int(min(imW,(boxes[i][3] * imW_1)))
                    

                        cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 1)

                    # Draw label
                    object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
                    
                    if object_name == 'person':
                        
                        label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
                        labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1) # Get font size
                        label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
                        cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-7), (xmin+labelSize[0], label_ymin+baseLine-7), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
                        cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1) # Draw label text


            # All the results have been drawn on the frame, so it's time to display it.
            #frame = cv2.resize(frame, (imW,imH))
            #cv2.imshow('Object detector', frame)
            ret, buffer = cv2.imencode('.png', frame)
            frame = buffer.tobytes()
            self.q.put(b'--frame\r\n'b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')

            # Press 'q' to quit
            #if cv2.waitKey(1) == ord('q'):
            #    break
            
    def loading(self):
        return (b'--frame\r\n'b'Content-Type: image/png\r\n\r\n' + self.loadimg + b'\r\n')
    
    def set_state(self, state):
        self.state = state
    
    def clear_q(self):
        while(not self.q.empty()):
            self.q.get()
        #print("q_empty")   
        
    def get_q(self):
        return self.q.get()
# Clean up
#cv2.destroyAllWindows()
#videostream.stop()


