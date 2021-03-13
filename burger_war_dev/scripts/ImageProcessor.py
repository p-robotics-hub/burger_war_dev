#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import cv2
from burger_war_dev.msg import ImgInfo
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

from EnemyRecognizer import EnemyRecognizer


class ImageProcessor:
    def __init__(self, name):
        self.name = name

        # publisher
        self.img = None
        self.imgInfo_pub = rospy.Publisher('img_info', ImgInfo, queue_size=1)
        self.imgInfo = ImgInfo()

        # image subscriber
        self.image_sub = rospy.Subscriber('/image_raw', Image, self.imageCallBack)
        self.cv_bridge = CvBridge()

    def imageCallBack(self, data):
        try:
            self.img = self.cv_bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
        enem_rec = EnemyRecognizer(self.img)
        if enem_rec.isEnemyRecognized:
            self.imgInfo.is_enemy_recognized = True
            self.imgInfo.enemy_dist = enem_rec.calcDistance()
            self.imgInfo.enemy_direct = enem_rec.calcDirection()
        else:
            self.imgInfo.is_enemy_recognized = False
            self.imgInfo.enemy_dist = 0
            self.imgInfo.enemy_direct = 0

        if enem_rec.isEnemyMarkerRecognized:
            self.imgInfo.is_enemy_marker_recognized = True
            self.imgInfo.enemy_marker_direct = enem_rec.calcMarkerDirection()
        else:
            self.imgInfo.is_enemy_marker_recognized = False
            self.imgInfo.enemy_marker_direct = 0
        # self.getImgInfo()

    # def getImgInfo(self):
    #     enem_rec = EnemyRecognizer(self.img)
    #     self.img_info.enemy_dist = int(enem_rec.calcDistance())
    #     self.img_info.enemy_direct = int(enem_rec.calcDirection())
        # self.view_info.enemy.targer_derection = self.getEnemyTargetDirections()
        # self.view_info.wall_target.directions = self.getWallTargetDirections()
        # self.view_info.hole.direction = self.getHoleDirections()
    
    def getEnemyDirection(self):
        pass

    def getEnemyMarkerDirections(self):
        pass
        
    def getWallTargetDirections(self):
        pass

    def getHoleDirections(self):
        pass

    def strategy(self):
        r = rospy.Rate(10) # change speed 10fps

        while not rospy.is_shutdown():
            self.imgInfo_pub.publish(self.imgInfo)
            # print(self.img_info)
            r.sleep()

if __name__ == '__main__':
    rospy.init_node('image_processor')
    img_proc = ImageProcessor('ImageProcessor')
    img_proc.strategy()
