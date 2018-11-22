# -*- coding: utf-8 -*-
import numpy as np
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestRegressor
from KEnv import KEnv
import pickle
import os

X = []
y_back = []
y_reward = []
y_order = []

env = KEnv(False, ratio = 0.8)
#for i in range(int(15 * 12 * 3 * 2 * 4.35 * 12)):
while(env.race < env.races - 1):
    observation, reward, done, info = env.step(1)
    if not done:
        X.append(observation)
        y_back.append(info['back'])
        y_reward.append(reward)
        y_order.append(info['order'])
    else:
        env.reset()
    
X = np.array(X)
feature_names = [
#    "odds",
    "horse_number",
    "horse_sex",
    "horse_age",
    "load_weight",
    "horse_weight",
    "dhorse_weight",
    "preSpan",
    "preHeadsRt",
    "preOOF",
    "preNumber",
    "preJWeightRt",
    "preHWeightRt",
    "preDHWeight",
    "preRespond",
    "preDTimeTop3",
    "preDTime3FTop3",
    "pre2Span",
    "pre2HeadsRt",
    "pre2OOF",
    "pre2Number",
    "pre2JWeightRt",
    "pre2HWeightRt",
    "pre2DHWeight",
    "pre2Respond",
    "pre2DTimeTop3",
    "pre2DTime3FTop3",
    "pre4AvgDstRt",
    "pre4AvgPurse",
    "pre4AvgVicRt",
    "pre4AvgWinRt",
    "pre4AvgRespond",
    "enterTimes",
    "pstAvgDstRt",
    "pstAvgPurse",
    "pstAvgVicRt",
    "pstAvgWinRt",
    "pstAvgRespond",
    "pre4SameAreaAvgPurse",
    "pre4SameAreaAvgVicRt",
    "pre4SameAreaAvgWinRt",
    "pre4SameAreaAvgRespond",
    "pre4SameDstAvgPurse",
    "pre4SameDstAvgVicRt",
    "pre4SameDstAvgWinRt",
    "pre4SameDstAvgRespond",
    "pre4SameCondAvgPurse",
    "pre4SameCondAvgVicRt",
    "pre4SameCondAvgWinRt",
    "pre4SameCondAvgRespond",
    "pre4SameJcyAvgPurse",
    "pre4SameJcyAvgVicRt",
    "pre4SameJcyAvgWinRt",
    "pre4SameJcyAvgRespond",
    "pre4AvgJcyPurse",
    "pre4AvgJcyWin",
    "pre4AvgJcyVic",
    "pstAvgJcyPurse",
    "pstAvgJcyVic",
    "pstAvgJcyWin",
    "pstAvgTrnWin",
    "pstAvgTrnVic"
]

#rf_back = RandomForestRegressor(n_estimators=10)
#rf_back = rf_back.fit(X, y_back)
##rf_back = rf_back.fit(X[:,1:], y_back)
#
#fti_back = rf_back.feature_importances_
#
#fti_back_ns = zip(fti_back, feature_names)
##fti_back_ns = zip(fti_back, feature_names[1:])
#fti_back_ns = sorted(fti_back_ns, reverse=True)
#
#print('Feature Importances(back):')
#for i, ftin in enumerate(fti_back_ns):
#    print('\t{0:30s} : {1:>.6f}'.format(ftin[1], ftin[0]))
#
fti_reward_ave = [0] * 61
for i in range(10):
    rf_reward = RandomForestRegressor(n_estimators=10)
    rf_reward = rf_reward.fit(X, y_reward)
    #rf_reward = rf_reward.fit(X[:,1:], y_reward)
    
    fti_reward = rf_reward.feature_importances_
    fti_reward_ave += fti_reward
fti_reward /= 10.0
    
fti_reward_ns = zip(fti_reward, feature_names)
#fti_reward_ns = zip(fti_reward, feature_names[1:])
fti_reward_ns = sorted(fti_reward_ns, reverse=True)

print('Feature Importances(reward):')
for i, ftin in enumerate(fti_reward_ns):
    print('\t{0:30s} : {1:>.6f}'.format(ftin[1], ftin[0]))

#rf_order = RandomForestRegressor(n_estimators=10)
#rf_order = rf_order.fit(X, y_order)
##rf_order = rf_order.fit(X[:,1:], y_order)
#
#fti_order = rf_order.feature_importances_
#
#fti_order_ns = zip(fti_order, feature_names)
##fti_order_ns = zip(fti_order, feature_names[1:])
#fti_order_ns = sorted(fti_order_ns, reverse=True)
#
#print('Feature Importances(order):')
#for i, ftin in enumerate(fti_order_ns):
#    print('\t{0:30s} : {1:>.6f}'.format(ftin[1], ftin[0]))