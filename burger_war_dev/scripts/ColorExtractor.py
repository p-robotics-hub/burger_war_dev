#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


# color extracted image using each rgb thresh
class ColorExtractor:
    def __init__(self, image):
        self.red_bgr_thresh = {"upper": (30, 30, 255), "lower": (0, 0, 70)}
        self.blue_bgr_thresh =  {"upper": (150, 20, 20), "lower": (100, 0, 0)}
        self.green_bgr_thresh = {"upper": (10, 255, 10), "lower": (0, 160, 0)}
        self.yellow_bgr_thresh = {"upper": (20, 255, 255), "lower": (0, 180, 180)}

        self.image = image
    
    def extract_red(self):
        red_mask = cv2.inRange(self.image, self.red_bgr_thresh["lower"], self.red_bgr_thresh["upper"]) 
        return red_mask

    def extract_blue(self):
        blue_mask = cv2.inRange(self.image, self.blue_bgr_thresh["lower"],self.blue_bgr_thresh["upper"]) 
        return blue_mask

    def extract_green(self):
        green_mask = cv2.inRange(self.image, self.green_bgr_thresh["lower"], self.green_bgr_thresh["upper"])
        return green_mask

    def extract_yellow(self):
        yellow_mask = cv2.inRange(self.image, self.yellow_bgr_thresh["lower"], self.yellow_bgr_thresh["upper"]) 
        return yellow_mask


# for development
def main():
    import glob
    import os
    import matplotlib.pyplot as plt
    image_list = glob.glob("burger_war_dev/data/image_raws/1140*")
    print(os.getcwd())
    print(image_list)

    image = cv2.imread(image_list[0])    
    # print(type(image))
    # fig, axes= plt.subplots(2,2)
    color_extractor = ColorExtractor(image)

    image1 = color_extractor.extract_red()
    cv2.imshow("image1", image1)
    cv2.waitKey(0)
    # image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
    # axes[0][0].imshow(image1)
    
    # image2 = color_extractor.extract_red()
    # image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
    # axes[0][1].imshow(image2)

    # image3 = color_extractor.extract_green()
    # image3 = cv2.cvtColor(image3, cv2.COLOR_BGR2RGB)
    # axes[1][0].imshow(image3)

    # image4 = color_extractor.extract_yellow()
    # image4 = cv2.cvtColor(image4, cv2.COLOR_BGR2RGB)
    # axes[1][1].imshow(image4)

    # color_extractor = ColorExtractor(image)
    # image = color_extractor.extract_blue()
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # plt.imshow(image)
    # plt.show()

# if __name__ == '__main__':
#     main()
