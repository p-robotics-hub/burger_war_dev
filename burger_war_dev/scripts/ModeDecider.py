from ActMode import ActMode

class ModeDecider:
    def __init__(self):
        self.enemy_dist_min = 0.8
    
    def getActMode(self, current_mode, imgInfo, warState):
        if current_mode == ActMode.attack:
            gotten_enem_marker_num = sum(warState.is_enem_left_marker_gotten, warState.is_enem_back_marker_gotten, warState.is_enem_right_marker_gotten)
            if gotten_enem_marker_num>=2:
                return ActMode.basic
            return ActMode.attack

        elif current_mode == ActMode.basic:
            if imgInfo.is_enemy_recognized and imgInfo.enemy_dist < self.enemy_dist_min:
                return ActMode.attack
            else:
                return ActMode.basic
