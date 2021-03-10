#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy

from naviBasic import NaviBasic
from naviAttack import NaviAttack

from ModeDecider import ModeDecider

# from burger_war_dev.msg import ImgInfo, WarState
from obstacle_detector.msg import Obstacles

from ActMode import ActMode

class PupeBot():
    def __init__(self, bot_name="NoName"):
        # bot name 
        self.name = bot_name
        # mode
        self.mode = ActMode.basic
        self.mode_prev = ActMode.basic
        self.navi = NaviBasic()
        self.modeDecider = ModeDecider()

        # img_info subscriber
        # self.imgInfo_sub = rospy.Subscriber('/img_info', ImgInfo, self.imgInfoCallBack)
        # self.imgInfo = None

        # WarState subscriber
        # self.warState_sub = rospy.Subscriber('/war_state', WarState, self.warStateCallBack)
        # self.warState = None

        # rospy.Timer(rospy.Duration(0.1), self.selectModeCallBack)

        # obstacles subscriber
        self.obstacles_sub = rospy.Subscriber('/raw_obstacles', Obstacles, self.imgInfoCallBack)

    def imgInfoCallBack(self, data):
        # print(data)
        self.imgInfo = data
    
    def warStateCallBack(self, data):
        self.warState = data
    
    def obstacleCallback(self, data):
        print("obstacle")
        print(data)

    def selectModeCallBack(self, state):
        print(self.imgInfo)
        if (self.imgInfo is not None) and (self.warState is not None):
            self.mode = self.modeDecider.getActMode(self.mode, self.imgInfo, self.warState)
        print(self.mode)
        if self.mode != self.mode_prev:
            if self.mode==ActMode.basic:
                self.navi = NaviBasic()
            elif self.mode==ActMode.attack:
                self.navi = NaviAttack()
        
        self.mode_prev = self.mode

    def strategy(self):
        r = rospy.Rate(5)

        while not rospy.is_shutdown():
            self.navi.main()
            r.sleep()


if __name__ == '__main__':
    rospy.init_node('pupe_run')
    bot = PupeBot('Puperun')
    bot.strategy()
