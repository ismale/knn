# -*- coding: utf-8 -*-
import numpy as np
import pickle
import chainer
from chainer import Chain
import chainer.links as L
import chainer.functions as F
from chainer import dataset
from KEnv import KEnv
import sqlite3

model_type = 1

if model_type == 1:

    class knn(Chain):
        def __init__(self):
            super(knn, self).__init__(
                l1=L.Linear(None, 1), #単勝回収率
            )
            self.resDir = 'resultR7'
#            self.resDir = 'resultR7(+100ep)'
            
        def __call__(self, x):
            y = self.fwd(x)
            return y
    
        def fwd(self, x):
            return self.l1(x)

elif model_type == 2:

    class knn(Chain):
        def __init__(self):
            super(knn, self).__init__(
                l1=L.Linear(None, 4),
                l2=L.Linear(None, 1), #単勝回収率
                bn1=L.BatchNormalization(4),
            )
            self.resDir = 'resultR8'

        def __call__(self, x):
            y = self.fwd(x)
            return y
    
        def fwd(self, x):
            h = F.leaky_relu(self.bn1(self.l1(x)))
            return self.l2(h)
    
class Regressor(Chain):

    def __init__(self, predictor):
        super(Regressor, self).__init__(predictor=predictor)

    def __call__(self, x, y):
        pred = self.predictor(x)
        loss = F.mean_squared_error(pred, y)
        chainer.report({'loss': loss}, self)

        return loss

class kdataset(dataset.DatasetMixin):
    def __init__(self, train = True, dbpath = 'kdb.db', start = "", end = ""):
        connection = sqlite3.connect(dbpath)
        cursor = connection.cursor()
        
        self.result_dir_name = start[:4] + (("TO" + end[:4]) if start[:4] != end[:4] else "")
#        self.result_dir = "PRE10PSNJ/" + self.result_dir_name
        self.result_dir = "Mgmt4Same28y60"
        view_name = "kdb" + self.result_dir_name
        
        cursor.execute("DROP VIEW IF EXISTS {}".format(view_name))
        cursor.execute("\
            CREATE VIEW {} AS SELECT * FROM kdb\
            WHERE JULIANDAY('{}') <= JULIANDAY(date) AND JULIANDAY(date) <= JULIANDAY('{}')".format(
            view_name, start, end))
        connection.commit()

        self.env = KEnv(train = train, dbpath = dbpath, view_name = view_name)        
    
    def __len__(self):
#        return int(self.env.races * 14.9)
        return self.env.get_horses()

    def get_example(self, i):
        if self.env.done:
            observation = self.env.reset()
        else:
            observation, _, done, _ = self.env.step(1)            
            if done:
                return self.get_example(i + 1)

        vx = np.array(observation, dtype=np.float32)
        back_vic, _, _ = self.env.get_data("back")
        vt = np.array([back_vic], dtype=np.float32)
        return vx, vt
