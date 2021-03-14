#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy

from geometry_msgs.msg import Twist
from burger_war_dev.msg import ImgInfo, WarState, ScanInfo


class NaviAttack2():
    def __init__(self):
        # subscliber
        self.scanInfo_sub = rospy.Subscriber('scan_enemy_pose', ScanInfo, self.scanInfoCallBack)
        self.scanInfo = ScanInfo()
        self.imgInfo_sub = rospy.Subscriber('img_info', ImgInfo, self.imgInfoCallBack)
        self.imgInfo = ImgInfo()

        # velocity publisher
        self.vel_pub = rospy.Publisher('cmd_vel', Twist,queue_size=1)

    def scanInfoCallBack(self, data):
        self.scanInfo = data
    
    def imgInfoCallBack(self, data):
        self.imgInfo = data
    
    def calcTwist(self):
        twist = Twist()
        twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0

        if self.imgInfo.is_enemy_marker_recognized:
            twist.angular.z = -0.1*self.imgInfo.enemy_marker_direct
        else:
            if self.scanInfo.enemy_direct>0:
                twist.angular.z = 0.5
            else:
                twist.angular.z = -0.5
        twist.linear.x = self.scanInfo.enemy_dist - 0.6
        return twist

    def main(self):
        print("naviAttack2")
        twist = self.calcTwist()
        self.vel_pub.publish(twist)
