#!/usr/bin/env python
# -*- coding: utf-8 -*-
from posixpath import split
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseWithCovarianceStamped
from sensor_msgs.msg import LaserScan
import tf
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib_msgs

import math
import json

# Ref: https://hotblackrobotics.github.io/en/blog/2018/01/29/action-client-py/

from std_msgs.msg import Bool, String, Int32, Float64, Int32MultiArray
import numpy as np

from visualization_msgs.msg import Marker

TargetKey = [   "Tomato_N", 
                "Tomato_S", 
                "Omelette_N", 
                "Omelette_S", 
                "Pudding_N", 
                "Pudding_S", 
                "OctopusWiener_N", 
                "OctopusWiener_S", 
                "FriedShrimp_N", 
                "FriedShrimp_E", 
                "FriedShrimp_W", 
                "FriedShrimp_S"
            ]


class WarStatus():

    def __init__(self):

        # publisher
        self.score_status = rospy.Publisher('score_status', Int32MultiArray, queue_size=10)

        # subscriber
        self.state_sub = rospy.Subscriber('war_state', String, self.StateCallback)

        self.json_score = ""
        self.score_array = []

    def StateCallback(self, data):
        self.score_array = []
        self.json_score = json.loads(data.data)

        for i in range(0, len(self.json_score["targets"])):
            for j , key in enumerate(TargetKey):
                if(self.json_score["targets"][i]["name"] == key):
                    if self.json_score["targets"][i]["player"] == rospy.get_param("/side"):
                        self.score_array.append(1)
                    else:
                        self.score_array.append(0)
        
        # print(self.score_array)
        rospy.loginfo("SCORE: {}".format(self.score_array))
        self.score_status.publish(Int32MultiArray(data = self.score_array))





if __name__ == '__main__':
    try:
        rospy.init_node('score_status', anonymous=False)
        status = WarStatus()

        rate = rospy.Rate(10) # 10hz

        while not rospy.is_shutdown():
            rate.sleep()

    except rospy.ROSInterruptException:
        pass



