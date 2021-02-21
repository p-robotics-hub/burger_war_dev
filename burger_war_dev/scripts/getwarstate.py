#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This is get warstate node.
subscribe No topcs.
Publish 'warstate' topic. 

'''

import rospy
from warstate_msgs.msg import WarState


class PupeRun():

    def __init__(self, bot_name="NoName"):
        
        # bot name 
        self.name = puperun
        # warstate publisher
        self.warstate_pub = rospy.Publisher('warstate', WarState,queue_size=1)

        self.game_timestamp = 0
        self.my_score = 0
        self.enemy_score = 0
        self.Is_lowwer_score = False
        self.all_field_score = np.ones([18])  # field score state
        self.all_field_score_prev = np.ones([18])  # field score state (previous)
        self.enemy_get_target_no = -1
        self.enemy_get_target_no_timestamp = -1
        self.enemy_body_remain = 3

        # warstate callback should be called after all parameter is ready!!
        rospy.Timer(rospy.Duration(0.11), self.WarState_timerCallback)
        JUDGE_URL = rospy.get_param('/send_id_to_judge/judge_url')
        
        # RESPECT @F0CACC1A
    def WarState_timerCallback(self, state):
        self.getWarState()

        # RESPECT seigorun2.py
    def getWarState(self):
        # get current state from judge server
        resp = requests.get(JUDGE_URL + "/warState")
        dic = resp.json()
        # get score
        if self.my_side == "r":  # red_bot
            self.my_score = int(dic["scores"]["r"])
            self.enemy_score = int(dic["scores"]["b"])
        else:  # blue_bot
            self.my_score = int(dic["scores"]["b"])
            self.enemy_score = int(dic["scores"]["r"])

        self.game_timestamp = int(dic["time"])

        # get warstate score state and compare previous value
        for idx in range(18):  # number of field targets, how to get the number?
            self.all_field_score_prev[idx] = self.all_field_score[idx]
            target_state = dic["targets"][idx]["player"]
            if target_state == "n":
                self.all_field_score[idx] = 1  # no one get this target
            elif target_state == self.my_side:
                self.all_field_score[idx] = 0  # my_bot get this target
            else:
                self.all_field_score[idx] = 2  # enemy get this target

            # check if field score is updated.
            if self.all_field_score[idx] != self.all_field_score_prev[idx]:
                if self.all_field_score[idx] == 2:
                    print("enemy get target No.", idx, self.game_timestamp)
                    self.enemy_get_target_no = idx
                    self.enemy_get_target_no_timestamp = self.game_timestamp
        # update field score state to check enemy get target

        self.waypoint.set_field_score(self.all_field_score[6:])

        # update body AR marker point
        if self.my_side == "b":
            self.enemy_body_remain = np.sum(self.all_field_score[3:6])
        elif self.my_side == "r":
            self.enemy_body_remain = np.sum(self.all_field_score[0:3])

        # update which bot is higher score
        if self.my_score <= self.enemy_score:
            self.Is_lowwer_score = True
        else:
            self.Is_lowwer_score = False
        #print("Is_lowwer_score", self.Is_lowwer_score)

   def strategy(self):
        r = rospy.Rate(1) # change speed 1fps
      
        while not rospy.is_shutdown():
            warstate = self.getwarstate()
            print(warstate)
            self.warstate_pub.publish(warstate)

            r.sleep()

if __name__ == '__main__':
    rospy.init_node('get_war_state')
    Puperun = Puperun('Puperun')
    Puperun.strategy()