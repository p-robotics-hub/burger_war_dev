from scripts.ActMode import ActMode
from burger_war_dev.msg import ImgInfo, WarState, ScanInfo


test_cases = [
    {
        "input": {
            "current_mode": ActMode.basic,
            "info_dict": {
                "img_info": ImgInfo(False, 0, 0, False, 0),
                "war_state": WarState(False, False, False),
                "scan_info": ScanInfo(False, 0, 0)            
            }
        },
        "next_mode": ActMode.basic
    },
    {
        "input": {
            "current_mode": ActMode.basic,
            "info_dict": {
                "img_info": ImgInfo(False, 0, 0, False, 0),
                "war_state": WarState(False, False, False),
                "scan_info": ScanInfo(True, 0.7, 0)            
            }
        },
        "next_mode": ActMode.attack
    }

]