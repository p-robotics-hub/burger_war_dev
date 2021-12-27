#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import rosbag
from geometry_msgs.msg import Twist


class RosbagLogger:
    def __init__(self, name):
        self.name = name
        self.bag = rosbag.Bag('test.bag', 'w')

        self.log = Twist()

        # topic subscribers
        self.cmd_vel_sub = rospy.Subscriber('/cmd_vel', Twist, self.logCallBack)
        

    def logCallBack(self, data):
        self.log = data

    def strategy(self):
        r = rospy.Rate(10) # change speed 1fps

        while not rospy.is_shutdown():
            self.bag.write('cmd_vel', self.log)
            r.sleep()
        self.bag.close()

if __name__ == '__main__':
    rospy.init_node('rosbag_logger')
    rosbag_logger = RosbagLogger('rosbag_logger')
    rosbag_logger.strategy()