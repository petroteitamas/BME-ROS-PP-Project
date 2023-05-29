#!/usr/bin/env python3
import rospy
import math
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from std_msgs.msg import Float32


#Length of the robot arms
a1 = 0.29 #Length of the link1
a2 = 0.26 #Length of the link2


rospy.init_node('send_joint_angles')
pub = rospy.Publisher('/arm_controller/command', JointTrajectory, queue_size=1)
controller_name = "arm_controller"
joint_names = rospy.get_param("/%s/joints" % controller_name)
rospy.loginfo("Joint names: %s" % joint_names)
rate = rospy.Rate(2)

trajectory_command = JointTrajectory()
trajectory_command.joint_names = joint_names
point = JointTrajectoryPoint()


def IKIN(x, y, a1, a2):
    #print("x:", x, "y:", y, "a1:", a1, "a2:", a2)
    if(math.sqrt(x**2 + y**2) < a1 + a2):
        q2 = math.acos((x**2+y**2-a1**2-a2**2)/(2*a1*a2))
        q1 = math.atan2(y,x)-math.atan2((a2*math.sin(q2)),(a1+a2*math.cos(q2)))
        return q1-math.pi/2, q2, 1
    return 0, 0, 0


def publishIKIN_coords(msg):
    x = msg.positions[0]
    y = msg.positions[1]
    z = msg.positions[2]
    mp1 = msg.positions[4]
    mp2 = msg.positions[5]
    #print("Sub x:", x, "y:", y, "z:", z)

    q1, q2, ok = IKIN(x, y, a1, a2)

    # Axis 4 beállítása
    q4 = math.pi/2-q1-q2
    print("q1:", q1, "q2:", q2, "q3:", z, "q4:", q4, "mp1:", mp1, "mp2:", mp2)

    point.positions = [q1, q2, z, q4, mp1, mp2]
    point.velocities = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    point.time_from_start = rospy.rostime.Duration(2)
    trajectory_command.points = [point]




rospy.Subscriber("bme_robot_coordinates", JointTrajectoryPoint, publishIKIN_coords, queue_size=100) 

while not rospy.is_shutdown():
    trajectory_command.header.stamp = rospy.Time.now()
    pub.publish(trajectory_command)
    rate.sleep()
    