import random

import cv2
import gym
import numpy as np
import rospy
from gym import spaces
from sensor_msgs.msg import Image, LaserScan


class BurgerWarEnv(gym.Env):

    def __init__(self):
        super().__init__()

        self.sub_scan = rospy.Subscriber("scan", LaserScan, self.scan_callback)

        # 行動空間の定義
        self.action_space = spaces.Discrete(3)

        # 観測空間(状態空間)の定義
        # low = np.array([[-1]*3 for _ in range(3)])
        # high = np.array([[1]*3 for _ in range(3)])
        # self.observation_space = spaces.Box(low=low, high=high, dtype=np.int8)
        self.observation_space = spaces.Box(low=0, high=3.5, shape=(360,))

        self.reset()
