#!/usr/bin/env python3
from __future__ import print_function

from std_msgs.msg import Float32  # Message type used in the node
from trajectory_msgs.msg import JointTrajectoryPoint
import roslib
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np

from skimage import data
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import label2rgb
from skimage.color import rgb2gray


rospy.init_node('bme_image_process')
pub = rospy.Publisher('bme_robot_coordinates', JointTrajectoryPoint, queue_size=1)
rate = rospy.Rate(0.5)


place_pose = {"red":(0.05, 0.3, 0.1), "green":(0.05, 0.4, 0.1)} # X, Y, increment
gripper = {"close": -0.016, "open": 0.01}
pp_height = -0.04 #Height of the cube




cube_pose = None
cube_is_ready = False

def xyzw(x, y, z, w, mp1, mp2):
    point = JointTrajectoryPoint()
    point.positions = [x, y, z, 0.0, mp1, mp2]
    point.velocities = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    point.time_from_start = rospy.rostime.Duration(2)
    pub.publish(point)


class image_converter:
  def __init__(self):
    #self.image_pub = rospy.Publisher("image_topic_2",Image, queue_size=1)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("table_camera/image_raw",Image,self.callback)
  # Kép koordinátákat kap
  # Visszaadja a robothoz képesti XY koordinátákat
  def camera2xy(self, px, py):
    camera_x = -0.275
    camera_y = 0.275
    
    W = 640
    H = 480
    scale_x = 1
    scale_y = 1
    x = ((px-W/2)*scale_x) / 1000 + camera_x
    y = ((H/2-py)*scale_y) / 1000 + camera_y

    return x, y
    #input: [[140.0, 320.0], [240.0, 320.0]]

  def callback(self,data):
    global cube_is_ready
    global cube_pose
    # Convert ROS data to CV2
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)
    #Process the image with cv2
    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    
    green_min = np.array([50, 100, 100])
    green_max = np.array([70, 255, 255])
    # preparing the mask to overlay
    mask_green = cv2.inRange(hsv, green_min, green_max)
    red_min = np.array([0, 70, 50])
    red_max = np.array([10, 255, 255])
    # preparing the mask to overlay
    mask_red = cv2.inRange(hsv, red_min, red_max)


    kernel = np.ones((5,5),np.uint8)
    red_opened = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
    green_opened = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)



    #green_count, green_markers = cv2.connectedComponents(red_opened)
    #red_count, red_markers = cv2.connectedComponents(green_opened)


    #Red
    label_image = label(red_opened)
    red_coords=list()
    for region in regionprops(label_image):
      if region.area >= 100:
        minr, minc, maxr, maxc = region.bbox
        py = (minr+maxr)/2
        px = (minc+maxc)/2
        x, y = self.camera2xy(px, py)
        red_coords.append((x, y))
        
    #Green
    label_image = label(green_opened)
    green_coords=list()
    for region in regionprops(label_image):
      if region.area >= 100:
        minr, minc, maxr, maxc = region.bbox
        py = (minr+maxr)/2
        px = (minc+maxc)/2
        x, y = self.camera2xy(px, py)
        green_coords.append((x, y))
    
    cube_pose = {"red":red_coords, "green":green_coords}
    print(cube_pose)
    
    #cv2.imshow("Image markers", markers)
    #cv2.imshow("Image red_opened", red_opened)
    #cv2.imshow("Image green_opened", green_opened)
    #cv2.waitKey(3)
    cube_is_ready = True
    self.image_sub.unregister()
    

rospy.sleep(3.0)
ic = image_converter()

while not rospy.is_shutdown():  # Run the node until Ctrl-C is pressed
    if cube_is_ready == True:
        cube_is_ready = False
        red_cubes = cube_pose["red"]
        green_cubes = cube_pose["green"]

        # Red cube PP
        for i in range(0, len(red_cubes)):
            # Pick
            # -> approach
            xyzw(red_cubes[i][0], red_cubes[i][1], 0, 0, gripper["open"], gripper["open"])
            rospy.sleep(5.0)
            # -> pick pose
            xyzw(red_cubes[i][0], red_cubes[i][1], pp_height, 0, gripper["open"], gripper["open"])
            rospy.sleep(5.0)
            # -> close the gripper
            xyzw(red_cubes[i][0], red_cubes[i][1], pp_height, 0, gripper["close"], gripper["close"])
            rospy.sleep(5.0)
            # -> approach point with cube
            xyzw(red_cubes[i][0], red_cubes[i][1], 0, 0, gripper["close"], gripper["close"])
            rospy.sleep(5.0)




            #place
            # -> approach
            place_x = place_pose["red"][0] + i * place_pose["red"][2]
            place_y = place_pose["red"][1]
            xyzw(place_x, place_y, 0, 0, gripper["close"], gripper["close"])
            rospy.sleep(5.0)
            # -> place pose
            xyzw(place_x, place_y, pp_height, 0, gripper["close"], gripper["close"])
            rospy.sleep(5.0)
            # -> open the gripper
            xyzw(place_x, place_y, pp_height, 0, gripper["open"], gripper["open"])
            rospy.sleep(5.0)
            # -> approach point without cube
            xyzw(place_x, place_y, 0, 0, gripper["open"], gripper["open"])
            rospy.sleep(5.0)


        # Green cube PP
        for i in range(0, len(green_cubes)):
            # Pick
            # -> approach
            xyzw(green_cubes[i][0], green_cubes[i][1], 0, 0, gripper["open"], gripper["open"])
            rospy.sleep(5.0)
            # -> pick pose
            xyzw(green_cubes[i][0], green_cubes[i][1], pp_height, 0, gripper["open"], gripper["open"])
            rospy.sleep(5.0)
            # -> close the gripper
            xyzw(green_cubes[i][0], green_cubes[i][1], pp_height, 0, gripper["close"], gripper["close"])
            rospy.sleep(5.0)
            # -> approach point with cube
            xyzw(green_cubes[i][0], green_cubes[i][1], 0, 0, gripper["close"], gripper["close"])
            rospy.sleep(5.0)


            #place
            # -> approach
            place_x = place_pose["green"][0] + i * place_pose["green"][2]
            place_y = place_pose["green"][1]
            xyzw(place_x, place_y, 0, 0, gripper["close"], gripper["close"])
            rospy.sleep(5.0)
            # -> place pose
            xyzw(place_x, place_y, pp_height, 0, gripper["close"], gripper["close"])
            rospy.sleep(5.0)
            # -> open the gripper
            xyzw(place_x, place_y, pp_height, 0, gripper["open"], gripper["open"])
            rospy.sleep(5.0)
            # -> approach point without cube
            xyzw(place_x, place_y, 0, 0, gripper["open"], gripper["open"])
            rospy.sleep(5.0)




    xyzw(0, 0.54, 0, 0, 0.06, 0.06)
    rospy.sleep(5.0)

    rate.sleep()
