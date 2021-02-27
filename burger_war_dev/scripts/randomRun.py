#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This is rumdom run node.
subscribe No topcs.
Publish 'cmd_vel' topic. 
mainly use for simple sample program

by Takuya Yamaguhi.
'''

import rospy

from geometry_msgs.msg import Twist

from naviBasic import NaviBasic

class RandomBot():
    def __init__(self, bot_name="NoName"):
        # bot name 
        self.name = bot_name
        # velocity publisher
        self.vel_pub = rospy.Publisher('cmd_vel', Twist,queue_size=1)

        self.BasicMode = NaviBasic()

    def strategy(self):
        r = rospy.Rate(1) # change speed 1fps

        while not rospy.is_shutdown():
            self.BasicMode.main()
            r.sleep()


if __name__ == '__main__':
    rospy.init_node('random_run')
    bot = RandomBot('Random')
    bot.strategy()

