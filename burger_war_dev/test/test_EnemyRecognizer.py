import os
import glob
import unittest2

import cv2

from scripts.EnemyRecognizer import EnemyRecognizer


class TestEneRec(unittest2.TestCase):
    def setUp(self):
        self.test_images = glob.glob("data/image_raws/*")
        
    def test_get_complement_circle_info(self):
        file_folder = "data/image_raws/"
        test_cases = [{"file": "1.jpg", "isEnemyRecgnized": True},
                      {"file": "10.jpg", "isEnemyRecgnized": True},
                      {"file": "20.jpg", "isEnemyRecgnized": True},
                      {"file": "30.jpg", "isEnemyRecgnized": True},
                      {"file": "46.jpg", "isEnemyRecgnized": False},
                      {"file": "57.jpg", "isEnemyRecgnized": True},
                      {"file": "200.jpg", "isEnemyRecgnized": True},
                      {"file": "210.jpg", "isEnemyRecgnized": False},
                      {"file": "410.jpg", "isEnemyRecgnized": True},
                      {"file": "940.jpg", "isEnemyRecgnized": False},
                      {"file": "1130.jpg", "isEnemyRecgnized": True},
                      {"file": "1240.jpg", "isEnemyRecgnized": False}]

        for case in test_cases:
            with self.subTest(file=case["file"]):
                file_path = file_folder + case["file"]
                print(case["file"])
                enemy_rec = EnemyRecognizer(cv2.imread(file_path))
                self.assertEqual(bool(enemy_rec.get_complement_circle_info()), case["isEnemyRecgnized"])
