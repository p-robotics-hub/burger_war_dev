from ActMode import ActMode

class ModeDecider:
    def __init__(self):
        self.enemy_dist_min = 1.2
    
    def getActMode(self, isEnemyRecognized, enemy_dist):
        if isEnemyRecognized and enemy_dist < self.enemy_dist_min:
            return ActMode.attack
        else:
            return ActMode.basic
