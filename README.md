# jetson_nano_smart
```
https://github.com/addpipe/simple-recorderjs-demo
```

# first
```
sudo apt autoremove

sudo apt update
sudo apt upgrade

sudo apt install terminator

sudo apt install thonny
```

# install ROS
```
sudo apt update
sudo apt upgrade

sudo apt-key del 421C365BD9FF1F717815A3895523BAEEB01FA116
sudo -E apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-get update
sudo apt-get install ros-melodic-desktop-full
sudo apt-get install python-rosdep
sudo rosdep init
rosdep update
echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
source ~/.bashrc

sudo apt-get install python-catkin-tools

```
```
mkdir -p ~/catkin_ws/src
catkin_make
cd ~/catkin_ws/src
catkin_init_workspace
cd ~/catkin_ws/
catkin buildcatkin_create_pkg smart rospy roscpp std_msgs
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc
```
```
//in bashrc
//if Wifi = smart2.4G
export ROS_HOSTNAME=192.168.0.141
export ROS_MASTER_URI=htcatkin_maketp://192.168.0.141:11311
```

# make ros package
```
//catkin_create_pkg <package_name> [dependencies]
cd ~/catkin_ws/src
catkin_create_pkg smart rospy roscpp std_msgs
cd ~/catkin_ws
//delete bulid and devel files in catkin_ws
catkin_make
```


# how to start
bashrc, static/roslisb2.js, launch/websoket.launch

roscore

rosrun smart stereoDetect_ORG.py	or	rosrun smart stereoDetect_SMART.py

rosrun smart main.py	or	rosrun smart main_smart.py

rosrun rosserial_arduino serial_node.py _port:=/dev/ttyACM0 _baud:=115200

sudo chmod 666 /dev/ttyACM0 

cd catkin_ws/src/smart/

rosrun smart main_slam.py	or	rosrun smart main_slam_SMART.py

roslaunch rosbridge_server rosbridge_websocket.launch

roslaunch ydlidar_ros_driver TX.launch

source /opt/ros/noetic/setup.bash
source ~/ydlidar_ws/devel/setup.bash
roslaunch hector_slam_launch tutorial.launch

cd ~

#avrdude -C /etc/avrdude.conf -v -patmega328p -carduino -P/dev/ttyACM0 -b115200 -D -Uflash:w:/#home/khw/catkin_ws/src/smart/arduino/test2/test2.ino 

source ~/ydlidar_ws/devel/setup.bash
source ~/catkin_ws/devel/setup.bash

   #smart 2.4G
export ROS_HOSTNAME=192.168.0.141
e xport ROS_MARSTER_URI=http://192.168.0.141:11311


#현우의 핫스팟
export ROS_HOSTNAME=192.168.70.200
export ROS_MARSTER_URI=http://192.168.70.200:11311

killall -9 rosmaster
