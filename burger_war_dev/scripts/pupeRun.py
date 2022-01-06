#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy

from navi.naviBasic import NaviBasic
from navi.naviAttack import NaviAttack
from navi.naviAttack2 import NaviAttack2

from ModeDecider import ModeDecider

from burger_war_dev.msg import ImgInfo, WarState, ScanInfo
# from obstacle_detector.msg import Obstacles

from ActMode import ActMode

class PupeBot():
    def __init__(self, bot_name="NoName"):
        # bot name 
        self.name = bot_name
        # mode
        self.mode = ActMode.basic
        self.mode_prev = ActMode.basic
        self.modeDecider = ModeDecider()

        #initialize navis
        self.navi_basic = NaviBasic()
        self.navi_attack = NaviAttack2()
        self.navi = self.navi_basic

        # subscriber
        self.imgInfo_sub = rospy.Subscriber('/img_info', ImgInfo, self.imgInfoCallBack)
        self.imgInfo = ImgInfo()
        self.warState_sub = rospy.Subscriber('/war_state', WarState, self.warStateCallBack)
        self.warState = WarState()
        self.scanInfo_sub = rospy.Subscriber('/scan_enemy_pose', ScanInfo, self.scanInfoCallBack)
        self.scanInfo = ScanInfo()

        rospy.Timer(rospy.Duration(0.1), self.selectModeCallBack)

        # obstacles subscriber
        # self.obstacles_sub = rospy.Subscriber('/raw_obstacles', Obstacles, self.imgInfoCallBack)

    def imgInfoCallBack(self, data):
        self.imgInfo = data
    
    def warStateCallBack(self, data):
        self.warState = data
    
    def scanInfoCallBack(self, data):
        self.scanInfo = data

    def selectModeCallBack(self, state):
        print()
        info_dict = {
            "img_info": self.imgInfo,
            "war_state": self.warState,
            "scan_info": self.scanInfo
        }

        if None not in info_dict.values():
            self.mode = self.modeDecider.getActMode(self.mode, **info_dict)
        print(self.mode, self.mode_prev)
        if self.mode != self.mode_prev:
            if self.mode==ActMode.basic:
                self.navi = self.navi_basic
            elif self.mode==ActMode.attack:
                # self.navi = NaviAttack()
                print("select attack mode")
                self.navi = self.navi_attack
        
        self.mode_prev = self.mode

    def strategy(self):
        r = rospy.Rate(10)

        while not rospy.is_shutdown():
            self.navi.main()
            r.sleep()


if __name__ == '__main__':
    rospy.init_node('pupe_run')
    bot = PupeBot('Puperun')
    bot.strategy()
