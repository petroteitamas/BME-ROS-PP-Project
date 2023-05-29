#!/usr/bin/env python3

# For debug purpose


import rospy
from std_msgs.msg import Float32  # Message type used in the node
from trajectory_msgs.msg import JointTrajectoryPoint

rospy.init_node('publisher')    # Init the node with name "publisher"
pub = rospy.Publisher('bme_robot_coordinates', JointTrajectoryPoint, queue_size=1)
rate = rospy.Rate(0.5)

def xyzw(x, y, z, w, mp1, mp2):
    point = JointTrajectoryPoint()
    point.positions = [x, y, z, 0.0, mp1, mp2]
    point.velocities = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    point.time_from_start = rospy.rostime.Duration(2)
    pub.publish(point)


#pub_xyzw = rospy.Publisher('publisher_topic', Float32, queue_size=1)
rospy.loginfo("Publisher Python node has started and publishing data on publisher_topic")


rospy.sleep(3.0)
xyzw(0.375, 0.2, 0, 0, 0.06, 0.06)
 
    

while not rospy.is_shutdown():  # Run the node until Ctrl-C is pressed
    #xyzw(-0.375, 0.375, 0, 0, 0, 0)
    #xyzw(-0.375, 0.375, -0.04, 0, 0, 0)        
    #xyzw(-0.375, 0.375, -0.04, 0, 0.06, 0.06)
    #xyzw(0.375, 0.2, 0, 0, 0.06, 0.06)    
       
    rate.sleep()
    