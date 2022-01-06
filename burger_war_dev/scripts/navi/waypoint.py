#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy

import csv
import math

from burger_war_dev.msg import WarState

# Respect seigot

class Waypoint:

    next_lap_flag = False
    count_waypoint = 0
    waypoint_reverse_flag_for_blue = True

    def __init__(self, path_waypoints, path_waypoints_depending_on_score):

        self.points = []
        self.points_depending_on_score = []
        
        self.marker_no_offset = 6
        
        self.warState_sub = rospy.Subscriber('war_state', WarState, self.warStateCallBack)
        self.warState = WarState()

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
    
    def warStateCallBack(self, data):
        self.warState = data
        print('get data!')
        print(self.warState.enem_get_wall_marker_no)
        
        if Waypoint.waypoint_reverse_flag_for_blue:
            # blue side の場合は，180度ひっくり返す
            if self.warState.my_side == 'b':
                for i, point in enumerate(self.points_depending_on_score):
                    self.points_depending_on_score[i][0] *= -1
                    self.points_depending_on_score[i][1] *= -1
                    self.points_depending_on_score[i][2] -= 3.141592654
                
                print('my side:', self.warState.my_side)
                print(self.points_depending_on_score)
            Waypoint.waypoint_reverse_flag_for_blue = False

    def get_next_waypoint(self):
        print(self.warState.enem_get_wall_marker_flag)
        Waypoint.count_waypoint = Waypoint.count_waypoint + 1

        # 2週目からは，相手に奪われているところを狙う
        if Waypoint.count_waypoint == len(self.points):
            print('Next Lap')
            Waypoint.count_waypoint = 0
            
            # 2週目開始のフラグを立てる
            Waypoint.next_lap_flag = True
        
        # フィールドのマーカを（新たに）一つも奪われていないときはまた周回コースに戻る
        if Waypoint.next_lap_flag and self.warState.enem_get_wall_marker_flag:
            # print('Waypoint.watch_score_flag')
            Waypoint.count_waypoint = Waypoint.count_waypoint - 1
            return self.points_depending_on_score[self.warState.enem_get_wall_marker_no - self.marker_no_offset][0:3]
        else:
            return self.points[Waypoint.count_waypoint][0:3]
    
    def get_current_waypoint(self):
        if Waypoint.next_lap_flag and self.warState.enem_get_wall_marker_flag:
            # print('Waypoint.watch_score_flag')
            return self.points_depending_on_score[self.warState.enem_get_wall_marker_no - self.marker_no_offset][0:3]
        else:
            return self.points[Waypoint.count_waypoint][0:3]
    
    # 敵が近くにいると判断できたときだけ，以下の行動を行う
    # 事前設定のルートへの復帰どうする？？
    # 適当に座標が一番近いところへ行く？？
    def get_enemy_waypoints(self):
        pass