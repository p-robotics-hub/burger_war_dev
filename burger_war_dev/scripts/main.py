#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseWithCovarianceStamped
from sensor_msgs.msg import LaserScan
import tf
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib_msgs
from actionlib_msgs.msg import GoalStatus

import math
from std_msgs.msg import Int32MultiArray

# Ref: https://hotblackrobotics.github.io/en/blog/2018/01/29/action-client-py/

from std_msgs.msg import String, Bool, Int32, Float64
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2


class SampleBot():

    waypoint_list = []

    # waypoint_list.append([-1.0,0.0,300])
    # waypoint_list.append([-1.0,0.0,70])

    # # waypoint_list.append([-0.8,0.15,0])
    # waypoint_list.append([-0.23,0.35,340])

    # waypoint_list.append([0.3,0.35,320])
    # waypoint_list.append([1.0,0.0,110])

    # スタート地点付近
    waypoint_list.append([-0.95,0.0,300])
    waypoint_list.append([-0.98,0.0,90])

    # パティ横の壁
    waypoint_list.append([-0.9,0.58,50])
    # waypoint_list.append([-0.72,0.72,45])
    waypoint_list.append([-0.55,0.98,45])

    # waypoint_list.append([0,0.9,0])
    waypoint_list.append([0,0.9,225])
    waypoint_list.append([0,0.9,30])

    # カレー横の壁
    waypoint_list.append([0.5,0.95,315])
    # waypoint_list.append([0.72,0.72,315])
    waypoint_list.append([0.9,0.55,315])

    # waypoint_list.append([0.9,0,270])
    waypoint_list.append([0.9,0,120])
    waypoint_list.append([0.9,0,270])

    # チーズ横の壁
    waypoint_list.append([0.8,-0.55,225])
    # waypoint_list.append([0.72,-0.72,225])
    waypoint_list.append([0.5,-0.85,225])

    # waypoint_list.append([0,-0.9,180])
    waypoint_list.append([0,-0.9,45])
    waypoint_list.append([0,-0.9,180])

    # トマト横の壁
    waypoint_list.append([-0.7,-0.85,140])
    # waypoint_list.append([-0.72,-0.72,135])
    waypoint_list.append([-0.93,-0.58,135])

    # waypoint_list.append([-1.2,0,90])
    waypoint_list.append([-1.0,0,300])

    waypoint_list.extend(waypoint_list)

    def __init__(self):
        
        # velocity publisher
        self.vel_pub = rospy.Publisher('cmd_vel', Twist,queue_size=1)
        self.client = actionlib.SimpleActionClient('move_base',MoveBaseAction)

        # debug用
        self.diff_pub = rospy.Publisher('diff_degree', Int32, queue_size=1)


        # subscriber
        self.pose_sub = rospy.Subscriber('amcl_pose', PoseWithCovarianceStamped, self.poseCallback)
        # self.lidar_sub = rospy.Subscriber('scan', LaserScan, self.lidarCallback)
        # self.state_sub = rospy.Subscriber('war_state', PoseWithCovarianceStamped, self.poseCallback)

        # 敵の緑の的の重心座標を受け取る
        self.enemy_green_center_sub = rospy.Subscriber('enemy_green_center', Int32MultiArray, self.enemyGreenCenterCallback)

        self.cx = 0
        self.cy = 0

        # lidarで敵がいるか
        self.enemy_points_sub = rospy.Subscriber('is_enemy_points', Bool, self.isEnemyPointsCallback)
        self.enemy_direction_sub = rospy.Subscriber('enemy_direction', Int32, self.enemyDirectionCallback)
        self.enemy_distance_sub = rospy.Subscriber('enemy_distance', Float64, self.enemyDistanceCallback) # 距離追加
        self.is_enemy_points = None
        self.enemy_direction_deg = None
        self.enemy_distance = None

        # amclの推定位置が入る
        self.pose_x = 0
        self.pose_y = 0
        self.th = 0


    def isEnemyPointsCallback(self, msg):
        self.is_enemy_points = msg.data
        # rospy.loginfo("Enemy:{}".format(self.is_enemy_points))


    def enemyDirectionCallback(self, msg):
        self.enemy_direction_deg = msg.data
    
    def enemyDistanceCallback(self, msg):
        self.enemy_distance = msg.data



    def enemyGreenCenterCallback(self, msg):
        self.cx = msg.data[0]
        self.cy = msg.data[1]
#        print(self.cx, self.cy)
#        rospy.loginfo(self.cx, self.cy)

    def poseCallback(self, data):
        '''
        pose topic from amcl localizer
        update robot twist
        '''
        self.pose_x = data.pose.pose.position.x
        self.pose_y = data.pose.pose.position.y
        quaternion = data.pose.pose.orientation
        rpy = tf.transformations.euler_from_quaternion((quaternion.x, quaternion.y, quaternion.z, quaternion.w))
        theta = math.degrees(rpy[2])
        if theta < 0:
            self.th = 360 + theta
        else:
            self.th = theta

#        print("pose_x: {}, pose_y: {}, theta: {}".format(pose_x, pose_y, th))
        # rospy.loginfo("pose_x: {}, pose_y: {}, theta: {}".format(self.pose_x, self.pose_y, self.th))


    def setGoal(self,goal_position):#yaw[degree]
#        print(goal_position)
        x,y,yaw = goal_position[0], goal_position[1], math.radians(goal_position[2])
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

        """
        wait = self.client.wait_for_result()
        if not wait:
            rospy.logerr("Action server not available!")
            rospy.signal_shutdown("Action server not available!")
        else:
            return self.client.get_result()        
        """

    def strategy(self):
        r = rospy.Rate(10) # change speed 5fps
        waypoint_num = 0

#        while(1):
#            pass
#            r.sleep()

        while not rospy.is_shutdown():


            # カメラ画像内に敵がいた場合
            if self.cx != 0 and self.cy != 0:
#            if False:
                self.client.cancel_goal()

                # 真ん中を向くように方向転換
                diff_pix = self.cx - 320
                linear_x = 0.0
                linear_y = 0.0
                anglular_z = 0

                if abs(diff_pix) < 320 and diff_pix > 20:
                    anglular_z = -0.5 #-0.3
                elif abs(diff_pix) < 320 and diff_pix < -20:
                    anglular_z = 0.5 #0.3
                elif self.enemy_distance > 0.5: # 距離みて近づく（距離見れてないから動いてない）
                    linear_x = 2.0
                    linear_y = 2.0
                else:
                    anglular_z = 0.0

                twist = Twist()
                twist.linear.x = linear_x; twist.linear.y = linear_y; twist.linear.z = 0
                twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = anglular_z
                self.vel_pub.publish(twist)


            # Lidarが敵を捉えた場合
#            elif self.is_enemy_points == True:
            elif self.enemy_direction_deg > 0:
                self.client.cancel_goal()
#                diff_degree = self.enemy_direction_deg - self.th
                linear_x = 0.0
                linear_y = 0.0
                anglular_z = 0.0
                
#                self.diff_pub(diff_degree)

                # 前方189度のみ監視する版(後ろを振り向くと的が取られることがある)
                if abs(self.enemy_direction_deg) > 10 and self.enemy_direction_deg > 270:
                    anglular_z = -0.85 #-1.5
                elif abs(self.enemy_direction_deg) > 10 and self.enemy_direction_deg < 91:
                    anglular_z = 0.85 #1.5
                elif self.enemy_distance > 0.5: # 距離みて近づく（距離見れてないから動いてない）
                    linear_x = 2.0
                    linear_y = 2.0
                else:
                    anglular_z = 0.0

                """
                # 360度監視する板
                if abs(self.enemy_direction_deg) > 10 and self.enemy_direction_deg > 180:
                    anglular_z = -1.5
                elif abs(self.enemy_direction_deg) > 10 and self.enemy_direction_deg < 181:
                    anglular_z = 1.5
                else:
                    anglular_z = 0.0
                """

                # rospy.loginfo("enemy_direction_deg: {}".format(self.enemy_direction_deg))
                # rospy.loginfo("enemy_distance: {}".format(self.enemy_distance))

                twist = Twist()
                twist.linear.x = linear_x; twist.linear.y = linear_y; twist.linear.z = 0
                twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = anglular_z
                self.vel_pub.publish(twist)


#                if self.client.get_state() != GoalStatus.ACTIVE:
#                    self.setGoal([self.pose_x, self.pose_y, self.enemy_direction_deg])


            # 敵がいない場合
#            """
            else:
                # rospy.loginfo(self.client.get_state())
                # waypointに到達したら次のwaypointにする
                if self.client.get_state() == GoalStatus.SUCCEEDED:
                    waypoint_num += 1

                # 動いてなかったらwaypointをセット
                if self.client.get_state() != GoalStatus.ACTIVE:
                    self.setGoal(self.waypoint_list[waypoint_num])
#            """

            r.sleep()





if __name__ == '__main__':
    rospy.init_node('main')
    bot = SampleBot()
    bot.strategy()