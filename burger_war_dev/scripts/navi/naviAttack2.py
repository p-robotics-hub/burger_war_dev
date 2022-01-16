#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy

from geometry_msgs.msg import Twist
from burger_war_dev.msg import ImgInfo, WarState, ScanInfo


class NaviAttack2():
    def __init__(self):
        
        self.vel_kp = 1
        self.vel_kv = 1
        self.ang_kp = 1
        self.ang_kv = 1
        
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
            twist.angular.z = self.ang_kp*self.scanInfo.enemy_direct
    
        twist.linear.x = self.vel_kp*(self.scanInfo.enemy_dist - 0.5) + self.vel_kv*twist.linear.x
        print('enemy_dist:', self.scanInfo.enemy_dist)
        print('enemy_direction:', self.scanInfo.enemy_direct)
        print('vel_x:', twist.linear.x)
        print('omega:', twist.angular.z)
        return twist

    def main(self):
        print("naviAttack")
        twist = self.calcTwist()
        self.vel_pub.publish(twist)
