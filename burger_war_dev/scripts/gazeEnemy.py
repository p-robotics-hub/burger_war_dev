#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy

from geometry_msgs.msg import Twist
from burger_war_dev.msg import ImgInfo


class GazeEnemyBot():
    def __init__(self):

        # velocity publisher
        self.vel_pub = rospy.Publisher('cmd_vel', Twist,queue_size=1)

        # img_info subscriber
        self.imgInfo_sub = rospy.Subscriber('/img_info', ImgInfo, self.imgInfoCallBack)
        self.imgInfo_data = None

    def imgInfoCallBack(self, data):
        print(data)
        self.imgInfo_data = data

    def calcTwist(self):
        th = -self.imgInfo_data.enemy_direct*0.03
        twist = Twist()
        twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = th
        return twist

    def main(self):
        r = rospy.Rate(5)

        while not rospy.is_shutdown():
            twist = self.calcTwist()
            print(self.mode)
            self.vel_pub.publish(twist)

            r.sleep()
