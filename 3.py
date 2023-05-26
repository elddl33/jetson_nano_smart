#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from flask import Flask, Response

app = Flask(__name__)

# ROS callback to handle incoming image messages
def image_callback(msg):
    # Convert the ROS Image message to an OpenCV image
    bridge = CvBridge()
    img = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

    # Update the global image variable for Flask to use
    global latest_image
    latest_image = img

# Flask route to serve the image
@app.route('/')
def image():
    # Get the latest image from the global image variable
    global latest_image
    img = latest_image

    # Convert the image to JPEG format
    ret, jpeg = cv2.imencode('.jpg', img)
    if ret:
        # Return the JPEG image as response
        return Response(jpeg.tobytes(), content_type='image/jpeg')
    else:
        return 'Image not found'

if __name__ == '__main__':
    # Initialize ROS node and image publisher
    rospy.init_node('image_publisher', anonymous=True)
    img_pub = rospy.Publisher('image', Image, queue_size=10)
    rospy.Subscriber('image', Image, image_callback)

    # Start Flask web server
    latest_image = None
    app.run(host='192.168.0.141', port=8080)  # Run the server on all available network interfaces, on port 8080
