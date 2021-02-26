#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import math

# Respect seigot

class Waypoint:

    def __init__(self, path):

        self.points = []
        self.way_count = -1

        with open(path) as f:
            lines = csv.reader(f)
            for l in lines:
                point = [float(i) for i in l]
                # print(point)
                self.points.append(point[0:3])

    def get_next_waypoint(self):
        self.way_count = self.way_count + 1

        if self.way_count == len(self.points):
            self.way_count = 0
            print('Next Lap')
         
        return self.points[self.way_count][0:3]
