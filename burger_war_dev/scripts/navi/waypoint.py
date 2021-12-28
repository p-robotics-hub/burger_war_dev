#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import math

# Respect seigot

class Waypoint:

    count_waypoint = 0

    def __init__(self, path):

        self.points = []
        # self.count_waypoint = 0

        with open(path) as f:
            lines = csv.reader(f)
            for l in lines:
                point = [float(i) for i in l]
                # print(point)
                self.points.append(point[0:3])

    def get_next_waypoint(self):
        Waypoint.count_waypoint = Waypoint.count_waypoint + 1

        # 出来れば2週目からは，相手に奪われているところを狙いたい．
        if Waypoint.count_waypoint == len(self.points):
            Waypoint.count_waypoint = 0
            print('Next Lap')
         
        return self.points[Waypoint.count_waypoint][0:3]
    
    def get_current_waypoint(self):
        return self.points[Waypoint.count_waypoint][0:3]
    
    # 敵が近くにいると判断できたときだけ，以下の行動を行う
    # 事前設定のルートへの復帰どうする？？
    # 適当に座標が一番近いところへ行く？？
    def get_enemy_waypoints(self):
        pass
