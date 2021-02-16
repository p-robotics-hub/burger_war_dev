#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import cv2

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

# # in progress
from xxxx import ViewInfo

from ColorExtractor import ColorExtractor


class ImageProcessor:
    def __init__(self, image):

        # publisher
        self.view_info_pub = rospy.Publisher('view_info', ViewInfo, queue_size=1)
        self.view_info = ViewInfo()

        # image subscriber
        self.image_sub = rospy.Subscriber('image_raw', Image, self.imageCallBack)
        self.cv_bridge = CvBridge()

        self.color_extractor = ColorExtractor()

    def imageCallBack(self, data):

        try:
            self.img = self.cv_bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

    def getViewInfo(self):
        self.view_info.enemy.direction = self.getEnemyDirection()
        self.view_info.enemy.targer_derection = self.getEnemyTargetDirections()
        self.view_info.wall_target.directions = self.getWallTargetDirections()
        self.view_info.hole.direction = self.getHoleDirections()
    
    def getEnemyDirection(self) -> float:
        pass

    def getEnemyTargetDirections(self) -> list(float):
        pass
        
    def getWallTargetDirections(self) -> list(float):
        pass

    def getHoleDirections(self) -> list(float):
        pass

    def strategy(self):
        r = rospy.Rate(1) # change speed 1fps

        while not rospy.is_shutdown():
            view_info = self.getViewInfo()
            print(view_info)
            self.view_info_pub.publish(view_info)

            r.sleep()

if __name__ == '__main__':
    rospy.init_node('image_processor')
    img_proc = ImageProcessor('Imageprocessor')
    img_proc.strategy()