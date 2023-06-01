#!/usr/bin/env python

from flask import Flask, render_template, Response
from threading import Thread
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

app = Flask(__name__)
bridge = CvBridge()
pub = rospy.Publisher("camera/image", Image, queue_size=10)
image = None

def publish_image():
    global image
    cap = cv2.VideoCapture(0) # camera device number
    rate = rospy. Rate(10) # 10 Hz
    while not rospy.is_shutdown():
        if cv2.waitKey(1) == ord('q'):
            break
        ret, frame = cap.read() # read image from camera
        frame = cv2.resize(frame, (1500, 1000))
        cv2.imshow('USB Camera', frame)
        if ret:
            image_message = bridge.cv2_to_imgmsg(frame, encoding="bgr8") # Convert OpenCV image to ROS message
            #pub.publish(image_message) # publish a ROS message
            image = frame # save image
        rate. sleep()
    cap. release()

def generate():
    global image
    while True:
        if image is not None:
            ret, jpeg = cv2.imencode(".jpg", image) # Encode OpenCV image to JPEG format
            frame = jpeg.tobytes() # Convert to byte array
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n") # in multipart format send

@app.route("/")
def index():
    return render_template("index.html") # Render the web page template

@app.route("/video_feed")
def video_feed():
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame") # video stream response

if __name__ == "__main__":
    rospy.init_node("camera_flask_app")
    thread = Thread(target=publish_image)
    thread.daemon = True
    thread.start()
    app.run(host="192.168.0.141", port=8080, debug=True) # Run flask application
