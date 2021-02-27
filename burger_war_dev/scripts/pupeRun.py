#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
import rospy

from naviBasic import NaviBasic
# from naviAttack import NaviAttack

# from modeDecider import getActMode


class ActMode(Enum):
    basic = 1
    attack = 2


class PupeBot():
    def __init__(self, bot_name="NoName"):
        # bot name 
        self.name = bot_name
        # mode
        self.mode = ActMode.basic
        self.navi = NaviBasic()

    def decide_mode(self):
        # self.mode = getActMode()
        if self.mode==ActMode.basic:
            self.navi = NaviBasic()
        # elif self.mode==ActMode.attack:
        #     self.navi = NaviAttack()

    def strategy(self):
        r = rospy.Rate(5)

        while not rospy.is_shutdown():
            self.decide_mode()
            self.navi.main()
            r.sleep()


if __name__ == '__main__':
    rospy.init_node('pupe_run')
    bot = PupeBot('Puperun')
    bot.strategy()
