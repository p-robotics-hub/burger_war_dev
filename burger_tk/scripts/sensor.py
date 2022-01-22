#!/usr/bin/env python3.8

import cv2
import numpy as np
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image, LaserScan
from std_msgs.msg import String


class ScanTest:

    def __init__(self):
        # self.scan = LaserScan()
        self.sub_scan = rospy.Subscriber("scan", LaserScan, self.scan_callback)
        self.pub_test = rospy.Publisher("test", String, queue_size=10)
        # self.vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        # self.image_pub = rospy.Publisher("cv_image", Image, queue_size=1)

    def scan_callback(self, scan: LaserScan):
        self.scan = scan
        rospy.loginfo(np.array(self.scan.ranges).shape)
        # rospy.loginfo("test")
        # self.pub_test.publish("test")

    # def strategy(self):
    #     r = rospy.Rate(30)
    #     rospy.on_shutdown(self.cleanup)

    #     while not rospy.is_shutdown():
    #         if not self.image is None:
    #             msg = self.bridge.cv2_to_imgmsg(self.image)
    #             self.image_pub.publish(msg)
    #         r.sleep()


def main():
    rospy.init_node("scan_test")
    scan_test = ScanTest()
    # rospy.spin()
    rate = rospy.Rate(0.1)
    while not rospy.is_shutdown():
        hello_str = "test"
        rospy.loginfo(hello_str)
        scan_test.pub_test.publish(hello_str)
        rate.sleep()

    # rospy.spin()


if __name__ == '__main__':
    main()
