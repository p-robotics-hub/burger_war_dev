#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy

import csv
import math

from burger_war_dev.msg import WarState

# Respect seigot

class Waypoint:

    count_waypoint = 0
    watch_score_flag = False

    def __init__(self, path_waypoints, path_waypoints_depending_on_score):

        self.points = []
        self.points_depending_on_score = []
        # self.count_waypoint = 0

        with open(path_waypoints) as f:
            lines = csv.reader(f)
            for l in lines:
                point = [float(i) for i in l]
                # print(point)
                self.points.append(point[0:3])
                
        with open(path_waypoints_depending_on_score) as f:
            lines = csv.reader(f)
            for l in lines:
                point_depending_on_score = [float(i) for i in l]
                # print(point)
                self.points_depending_on_score.append(point[0:3])

        self.warState_sub = rospy.Subscriber('war_state', WarState, self.warStateCallBack)
        self.warState = WarState()
    
    def warStateCallBack(self, data):
        self.warState = data
        print(self.warState.enem_get_wall_marker_no)

    def get_next_waypoint(self):
        Waypoint.count_waypoint = Waypoint.count_waypoint + 1

        # 2週目からは，相手に奪われているところを狙う
        if Waypoint.count_waypoint == len(self.points):
            print('Next Lap')
            Waypoint.count_waypoint = 0
            
            # judge-serverより得られるスコアに基づいた行動開始のフラグを立てる
            Waypoint.watch_score_flag = True
        
        if Waypoint.watch_score_flag:
            # もしフィールドのマーカを一つも奪われていないときはまた周回コースに戻る？？
            pass
         
        return self.points[Waypoint.count_waypoint][0:3]
    
    def get_current_waypoint(self):
        return self.points[Waypoint.count_waypoint][0:3]
    
    # 敵が近くにいると判断できたときだけ，以下の行動を行う
    # 事前設定のルートへの復帰どうする？？
    # 適当に座標が一番近いところへ行く？？
    def get_enemy_waypoints(self):
        pass
