# Rosbagを使ったlog出力

経緯はgithubのissueに全部書いてる→ https://github.com/EndoNrak/burger_war_dev/issues/48

## 使い時
通常のシミュレーション実行中にburger_war_dev/launch/rosbag.launchをlaunchする  
`roslaunch burger_war_dev rosbag.launch`

dockerを使っているときは~/catkin_ws/src/burger_war_devにいる状態で  
`bash commands/kit.sh -c roslaunch burger_war_dev rosbag.launch`  
を実行すればよい  

出力されたbagファイルは~/catkin_ws/src/burger_war_dev/burger_war_dev/data/rosbagフォルダ内に出力される