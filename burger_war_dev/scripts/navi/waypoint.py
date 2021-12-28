#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy

import csv
import math

from burger_war_dev.msg import WarState

# Respect seigot

class Waypoint:

    count_waypoint = 0

    def __init__(self, path_waypoints, path_waypoints_depending_on_score):

        self.points = []
        self.points_depending_on_score = []
        # self.count_waypoint = 0
        
        self.next_lap_flag = False
        self.watch_score_flag = False
        self.marker_no_offset = 6

        with open(path_waypoints) as f:
            lines = csv.reader(f)
            for l in lines:
                point = [float(i) for i in l]
                # print(point)
                self.points.append(point[0:3])
                
        with open(path_waypoints_depending_on_score) as f_score:
            lines_score = csv.reader(f_score)
            for l_score in lines_score:
                point_depending_on_score = [float(i_score) for i_score in l_score]
                # print(point)
                self.points_depending_on_score.append(point_depending_on_score[0:3])

        self.warState_sub = rospy.Subscriber('war_state', WarState, self.warStateCallBack)
        self.warState = WarState()
    
    def warStateCallBack(self, data):
        self.warState = data
        print('get data!')
        print(self.warState.enem_get_wall_marker_no)

    def get_next_waypoint(self):
        Waypoint.count_waypoint = Waypoint.count_waypoint + 1

        # 2週目からは，相手に奪われているところを狙う
        if Waypoint.count_waypoint == len(self.points):
            print('Next Lap')
            Waypoint.count_waypoint = 0
            
            # 2週目開始のフラグを立てる
            self.next_lap_flag = True
        
        # フィールドのマーカを一つも奪われていないときはまた周回コースに戻る
        if self.warState.enem_get_wall_marker_no == 0:
            self.watch_score_flag = False
        else:
            self.watch_score_flag = True
        
        if self.next_lap_flag and self.watch_score_flag:
            # print('Waypoint.watch_score_flag')
            return self.points_depending_on_score[self.warState.enem_get_wall_marker_no - self.marker_no_offset][0:3]
        else:
            return self.points[Waypoint.count_waypoint][0:3]
    
    def get_current_waypoint(self):
        if self.next_lap_flag and self.watch_score_flag:
            # print('Waypoint.watch_score_flag')
            return self.points_depending_on_score[self.warState.enem_get_wall_marker_no - self.marker_no_offset][0:3]
        else:
            return self.points[Waypoint.count_waypoint][0:3]
    
    # 敵が近くにいると判断できたときだけ，以下の行動を行う
    # 事前設定のルートへの復帰どうする？？
    # 適当に座標が一番近いところへ行く？？
    def get_enemy_waypoints(self):
        pass
