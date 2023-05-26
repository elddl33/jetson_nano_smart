#!/usr/bin/env python

import rospy
from sensor_msgs.msg import CompressedImage
import Queue as queue
import cv2

def image_publisher():
    # Initialize the ROS node
    rospy.init_node('image_publisher', anonymous=True)

    # Create a publisher for the compressed image topic
    pub = rospy.Publisher('/camera1', CompressedImage, queue_size=10)

    # Create a queue to store the images
    image_queue = queue.Queue(maxsize=10)

    # Open the camera
    cap = cv2.VideoCapture(0)

    while True:
        # Capture an image from the camera
        ret, frame = cap.read()
        cv2.imshow('USB Camera', frame)
        if cv2.waitKey(1) == ord('q'):
                break

        if ret:
            # Convert the image to JPEG format and compress it
            jpeg_data, _ = cv2.imencode('.jpg', frame)
            if type(jpeg_data) == bool:
                print("FUCK")
            compressed_data = jpeg_data.tobytes()

            # Create a CompressedImage message and publish it
            msg = CompressedImage()
            msg.header.stamp = rospy.Time.now()
            msg.format = 'jpeg'
            msg.data = compressed_data
            pub.publish(msg)
            print(msg)

            # Add the image to the queue
            image_queue.put(frame)

            # Remove the oldest image from the queue if it's full
            if image_queue.full():
                image_queue.get()

    # Release the camera and shutdown the node when done
    cap.release()
    rospy.signal_shutdown('Done')


if __name__ == '__main__':
    try:
        image_publisher()
    except rospy.ROSInterruptException:
        pass
