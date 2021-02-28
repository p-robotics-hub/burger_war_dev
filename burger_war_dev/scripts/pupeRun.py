#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy

from naviBasic import NaviBasic
# from naviAttack import NaviAttack
from gazeEnemy import GazeEnemyBot

from ModeDecider import ModeDecider

from burger_war_dev.msg import ImgInfo

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
        self.imgInfo_sub = rospy.Subscriber('/img_info', ImgInfo, self.imgInfoCallBack)
        self.imgInfo_data = None
    
    def imgInfoCallBack(self, data):
        print(data)
        self.imgInfo_data = data

    def select_mode(self):
        print(self.imgInfo_data)
        if self.imgInfo_data is not None:
            self.mode = self.modeDecider.getActMode(self.imgInfo_data.is_enemy_recognized, self.imgInfo_data.enemy_dist)
        print(self.mode)
        if self.mode != self.mode_prev:
            if self.mode==ActMode.basic:
                self.navi = NaviBasic()
            elif self.mode==ActMode.attack:
                # self.navi = NaviAttack()
                self.navi = GazeEnemyBot()
        
        self.mode_prev = self.mode

    def strategy(self):
        r = rospy.Rate(5)

        while not rospy.is_shutdown():
            self.select_mode()
            self.navi.main()
            r.sleep()


if __name__ == '__main__':
    rospy.init_node('pupe_run')
    bot = PupeBot('Puperun')
    bot.strategy()
