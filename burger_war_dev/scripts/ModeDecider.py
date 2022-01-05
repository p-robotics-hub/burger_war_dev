from ActMode import ActMode
from burger_war_dev.msg import ImgInfo, WarState, ScanInfo

class ModeDecider:
    def __init__(self):
        self.enemy_dist_min = 0.9
    
    def getActMode(self, current_mode, war_state, img_info, scan_info):
        if current_mode == ActMode.attack:
            gotten_enem_marker_num = sum([war_state.is_enem_left_marker_gotten, war_state.is_enem_back_marker_gotten, war_state.is_enem_right_marker_gotten])
            if gotten_enem_marker_num>=2:
                # 理想は Defense Mode 
                # 壁に背を向けて張り付いて，自マーカを見せないなど
                return ActMode.basic
            if not (scan_info.is_enemy_recognized or img_info.is_enemy_marker_recognized):
                return ActMode.basic
            return ActMode.attack

        elif current_mode == ActMode.basic:
            print(scan_info)
            if scan_info.is_enemy_recognized and scan_info.enemy_dist < self.enemy_dist_min:
                return ActMode.attack
            else:
                return ActMode.basic


# if __name__ == '__main__':
#     mode_decider = ModeDecider()
#     img_info = ImgInfo(False, 0, 0, False, 0)
#     war_state = WarState(False, True, False)
#     scan_info = ScanInfo(True, 0.8, 0)
#     info_dict = {
#             "img_info": img_info,
#             "war_state": war_state,
#             "scan_info": scan_info
#         }
#     next_mode = mode_decider.getActMode(current_mode=ActMode.attack, **info_dict)
#     print(next_mode)
