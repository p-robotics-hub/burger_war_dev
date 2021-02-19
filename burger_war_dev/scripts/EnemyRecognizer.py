import cv2
import numpy as np
from ColorExtractor import ColorExtractor


class EnemyRecognizer:
    def __init__(self, image):
        self.image = image
        self.red_image = ColorExtractor(image).extract_red()
        self.dist = None
        self.direct = None
    
    def get_complement_circle_info(self) -> tuple:
        cnts, _ = cv2.findContours(self.red_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        ((x, y), radius) = cv2.minEnclosingCircle(cnts[0])
        return ((x, y), radius)
        # print(circle_info)
        # img = cv2.circle(img,center,radius,(0,255,0),2)
        # return img
        # self.drawCenterMark((center[0], center[1]), radius)
        # cv2.imshow('MinEnclosingCircle', self.image)
        # cv2.imwrite("../data/after_proc_image/10_detect_red_circle.jpg", self.image)
        # cv2.waitKey(1)

    # 円のセンターマークを描画
    def drawCenterMark(self, point, radius):
        npt = (int(point[0]), int(point[1]))
        r = int(radius)
        cv2.circle(self.image,npt,r,(0,0,0),2)

        cv2.drawMarker(self.image, npt, (0,0,0),
            markerType=cv2.MARKER_CROSS,
            markerSize=10, thickness=1)


# if __name__ == '__main__':
#     import glob
#     import matplotlib.pyplot as plt
#     image_list = glob.glob("../data/image_raws/10*")

#     enemy_recognizer = EnemyRecognizer(cv2.imread(image_list[0]))
#     circle_info = enemy_recognizer.get_complement_circle_info()
#     print(circle_info)
    
