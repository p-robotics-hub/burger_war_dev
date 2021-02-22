import cv2
import numpy as np
import math
from ColorExtractor import ColorExtractor
# print(cv2.__version__)


class EnemyRecognizer:
    def __init__(self, image):
        self.image = image
        self.red_image = ColorExtractor(image).extract_red()
        self.isEnemyRecognized = self.judgeIsEnemyRecognized()
        self.const = 222
        self.dist = None
        self.direct = None

    
    def get_complement_circle_info(self):
        if self.isEnemyRecognized:
            _, cnts, _ = cv2.findContours(self.red_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            (x, y), radius = cv2.minEnclosingCircle(cnts[0])
            return ((x, y), radius)
        # elif ((len(cnts)==0) or (len(cnts[0])<5)):
        #     return None
        else:            
            return None
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

    def calcDistance(self):
        # dist_radius_list = [[7, 32],
        #                     [10, 22],
        #                     [15, 15],
        #                     [20, 11],
        #                     [25, 9]]
        if self.isEnemyRecognized:
            (_, _), radius = self.get_complement_circle_info()        
            distance = self.const/radius
            return distance  
        else:
            return None  
    
    def calcDirection(self):
        if self.isEnemyRecognized:
            balloon_r = 0.0325
            center_index = np.argmax(self.red_image.sum(axis=0))
            direct = math.degrees(math.atan((center_index-320)*balloon_r/self.const))
            return direct 
        else:
            return None         
            

    def judgeIsEnemyRecognized(self):
        if np.max(self.red_image.sum(axis=0))<5:
            return False
        else:
            return True


if __name__ == '__main__':
    import glob
    import matplotlib.pyplot as plt
    # image_list = glob.glob("burger_war_dev/data/image_distance/*")
    image_list = glob.glob("burger_war_dev/data/image_raws/46*")
    image_path = image_list[0]

    enem_rec = EnemyRecognizer(cv2.imread(image_path))
    # print(len(enem_rec.red_image))
    print(image_path)
    print(enem_rec.calcDirection())
    print(enem_rec.calcDistance())
