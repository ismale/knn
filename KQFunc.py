# -*- coding: utf-8 -*-
import chainer
import chainer.functions as F
import chainer.links as L
import chainerrl

model_type = 2

if model_type == 1:

    class QFunction(chainer.Chain):
    
        def __init__(self, obs_size, n_actions):
            super(QFunction, self).__init__(
                l0 = L.Linear(obs_size, n_actions),
                )
            self.resDir = 'result7'
    
        def __call__(self, x, test=False):
            return chainerrl.action_value.DiscreteActionValue(self.l0(x))

elif model_type == 2:
    
    class QFunction(chainer.Chain):
    
        def __init__(self, obs_size, n_actions, n_hidden_channels = 500):
            super(QFunction, self).__init__(
                l0 = L.Linear(obs_size, n_hidden_channels),
                l2 = L.Linear(n_hidden_channels, n_actions),
                bn0=L.BatchNormalization(n_hidden_channels),
                )
            self.resDir = 'result8'
    
        def __call__(self, x, test=False):
            h = F.leaky_relu(self.bn0(self.l0(x)))
            return chainerrl.action_value.DiscreteActionValue(self.l2(h))

elif model_type == 3:

    class QFunction(chainer.Chain):
    
        def __init__(self, obs_size, n_actions, n_hidden_channels=1000):
            super(QFunction, self).__init__(
                l0 = L.Linear(obs_size, n_hidden_channels),
                l1 = L.Linear(n_hidden_channels, n_hidden_channels),
                l2 = L.Linear(n_hidden_channels, n_actions),
                bn0=L.BatchNormalization(n_hidden_channels),
                bn1=L.BatchNormalization(n_hidden_channels),
                )
            self.resDir = 'result9'
    
        def __call__(self, x, test=False):
            h = F.leaky_relu(self.bn0(self.l0(x)))
            h = F.leaky_relu(self.bn1(self.l1(h)))
            return chainerrl.action_value.DiscreteActionValue(self.l2(h))
