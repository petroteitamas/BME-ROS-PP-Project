#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32  # Message type used in the node
from trajectory_msgs.msg import JointTrajectoryPoint

rospy.init_node('publisher')    # Init the node with name "publisher"
pub = rospy.Publisher('bme_robot_coordinates', JointTrajectoryPoint, queue_size=1)
rate = rospy.Rate(2)

def xyzw(x, y, z, w):
    point = JointTrajectoryPoint()
    point.positions = [x, y, z, 0.0, 0.0, 0.0]
    point.velocities = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    point.time_from_start = rospy.rostime.Duration(2)
    pub.publish(point)


#pub_xyzw = rospy.Publisher('publisher_topic', Float32, queue_size=1)
rospy.loginfo("Publisher Python node has started and publishing data on publisher_topic")



while not rospy.is_shutdown():  # Run the node until Ctrl-C is pressed
    xyzw(-0.3, 0.3, -0.1, 0)

    rate.sleep()                # The loop runs at 1Hz