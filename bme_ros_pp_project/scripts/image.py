#!/usr/bin/env python3

# For debug purpose

from __future__ import print_function

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

class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("image_topic_2",Image)

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
    
    points = {"red":red_coords, "green":green_coords}
    print(points)

    cv2.imshow("Image", cv_image)
    cv2.imshow("Image red_opened", red_opened)
    cv2.imshow("Image green_opened", green_opened)
    cv2.waitKey(3)
    #self.image_sub.unregister()
    


def main(args):
  rospy.sleep(3.0)
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:

    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)