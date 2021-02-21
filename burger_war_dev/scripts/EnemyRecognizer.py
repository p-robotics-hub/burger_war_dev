import cv2
import numpy as np
from ColorExtractor import ColorExtractor
# print(cv2.__version__)


class EnemyRecognizer:
    def __init__(self, image):
        self.image = image
        self.red_image = ColorExtractor(image).extract_red()
        self.dist = None
        self.direct = None
    
    def get_complement_circle_info(self):
        _, cnts, _ = cv2.findContours(self.red_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if ((len(cnts)==0) or (len(cnts[0])<5)):
            return None
        (x, y), radius = cv2.minEnclosingCircle(cnts[0])
        return ((x, y), radius)
        # self.drawCenterMark((x, y), radius)
        # cv2.imshow('MinEnclosingCircle', self.image)
        # cv2.imwrite("../data/after_proc_image/10_detect_red_circle.jpg", self.image)
        # cv2.waitKey(0)

    def drawCenterMark(self, point, radius):
        npt = (int(point[0]), int(point[1]))
        r = int(radius)
        cv2.circle(self.image,npt,r,(0,0,0),2)

        cv2.drawMarker(self.image, npt, (0,0,0),
            markerType=cv2.MARKER_CROSS,
            markerSize=10, thickness=1)


if __name__ == '__main__':
    import glob
    import matplotlib.pyplot as plt
    image_list = glob.glob("burger_war_dev/data/image_raws/210*")

    enemy_recognizer = EnemyRecognizer(cv2.imread(image_list[0]))
    circle_info = enemy_recognizer.get_complement_circle_info()
    print(circle_info)
    
