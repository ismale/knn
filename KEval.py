# -*- coding: utf-8 -*-
import numpy as np
import chainer
from chainer import serializers
import chainerrl
from KEnv import KEnv
from KQFunc import QFunction

env = KEnv(True, ratio = 0.2)
obs_size = env.observation_space.n
n_actions = env.action_space.n
q_func = QFunction(obs_size, n_actions)

use_step = 2810013
if use_step > 0:
    serializers.load_npz(q_func.resDir + "/" + str(use_step) + "/model.npz", q_func) 

optimizer = chainer.optimizers.Adam(eps=1e-2)
optimizer.setup(q_func) #設計したq関数の最適化にAdamを使う
gamma = 1
explorer = chainerrl.explorers.ConstantEpsilonGreedy(
    epsilon=0, random_action_func=env.action_space.sample)
replay_buffer = chainerrl.replay_buffer.ReplayBuffer(capacity = 10**6)
phi = lambda x:x.astype(np.float32, copy=False)##型の変換(chainerはfloat32型。float64は駄目)

agent = chainerrl.agents.DoubleDQN(
    q_func, optimizer, replay_buffer, gamma, explorer,
    replay_start_size=500, update_interval=1,
    target_update_interval=100, phi=phi)

back_vic = 0.
back_win = 0.
buy = 0.
nbuy = 0.
nvic = 0
nwin = 0
vic_list = []
win_list = []

observation = env.reset()
#while(env.race < env.races - 1):
for i in range(env.races * 15):
    action = agent.act(observation)
    observation, reward, done, info = env.step(action)
    if action == 1: #買う
        buy += 1
        if info["order"] == 1:
            back_vic += info["back_vic"]
            nvic += 1
            vic_list.append(info["back_vic"])

        if info["order"] <= 3:
            back_win += info["back_win"]
            nwin += 1
            win_list.append(info["back_win"])
    else:
        nbuy += 1

    if done:
        env.reset()

print "buy:{:d}/{:d}".format(int(buy), int(buy + nbuy))
print "vic back:{} ret:{:.2f}％ hit:{:.2f}％".format(back_vic, ((back_vic / buy) * 100) if buy != 0 else 100, ((nvic / buy) * 100) if buy != 0 else 0)
print "win back:{} ret:{:.2f}％ hit:{:.2f}％".format(back_win, ((back_win / buy) * 100) if buy != 0 else 100, ((nwin / buy) * 100) if buy != 0 else 0)
print vic_list
print win_list
