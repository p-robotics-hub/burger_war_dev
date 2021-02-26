#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import random
import csv
import math
import os 

from geometry_msgs.msg import Twist

import tf


import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib_msgs

from std_srvs.srv import Empty, EmptyRequest, EmptyResponse

from waypoint import Waypoint

PI = 3.1416

# Ref: https://hotblackrobotics.github.io/en/blog/2018/01/29/action-client-py/

#from std_msgs.msg import String
#from sensor_msgs.msg import Image
#from cv_bridge import CvBridge, CvBridgeError
#import cv2


class NaviBot():
    def __init__(self):

        self.path = os.environ['HOME'] + '/catkin_ws/src/burger_war_dev/burger_war_dev/scripts/waypoints.csv'
        self.waypoints = Waypoint(self.path)
        
        # velocity publisher
        self.vel_pub = rospy.Publisher('cmd_vel', Twist,queue_size=1)
        self.client = actionlib.SimpleActionClient('move_base',MoveBaseAction)

        rospy.wait_for_service("/move_base/clear_costmaps")
        self.clear_costmap = rospy.ServiceProxy("/move_base/clear_costmaps", Empty)


    def setGoal(self,points):
        self.client.wait_for_server()

        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = points[0]
        goal.target_pose.pose.position.y = points[1]

        # Euler to Quartanion
        q=tf.transformations.quaternion_from_euler(0,0,points[2])        
        goal.target_pose.pose.orientation.x = q[0]
        goal.target_pose.pose.orientation.y = q[1]
        goal.target_pose.pose.orientation.z = q[2]
        goal.target_pose.pose.orientation.w = q[3]

        self.client.send_goal(goal)
        
        wait = self.client.wait_for_result()
        if not wait:
            rospy.logerr("Action server not available!")
            rospy.signal_shutdown("Action server not available!")
        else:
            return self.client.get_result()
            


    def strategy(self):
        r = rospy.Rate(5) # change speed 5fps

        while not rospy.is_shutdown():
            self.waypoint = self.waypoints.get_next_waypoint()
            self.setGoal(self.waypoint)

    def navStateCheck(self):
        self.state = self.client.get_state()
        # print(100)


if __name__ == '__main__':
    rospy.init_node('navirun')
    bot = NaviBot()
    bot.strategy()
