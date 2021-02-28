#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import random
import csv
import math
import os 
import tf

from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseWithCovarianceStamped
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib_msgs
from burger_war_dev.msg import ImgInfo

from std_srvs.srv import Empty, EmptyRequest, EmptyResponse

from waypoint import Waypoint

PI = 3.1416

# Ref: https://hotblackrobotics.github.io/en/blog/2018/01/29/action-client-py/

#from std_msgs.msg import String
#from sensor_msgs.msg import Image
#from cv_bridge import CvBridge, CvBridgeError
#import cv2


class NaviAttack():
    def __init__(self):

        self.path = os.environ['HOME'] + '/catkin_ws/src/burger_war_dev/burger_war_dev/scripts/waypoints.csv'
        self.waypoints = Waypoint(self.path)
        
        # velocity publisher
        self.vel_pub = rospy.Publisher('cmd_vel', Twist,queue_size=1)
        self.client = actionlib.SimpleActionClient('move_base',MoveBaseAction)

        self.enemy_position_sub = rospy.Subscriber('img_info', ImgInfo, self.tfCallback)
        self.pose_sub = rospy.Subscriber('amcl_pose', PoseWithCovarianceStamped, self.poseCallback)

        rospy.wait_for_service("/move_base/clear_costmaps")
        self.clear_costmap = rospy.ServiceProxy("/move_base/clear_costmaps", Empty)

        self.status = self.client.get_state()

        self.tf_flag = False
        self.rotation_gain = 5.0


    def poseCallback(self, data):
        '''
        pose topic from amcl localizer
        update robot twist
        '''
        self.pose_x = data.pose.pose.position.x
        self.pose_y = data.pose.pose.position.y
        quaternion = data.pose.pose.orientation
        rpy = tf.transformations.euler_from_quaternion((quaternion.x, quaternion.y, quaternion.z, quaternion.w))
        self.th = rpy[2]

        print(self.pose_x, self.pose_y, self.th)


    def setGoal(self, x, y, yaw):
        self.client.wait_for_server()

        self.clear_costmap.call()

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

    # 座標変換
    # Global座標系における敵中心の座標を算出
    # カメラ座標系 -> Global座標系
    def tfCallback(self, data):

        self.enemy_info = data
        print(self.enemy_info)

        self.enemy_info.enemy_direct = -self.enemy_info.enemy_direct*PI/180

        # ModeDecisionで判定されているので恐らくif文は不要
        # if self.enemy_info.is_enemy_recognized: 
        self.enemy_pose_x = self.pose_x + self.enemy_info.enemy_dist * math.cos(self.enemy_info.enemy_direct) * math.cos(self.th) - self.enemy_info.enemy_dist * math.sin(self.enemy_info.enemy_direct) * math.sin(self.th)
        self.enemy_pose_y = self.pose_y + self.enemy_info.enemy_dist * math.cos(self.enemy_info.enemy_direct) * math.sin(self.th) + self.enemy_info.enemy_dist * math.sin(self.enemy_info.enemy_direct) * math.cos(self.th)
        
        # else:
        #     self.enemy_pose_x = None
        #     self.enemy_pose_y = None

        print(self.enemy_pose_x, self.enemy_pose_y)

        self.tf_flag = True


    # tfCallbackの結果から，敵マーカを読み取れるような位置に移動
    # 常に敵中心を向くような姿勢を目標姿勢とする
    # 敵中心からの距離は一旦，1.0とする        
    def get_next_enemypoint(self):
        self.enemypoint_th = self.th + self.enemy_info.enemy_direct * self.rotation_gain

        
    # get_next_enemypointの結果，目標位置が障害物内に設定される可能性もある
    def check_obstacle(self):
        pass

    def main(self):
        # r = rospy.Rate(1) # change speed 5fps

        # self.waypoint = self.waypoints.get_current_waypoint()
        # self.setGoal(self.waypoint)

        # self.setGoal(0.72,0.72,-0.785398163)

        # while not rospy.is_shutdown():
        if self.tf_flag:
            self.get_next_enemypoint()
            # self.setGoal(0.75,0.7,self.enemypoint_th)
            self.setGoal(0.8,0.6,self.enemypoint_th)
            self.tf_flag = False
            # r.sleep()

            # # Basic Mode
            # pre_status = self.status
            # self.status = self.client.get_state()

            # if pre_status != self.status:
            #     rospy.loginfo(self.client.get_goal_status_text())

            # if self.status == actionlib.GoalStatus.ACTIVE:
            #     print('ACTIVE')    
            
            # elif self.status == actionlib.GoalStatus.SUCCEEDED:
            #     print('SUCCEEDED')
            #     self.waypoint = self.waypoints.get_next_waypoint()
            #     self.setGoal(self.waypoint)
            
            # # 本来は今回の競技に適したRecovery Behaviorを設計すべき
            # # 現段階では，目標地点を次に設定して，強引にDeadrockを突破する
            # elif self.status == actionlib.GoalStatus.ABORTED:
            #     print('ABORTED')
            #     self.waypoint = self.waypoints.get_next_waypoint()
            #     self.setGoal(self.waypoint)

            # elif self.status == actionlib.GoalStatus.PENDING:
            #     print('PENDING')
            #     self.waypoint = self.waypoints.get_current_waypoint()
            #     self.setGoal(self.waypoint)

            # # 敵追従を終えた場合に，元の周回コースに復帰するため
            # # Navigationで敵追従するなら，要らないかも
            # elif self.status == actionlib.GoalStatus.PREEMPTING or self.status == actionlib.GoalStatus.PREEMPTED:
            #     print('PREEMPTING or PREEMPTED')    
            #     self.waypoint = self.waypoints.get_current_waypoint()
            #     self.setGoal(self.waypoint)    


# if __name__ == '__main__':
#     rospy.init_node('navirun')
#     bot = NaviAttack()
#     bot.main()
