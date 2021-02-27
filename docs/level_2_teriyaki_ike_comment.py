#!/usr/bin/env python
# -*- coding: utf-8 -*-

# level_2_teriyaki.py
# write by yamaguchi takuya @dashimaki360
## GO around field by AMCL localizer


import rospy
import random

from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseWithCovarianceStamped
from sensor_msgs.msg import LaserScan

import tf

PI = 3.1416
# 8x8  [rad]
# Filedを8×8のブロックに分割して，1ブロックごとに目標の姿勢（z軸回りの角度）を予め設定している．
    # xy平面上の移動なので，前進速度と姿勢を決定すれば任意の位置に移動可能．
# 下の角度はグローバル座標系（≠ロボット座標系）での角度を表す．
    # 原点固定，相手のロボット方向に向かってy軸正，y軸から時計回りに90度回転したものがx軸正．

# ややこしいのが，絶妙にマップの向きとマトリックスの向きが対応していないところ...
# ちょうど下のマトリックスを時計回りに90度回転したものが，実際のgazebo初期画面の向きに対応している．
# メソッド "poseToindex" を見れば分かるが
# ex. TARGET_TH[3][0]がテリヤキの初期位置，TARGET_TH[0][3]が向かって右の角（x=max, y=0）， TARGET_TH[3][7]が手前の角（x=0, y=min），TARGET_TH[7][3]が向かって左の角（x=min, y=0）
TARGET_TH = (
    (-PI/4, -PI/4, -PI/2, -PI/2, -PI*3/4, -PI*3/4, -PI*3/4, -PI*3/4),
    (-PI/4, -PI/4, -PI/4, -PI/4, -PI*3/4, -PI*3/4, -PI*3/4, -PI*3/4),
    (-PI/4, -PI/4, -PI/6,     0,   -PI/2, -PI*3/4, -PI*3/4,      PI),
    (-PI/4, -PI/6,     0,     0,   -PI/2,   -PI/2, -PI*3/4,      PI),
    (    0,     0,  PI/2,  PI/2,      PI,      PI,  PI*3/4,  PI*3/4),
    (    0,  PI/4,  PI/3,  PI/2,  PI*5/6,  PI*3/4,  PI*3/4,  PI*3/4),
    ( PI/4,  PI/4,  PI/4,  PI/3,  PI*5/6,    PI/2,  PI*3/4,  PI*3/4),
    ( PI/4,  PI/4,  PI/4,  PI/3,    PI/2,    PI/2,  PI*3/4,  PI*3/4),
)

WIDTH = 1.2 * (2 **0.5) # [m]

class TeriyakiBurger():
    def __init__(self, bot_name):
        # bot name 
        self.name = bot_name
        # robot state 'inner' or 'outer'
        self.state = 'inner' 
        # robot wheel rot 
        self.wheel_rot_r = 0
        self.wheel_rot_l = 0
        self.pose_x = 0
        self.pose_y = 0

        self.k = 0.5

        self.near_wall_range = 0.2  # [m]

        # speed [m/s]
        self.speed = 0.07

        # lidar scan
        self.scan = []

        # publisher
        self.vel_pub = rospy.Publisher('cmd_vel', Twist,queue_size=1)

        # subscriber

        # 一旦無視でいいと思う．
        # やっていることとしては，Lidarやエンコーダから得られた情報をもとに，AMCLというアルゴリズムを使用して，今ロボットが地図上（今回で言うと，フィールド上）のどの位置にいるかを推定している．
            # 壁の形状やオドメトリを利用して，自己位置を確率付きで推定している．
        self.pose_sub = rospy.Subscriber('amcl_pose', PoseWithCovarianceStamped, self.poseCallback)

        # "sensor_msgs"というパッケージから，"LaserScan" というMessageをインポート
        # URL:http://docs.ros.org/en/melodic/api/sensor_msgs/html/msg/LaserScan.html

        # 今回使用しているのは，"ranges"というメンバ変数だけ．
            # 障害物までの距離を測定．角度分解能に応じて，配列生成．
            # ex. self.ranges[i]:i番目の角度における障害物までの距離データ
        self.lidar_sub = rospy.Subscriber('scan', LaserScan, self.lidarCallback)

        self.twist = Twist()
        self.twist.linear.x = self.speed; self.twist.linear.y = 0.; self.twist.linear.z = 0.
        self.twist.angular.x = 0.; self.twist.angular.y = 0.; self.twist.angular.z = 0.
 
    def poseCallback(self, data):
        '''
        pose topic from amcl localizer
        update robot twist
        '''

        # AMCLから現在の自己位置（位置：pose_x, pose_y　姿勢：th）を推定．
        pose_x = data.pose.pose.position.x
        pose_y = data.pose.pose.position.y
        quaternion = data.pose.pose.orientation
        rpy = tf.transformations.euler_from_quaternion((quaternion.x, quaternion.y, quaternion.z, quaternion.w))
        th = rpy[2]

        # 推定した位置から，ロボットの目標姿勢（TARGET_TH）を算出．
        th_xy = self.calcTargetTheta(pose_x,pose_y)
        
        # TARGET_THと現在の実際の姿勢の差（つまり目標からのズレ）を計算． -> そのズレを補正するように次の移動ベクトルを決定する．
        th_diff = th_xy - th

        # thetaが-PIからPIの範囲に収まるように．
        while not PI >= th_diff >= -PI:
            if th_diff > 0:
                th_diff -= 2*PI
            elif th_diff < 0:
                th_diff += 2*PI

        # 上で求めたズレ"th_diff"を元に，次の移動ベクトルを決定する．
        # ただ，ここでややこしいのが，そのズレ分だけでなく，周辺の障害物情報も考慮して，最終的な移動方向を決定しているところ．
        # 下の"clacDeltaTheta"を確認してね
        delta_th = self.calcDeltaTheta(th_diff)

        # "th_diff（目標姿勢とのズレ）"と"delta_th（障害物回避）"にゲイン"self.k"をかけて，最終的な移動ベクトルを決定
            # いわゆるフィードバック制御（比例制御，P制御）．ただただ，差分を補うというもの．オーバシュートなど，収束せず振動しがち．
        new_twist_ang_z = max(-0.3, min((th_diff + delta_th) * self.k , 0.3))
        
        self.twist.angular.z = new_twist_ang_z
        print("th: {}, th_xy: {}, delta_th: {}, new_twist_ang_z: {}".format(th, th_xy, delta_th, new_twist_ang_z))


    # "poseToindex"と組み合わせて，現在の位置における予め設定した目標姿勢を算出．
    def calcTargetTheta(self, pose_x, pose_y):
        x = self.poseToindex(pose_x)
        y = self.poseToindex(pose_y)
        th = TARGET_TH[x][y]
        print("POSE pose_x: {}, pose_y: {}. INDEX x:{}, y:{}".format(pose_x, pose_y, x, y))
        return th


    # 目標姿勢と現在の姿勢の差分（＝ズレ）だけでなく，周辺障害物情報を考慮して，移動ベクトルを決定するために必要．
    # "radToidx"はradを度に変換しているだけ
    def calcDeltaTheta(self, th_diff):
        if not self.scan:
            return 0.
        # th_diff == 0 として考えると分かりやすいはず．
        # それぞれロボットの進行方向（ロボット正面）に対して，-PI/8, -PI/4, PI/8, PI/4の角度にあるレーザ情報（障害物までの距離）を使って，移動ベクトル決定．
            # イメージで言うと，例えズレを補正するように移動ベクトルを決定できたとしても，その先に障害物があれば次の移動がしにくくなる．（目標姿勢を予め厳密に決めておけば，そこまで頻繁には怒らないはずではある）
        R0_idx = self.radToidx(th_diff - PI/8)
        R1_idx = self.radToidx(th_diff - PI/4)
        L0_idx = self.radToidx(th_diff + PI/8)
        L1_idx = self.radToidx(th_diff + PI/4)

        # Lidarからありえない値が出てきた場合には無視するというイメージ
            # 基本Lidarは100 [mm]以下などはあまり正確に測定できない
        R0_range = 99. if self.scan[R0_idx] < 0.1 else self.scan[R0_idx]
        R1_range = 99. if self.scan[R1_idx] < 0.1 else self.scan[R1_idx]
        L0_range = 99. if self.scan[L0_idx] < 0.1 else self.scan[L0_idx]
        L1_range = 99. if self.scan[L1_idx] < 0.1 else self.scan[L1_idx]

        # 周辺障害物を避けるための移動方向を決定．（下の条件を図で書いてみると分かりやすいはず）
        # ただ，移動方向は決め打ちの4通りのみで，この辺は結構雑？？
            # そのため，何周もするとかなり誤差が大きくなるのか．
        print("Ranges R0: {}, R1: {}, L0: {}, L1: {}".format(R0_range, R1_range, L0_range, L1_range))
        if R0_range < 0.3 and L0_range > 0.3:
            return PI/4
        elif R0_range > 0.3 and L0_range < 0.3:
            return -PI/4
        elif R1_range < 0.2 and L1_range > 0.2:
            return PI/8
        elif R1_range > 0.2 and L1_range < 0.2:
            return -PI/8
        else:
            return 0.
    
    def radToidx(self, rad):
        deg = int(rad / (2*PI) * 360)
        while not 360 > deg >= 0:
            if deg > 0:
                deg -= 360
            elif deg < 0:
                deg += 360
        return deg

    def poseToindex(self, pose):
        i = 7 - int((pose + WIDTH) / (2 * WIDTH) * 8)
        i = max(0, min(7, i))
        return i

    # Subscriber "self.lidar_sub" に対応するCallback関数（センサー情報を一定周期で受け取るたびに実行される関数）．
    # "data.ranges"がLidarを使って得られた，角度ごとの距離情報を格納した配列．
    # 障害物までの距離が近い場合は，後退する．
    def lidarCallback(self, data):
        '''
        lidar scan use for bumper
        controll speed.x
        '''
        scan = data.ranges
        self.scan = scan
        is_near_wall = self.isNearWall(scan)
        if is_near_wall:
            self.twist.linear.x = -self.speed / 2
        else:
            self.twist.linear.x = self.speed

    # 障害物を検出する範囲は360度ではなく，ある一定の領域のみ．
        # もちろん，進行方向に対する障害物の有無を知りたいから．
        # 回避動作に，バック走行やその場旋回を加味するなら，本当はもっと広い範囲の情報を使ったほうが良いのでは．
    def isNearWall(self, scan):
        if not len(scan) == 360:
            return False
        forword_scan = scan[:15] + scan[-15:]
        # drop too small value ex) 0.0
        forword_scan = [x for x in forword_scan if x > 0.1]
        if min(forword_scan) < 0.2:
            return True
        return False

    def strategy(self):
        '''
        calc Twist and publish cmd_vel topic
        Go and Back loop forever
        '''
        r = rospy.Rate(10) # change speed 10fps

        while not rospy.is_shutdown():
            # publish twist topic
            self.vel_pub.publish(self.twist)

            r.sleep()


if __name__ == '__main__':
    rospy.init_node('enemy')
    bot = TeriyakiBurger('teriyaki_burger')
    bot.strategy()

