#!/usr/bin/env python3.8

import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


class CvCam3:

    def __init__(self):
        self.cv_bridge = CvBridge()
        self.sub_image = rospy.Subscriber("image_raw", Image, self.image_callback)
        # self.cvrect_pub = rospy.Publisher("cv_rect", CvRect, queue_size=1000)
        # self.image_pub = rospy.Publisher("cv_image", Image, queue_size=1)

    def image_callback(self, image_raw: Image):
        self.image_raw_np: np.ndarray = self.cv_bridge.imgmsg_to_cv2(image_raw, "bgr8")

        cv2.imshow("img", self.image_raw_np)
        cv2.waitKey(1)


def main():
    rospy.init_node("cv_cam3")
    cv_cam3 = CvCam3()
    rospy.spin()

    # def main(self):
    #     rospy.init_node("cv_cam3")
    #     rospy.spin()

    # def strategy(self):
    #     r = rospy.Rate(30)
    #     rospy.on_shutdown(self.cleanup)

    #     while not rospy.is_shutdown():
    #         if not self.image is None:
    #             msg = self.bridge.cv2_to_imgmsg(self.image)
    #             self.image_pub.publish(msg)
    #         r.sleep()


if __name__ == '__main__':
    main()
