#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import random

from geometry_msgs.msg import Twist

import tf


import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib_msgs

from std_srvs.srv import Empty, EmptyRequest, EmptyResponse

PI = 3.1416

# Ref: https://hotblackrobotics.github.io/en/blog/2018/01/29/action-client-py/

#from std_msgs.msg import String
#from sensor_msgs.msg import Image
#from cv_bridge import CvBridge, CvBridgeError
#import cv2


class NaviBot():
    def __init__(self):
        
        # velocity publisher
        self.vel_pub = rospy.Publisher('cmd_vel', Twist,queue_size=1)
        self.client = actionlib.SimpleActionClient('move_base',MoveBaseAction)

        rospy.wait_for_service("/move_base/clear_costmaps")
        self.clear_costmap = rospy.ServiceProxy("/move_base/clear_costmaps", Empty)


    def setGoal(self,x,y,yaw):
        self.client.wait_for_server()

        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y

        # Euler to Quartanion
        q=tf.transformations.quaternion_from_euler(0,0,yaw)        
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

        # self.setGoal(-1.0,0,-PI/4)
        # self.setGoal(-1.3,0.1,PI/8)

        # self.setGoal(-0.72,0.72,PI/4)

        # self.setGoal(0,1.1,-PI/2)
        # self.setGoal(0,1.0,-PI*3/4)
        # self.setGoal(0.1,1.3,-PI*3/8)

        # self.setGoal(0.72,0.72,-PI/4)

        # self.setGoal(1.1,0,PI)
        # self.setGoal(1.0,0,PI*3/4)
        # self.setGoal(1.3,-0.1,-PI*7/8)

        # self.setGoal(0.72,-0.72,-PI*3/4)

        # self.setGoal(0,-1.1,PI/2)
        # self.setGoal(0,-1.0,PI/4)
        # self.setGoal(-0.1,-1.3,PI*5/8)

        # self.setGoal(-0.72,-0.72,PI*3/4)

        # self.setGoal(-1.0,0,-PI/4)

        self.setGoal(-1.0,0,-PI/4)
        self.setGoal(-1.0,0,PI/2)

        self.setGoal(-0.72,0.72,PI/4)

        self.setGoal(0,1.1,-PI/2)
        self.setGoal(0,1.1,-PI*3/4)
        self.setGoal(0,1.1,0)

        self.setGoal(0.72,0.72,-PI/4)

        self.setGoal(1.1,0,PI)
        self.setGoal(1.1,0,PI*3/4)
        self.setGoal(1.1,0,-PI/2)

        self.setGoal(0.72,-0.72,-PI*3/4)

        self.setGoal(0,-1.1,PI/2)
        self.setGoal(0,-1.1,PI/4)
        self.setGoal(0,-1.1,PI)

        self.setGoal(-0.72,-0.72,PI*3/4)

        self.setGoal(-1.0,0,-PI/4)




if __name__ == '__main__':
    rospy.init_node('navirun')
    bot = NaviBot()
    bot.strategy()
