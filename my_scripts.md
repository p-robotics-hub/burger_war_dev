# コマンド関連

## シミュレータ起動
```bash
cd ~/catkin_ws/src/burger_war_kit
bash scripts/sim_with_judge.sh
```

## 試合開始
```bash
cd ~/catkin_ws/src/burger_war_kit
bash scripts/start.sh -l 3
```

## シミュレータリセット
```bash
cd ~/catkin_ws/src/burger_war_dev/burger_tk
bash commands/reset.sh
```
## .pyをrosrunできるように実行権限を付与
```bash
chmod +x [.pyのpath]
```

# python3関連

## python3.8のインストール
```bash
apt update -y
apt install software-properties-common -y
add-apt-repository ppa:deadsnakes/ppa -y
apt install python3.8 -y

apt install python3-pip -y
pip3 install pipenv
echo "export PIPENV_VENV_IN_PROJECT=true" >> ~/.bashrc
echo "export PIPENV_VERBOSITY=-1" >> ~/.bashrc
source ~/.bashrc
# pipenv --python 3.8
# pipenv install opencv-python
# python3.8 -m pip install -U pip
# python3.8 -m pip install rospkg opencv-python autopep8 pylint
pipenv install -d
```

## python3でcv_bridgeを使えるようにする
- https://www.souya.biz/blog2/pinevillage/2021/01/31/post-0/
- https://medium.com/@beta_b0t/how-to-setup-ros-with-python-3-44a69ca36674
```bash
apt install python3-pip python3-yaml -y
pip3 install rospkg catkin_pkg
apt install python-catkin-tools python3-dev python3-numpy -y
mkdir -p ~/catkin_cv_bridge/src
cd ~/catkin_cv_bridge/src
git clone -b melodic https://github.com/ros-perception/vision_opencv.git
cd ~/catkin_cv_bridge
catkin config \
-DCMAKE_BUILD_TYPE=Release \
-DSETUPTOOLS_DEB_LAYOUT=OFF \
-DPYTHON_EXECUTABLE=/usr/bin/python3 \
-DPYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython3.6m.so \
-DPYTHON_INCLUDE_DIR=/usr/include/python3.6m
catkin config --install
catkin build cv_bridge
echo "source ~/catkin_cv_bridge/devel/setup.bash" >> ~/.bashrc
echo "PYTHONPATH=/root/catkin_cv_bridge/devel/lib/python3.6/site-packages:$PYTHONPATH" >> ~/.bashrc
```

<!-- # vscodeで勝手にpipenvの環境に入るのを無効化
vscodeの `setting.json` に
```json
"python.terminal.activateEnvironment": false
```
を追加 -->


# 参考
- catkin_tools
    - https://catkin-tools.readthedocs.io/en/latest/index.html
    - https://qiita.com/harumo11/items/ae604ba2e17ffda529c2

- msg作成
    - http://wiki.ros.org/ja/ROS/Tutorials/CreatingMsgAndSrv

# memo
dockerでroslaunchが実行できない  
.bashrcの  
source /opt/ros/melodic/setup.bash  
が実行されていない？