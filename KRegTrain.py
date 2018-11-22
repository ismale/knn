# coding: utf-8
import chainer
from chainer import optimizers
from chainer import training
from chainer import serializers
from chainer.training import extensions
from KReg import knn, Regressor, kdataset
from KRegSimu import KRegSimulation
import numpy as np
import os
import pprint

model = Regressor(knn())
optimizer = optimizers.Adam()
optimizer.setup(model)

def KRegTrain(dbpath, train_start, train_end, max_epoch = 100, epoch_offset = 0):

    train = kdataset(True, dbpath, train_start, train_end)
    
    batchsize = 100
    epoch = max_epoch
    snapshot_interval = 1
    train_iter = chainer.iterators.SerialIterator(train, batchsize)
    train_iter.epoch = epoch_offset

    # Set up a trainer
    updater = training.StandardUpdater(train_iter, optimizer)
    trainer = training.Trainer(updater, (epoch, 'epoch'), out=train.result_dir)
    
    trainer.extend(extensions.LogReport())
    trainer.extend(extensions.snapshot(filename='trainer_last'))
    trainer.extend(extensions.snapshot_object(model.predictor, 'predictor_epoch_{.updater.epoch}'), trigger=(snapshot_interval, 'epoch'))
    trainer.extend(extensions.snapshot_object(model, 'model_epoch_{.updater.epoch}'), trigger=(snapshot_interval, 'epoch'))
    trainer.extend(extensions.snapshot_object(optimizer, 'optimizer_epoch_{.updater.epoch}'), trigger=(snapshot_interval, 'epoch'))
    trainer.extend(extensions.ProgressBar())
    
#    trainer_last_path = train.result_dir + '/trainer_last'
#    if os.path.exists(trainer_last_path):
##        s = np.load(trainer_last_path)
##        pprint.pprint(s.keys())
#        serializers.load_npz(trainer_last_path, trainer)

    model_last_path = train.result_dir + '/model_epoch_{}'.format(epoch_offset)
    if os.path.exists(model_last_path):
        serializers.load_npz(model_last_path, model)

    optimizer_last_path = train.result_dir + '/optimizer_epoch_{}'.format(epoch_offset)
    if os.path.exists(optimizer_last_path):
        serializers.load_npz(optimizer_last_path, optimizer)

    # Run the training
    trainer.run()

if __name__ == "__main__":
    dbpath = "kdb.db"
#    for e in range(1, 101, 10):
    last_epoch = 1800
    train_start = "2011-07-01"
    train_end = "2018-06-30"
    test_start = "2018-10-01"
    test_end = "2018-12-31"
    KRegTrain(dbpath, train_start, train_end, 60, last_epoch)
#    KRegSimulation(dbpath, train_start, train_end, test_start, test_end, range(max(1, e - 100), e + 1, 1), np.arange(1.4, 1.91, 0.05))
#    last_epoch = max(last_epoch, e)