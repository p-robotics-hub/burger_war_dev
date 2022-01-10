#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import tf
import math

from geometry_msgs.msg import PoseWithCovarianceStamped
from sensor_msgs.msg import LaserScan
from burger_war_dev.msg import ScanInfo
PI = math.pi


# respect is_point_enemy freom team rabbit
# https://github.com/TeamRabbit/burger_war
class EnemyDetector:    
    def __init__(self):
        self.max_distance = 1.5
        self.thresh_corner = 0.25
        self.thresh_center = 0.35

        self.pose_x = 0
        self.pose_y = 0
        self.th = 0

        self.scan = []

        #subscriber
        self.lidar_sub = rospy.Subscriber('scan', LaserScan, self.lidarCallBack)
        self.pose_sub = rospy.Subscriber('amcl_pose', PoseWithCovarianceStamped, self.poseCallBack)
        self.is_initialized_pose = False

        #publisher
        self.enemy_pos_pub = rospy.Publisher('scan_enemy_pose', ScanInfo, queue_size=1)
        self.scanInfo = ScanInfo()

    def lidarCallBack(self, data):
        self.scan = data.ranges

    def poseCallBack(self, data):
        self.pose_x = data.pose.pose.position.x
        self.pose_y = data.pose.pose.position.y
        quaternion = data.pose.pose.orientation
        rpy = tf.transformations.euler_from_quaternion((quaternion.x, quaternion.y, quaternion.z, quaternion.w))

        self.th = rpy[2]
        self.is_initialized_pose = True
        self.updateScanInfo()
        # print(self.pose_x, self.pose_y, self.th)

    def updateScanInfo(self):
        if not len(self.scan) == 360:
            return False

        # drop too big and small value ex) 0.0 , 2.0 
        near_scan = [x if self.max_distance > x > 0.1 else 0.0 for x in self.scan]

        enemy_scan = [1 if self.is_point_emnemy(x,i) else 0 for i,x in enumerate(near_scan)]

        is_near_enemy = sum(enemy_scan) > 5  # if less than 5 points, maybe noise
        if is_near_enemy:
            idx_l = [i for i, x in enumerate(enemy_scan) if x == 1]
            idx = idx_l[len(idx_l)/2]
            enemy_dist = near_scan[idx]
            enemy_direction = idx / 360.0 * 2*PI
            
            while not PI >= enemy_direction >= -PI:
                if enemy_direction > 0:
                    enemy_direction -= 2*PI
                elif enemy_direction < 0:
                    enemy_direction += 2*PI
                        
        else:
            enemy_direction = 0
            enemy_dist = 0

        # print("Enemy: {}, Direction: {}".format(is_near_enemy, enemy_direction))
        # print("enemy points {}".format(sum(enemy_scan)))

        self.scanInfo.is_enemy_recognized = is_near_enemy
        self.scanInfo.enemy_dist = enemy_dist
        self.scanInfo.enemy_direct = enemy_direction

    def is_point_emnemy(self, dist, ang_deg):
        if dist == 0:
            return False

        ang_rad = ang_deg /360. * 2 * PI
        point_x = self.pose_x + dist * math.cos(self.th + ang_rad)
        point_y = self.pose_y + dist * math.sin(self.th + ang_rad)

        #フィールド内かチェック
        if   point_y > (-point_x + 1.53):
            return False
        elif point_y < (-point_x - 1.53):
            return False
        elif point_y > ( point_x + 1.53):
            return False
        elif point_y < ( point_x - 1.53):
            return False

        #フィールド内の物体でないかチェック
        len_p1 = math.sqrt(pow((point_x - 0.53), 2) + pow((point_y - 0.53), 2))
        len_p2 = math.sqrt(pow((point_x - 0.53), 2) + pow((point_y + 0.53), 2))
        len_p3 = math.sqrt(pow((point_x + 0.53), 2) + pow((point_y - 0.53), 2))
        len_p4 = math.sqrt(pow((point_x + 0.53), 2) + pow((point_y + 0.53), 2))
        len_p5 = math.sqrt(pow(point_x         , 2) + pow(point_y         , 2))

        if len_p1 < self.thresh_corner or len_p2 < self.thresh_corner or len_p3 < self.thresh_corner or len_p4 < self.thresh_corner or len_p5 < self.thresh_center:
            return False
        else:
            #print(point_x, point_y, self.pose_x, self.pose_y, self.th, dist, ang_deg, ang_rad)
            #print(len_p1, len_p2, len_p3, len_p4, len_p5)
            return True
    
    def isNearWall(self,scan):
        pass

    def strategy(self):
        r = rospy.Rate(10) # change speed 5fps

        while not rospy.is_shutdown():
            scan_info = self.scanInfo
            self.enemy_pos_pub.publish(scan_info)
            r.sleep()


# End Respect

if __name__ == '__main__':
    rospy.init_node('EnemyDetector')
    bot = EnemyDetector()
    bot.strategy()