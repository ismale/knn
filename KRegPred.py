# -*- coding: utf-8 -*-
import numpy as np
import chainer
from chainer import serializers
from KReg import knn, kdataset
from get_train_data import get_race_data

def KRegPredict(dbpath, test_start, test_end, epoch_range, target_range):

    test = kdataset(train = False, dbpath = dbpath, start = test_start, end = test_end)
    
    model = {}
    for e in epoch_range:
        model[e] = knn()
        serializers.load_npz(test.result_dir + "/predictor_epoch_" + str(e), model[e])
    
    for i in range(test.__len__()):
        x, _ = test.get_example(i)
    
        for e in epoch_range:
            y = 0.0
            with chainer.using_config('train', False):
                y = model[e].fwd(np.array([x], dtype=np.float32)).data[0][0]
    
            for target in target_range:
                if y > target: #ターゲットおいしさ指数以上で購入
                    print "{} {:2s} {:2d} {:2d} y = {:4.2f}".format(
                            test.env.date.encode('utf-8'), 
                            test.env.area_name.encode('utf-8'),
                            test.env.race_number,
                            test.env.horse_numbers[test.env.horse],
                            y)
                    y = -1
                    break
#            if y < 0: break
    
if __name__ == "__main__":
    target = 1.2
    year = 2018
    epoch = 1800
    days = ["2018-11-17", "2018-11-18"]
    ptds = [(5, 5, 5), (8, 5, 5), (3, 3, 5)]

    #土日×３開催地×13レース
    for i, day in enumerate(days):
        for ptd in ptds:
            for r in range(1, 13):
                p, t, d = ptd;
#                get_race_data(day, year, p, t, d + i, r)
        KRegPredict("kdb.db", day, day, range(epoch - 3 + 1, epoch + 1, 1), np.arange(target, 2.01, 0.05))