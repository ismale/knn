# -*- coding: utf-8 -*-
import numpy as np
import chainer
from chainer import serializers
import chainerrl
from KEnv import KEnv
from KQFunc import QFunction

max_steps = 3000000
use_steps = 2000000
cur_steps = max_steps - use_steps

env = KEnv(start_price = 1.3, end_price = 1.4, step_offset = use_steps, horses = max_steps)
eval_env = KEnv(False)
obs_size = env.observation_space.n
n_actions = env.action_space.n
q_func = QFunction(obs_size, n_actions)

if use_steps > 0:
    serializers.load_npz(q_func.resDir + "/" + str(use_steps) + "/model.npz", q_func) 
    explorer = chainerrl.explorers.ConstantEpsilonGreedy(
        epsilon=1.0 / 15 / 12, random_action_func=env.action_space.sample)
else:
    explorer = chainerrl.explorers.LinearDecayEpsilonGreedy(
    1.0 / 15, 1.0 / 15 / 12, max_steps, random_action_func=env.action_space.sample)

optimizer = chainer.optimizers.Adam(eps=1e-2)
optimizer.setup(q_func) #設計したq関数の最適化にAdamを使う
gamma = 1
replay_buffer = chainerrl.replay_buffer.ReplayBuffer(capacity = 10**6)
phi = lambda x:x.astype(np.float32, copy=False)##型の変換(chainerはfloat32型。float64は駄目)

agent = chainerrl.agents.DoubleDQN(
    q_func, optimizer, replay_buffer, gamma, explorer,
    replay_start_size=500, update_interval=1,
    target_update_interval=100, phi=phi)

chainerrl.experiments.train_agent_with_evaluation(
    agent, env,
    steps = max_steps,
    eval_n_runs = 100,
    max_episode_len = 20,
    eval_interval = cur_steps / 100,
    outdir = q_func.resDir,
    eval_env = eval_env,
    step_offset = use_steps)