#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This is ALL SENSOR use node.
Mainly echo sensor value in tarminal.
Please Use for your script base.

by Takuya Yamaguchi @dashimaki360
'''

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from sensor_msgs.msg import Imu
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import JointState
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
import cv2

#numpyを用いてLiDARの検出結果の演算を行う
import numpy as np

#random関数を呼ぶ
import random

#テスト用のカウント
LOOP_COUNT = 10 


class AllSensorBot(object):
    def __init__(self, 
                 use_lidar=True, use_camera=False, use_imu=False,
                 use_odom=False, use_joint_states=False):

        # velocity publisher
        self.vel_pub = rospy.Publisher('cmd_vel', Twist,queue_size=1)

        # lidar scan subscriber
        if use_lidar:
            self.scan = LaserScan()
            self.scaned = LaserScan()
            self.lidar_sub = rospy.Subscriber('scan', LaserScan, self.lidarCallback)

        # camera subscribver
        # please uncoment out if you use camera
        if use_camera:
            # for convert image topic to opencv obj
            self.img = None
            self.bridge = CvBridge()
            self.image_sub = rospy.Subscriber('image_raw', Image, self.imageCallback)

        # imu subscriber
        if use_imu:
            self.imu_sub = rospy.Subscriber('imu', Imu, self.imuCallback)

        # odom subscriber
        if use_odom:
            self.odom_sub = rospy.Subscriber('odom', Odometry, self.odomCallback)

        # joint_states subscriber
        if use_joint_states:
            self.odom_sub = rospy.Subscriber('joint_states', JointState, self.jointstateCallback)

    def strategy(self):
        r = rospy.Rate(1) # change speed 1fps

        target_speed = 0
        target_turn = 0
        control_speed = 0
        control_turn = 0

        while not rospy.is_shutdown():
          #  twist = self.calcTwist()
          #  print(twist)
          #  self.vel_pub.publish(twist)

            r.sleep()

    # lidar scan topic call back sample
    # update lidar scan state
    def lidarCallback(self, data):
        
        #エラー回避処理
        if len(self.scan.ranges) == 0:
            self.scan.ranges = data.ranges
            
        self.scaned.ranges = self.scan.ranges
        self.scan.ranges = data.ranges 

        npScanedRanges = np.array(self.scaned.ranges)
        print(npScanedRanges.shape)
        npScanRanges = np.array(self.scan.ranges)
        print(npScanRanges.shape)

        npCalData = abs(npScanRanges - npScanedRanges)
     
        for i in range(len(npCalData)):
            if npCalData[i] < 0.15:
                npCalData[i]=0
            else:
                npCalData[i]=1

        print('=================================')
        print('LiDAR is Working')
        print('=================================')
     
        print(npCalData)
        #print(npCalData.ndim)
        #print(npCalData.shape)

        print('=================================')
       
        #rospy.loginfo(self.scan)

    # camera image call back sample
    # comvert image topic to opencv object and show

    def calcTwist(self):
 
        value = random.randint(1,1000)
        if value < 250:
            x = 0.2
            #th = 0
        elif value < 500:
            x = -0.2
            th = 0
        elif value < 750:
            x = 0
            th = 1
        elif value < 1000:
            x = 0
            th = -1
        else:
            x = 0
            th = 0
        twist = Twist()
        twist.linear.x = x; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = th
        return twist

    def imageCallback(self, data):
        try:
            self.img = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)

        cv2.imshow("Image window", self.img)
        cv2.waitKey(1)

    # imu call back sample
    # update imu state
    def imuCallback(self, data):
        self.imu = data
        rospy.loginfo(self.imu)

    # odom call back sample
    # update odometry state
    def odomCallback(self, data):
        self.pose_x = data.pose.pose.position.x
        self.pose_y = data.pose.pose.position.y
        rospy.loginfo("odom pose_x: {}".format(self.pose_x))
        rospy.loginfo("odom pose_y: {}".format(self.pose_y))

    # jointstate call back sample
    # update joint state
    def jointstateCallback(self, data):
        self.wheel_rot_r = data.position[0]
        self.wheel_rot_l = data.position[1]
        rospy.loginfo("joint_state R: {}".format(self.wheel_rot_r))
        rospy.loginfo("joint_state L: {}".format(self.wheel_rot_l))

if __name__ == '__main__':
    rospy.init_node('all_sensor_sample')
    bot = AllSensorBot(use_lidar=True, use_camera=False, use_imu=False,
                       use_odom=False, use_joint_states=False)
    bot.strategy()


