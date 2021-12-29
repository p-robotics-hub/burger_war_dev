#!/bin/bash

cd ~/catkin_ws/src/burger_war_kit
# ロボットの位置の初期化
rosservice call /gazebo/reset_simulation "{}"
# 審判サーバーのリセット
bash judge/test_scripts/init_single_play.sh judge/marker_set/sim.csv localhost:5000 you enemy