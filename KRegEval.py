# -*- coding: utf-8 -*-
import numpy as np
import chainer
from chainer import serializers
from KReg import knn, kdataset
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import os

train_view_name = "kdb2011to15"
test_view_name = "kdb2016"
epoch_range = range(1, 51, 1)
target_range = np.arange(0.5, 2.0, 0.05)

model = knn()

test = kdataset(False, view_name = test_view_name)

train_dir = model.resDir + "(" + train_view_name + ")"
test_dir = train_dir + "/" + test_view_name

if not os.path.exists(test_dir):
    os.mkdir(test_dir)

#検証するエポック番号を指定する
for e in epoch_range:
    serializers.load_npz(train_dir + "/model_epoch_" + str(e), model)

    buyn = {}
    back = {}
    hitn = {}
    stock = {}
    pay = {}
    for i in range(test.__len__()):
#    for i in range(100):
        x, t = test.get_example(i)
        y = 0.0
        with chainer.using_config('train', False):
            y = model.fwd(np.array([x], dtype=np.float32)).data[0][0]

        for target in target_range:
            stock[target] = 0.0 if target not in stock else stock[target]
            pay[target] = 0 if target not in pay else pay[target]
            if y > target: #ターゲットおいしさ指数以上で購入
                pay1 = 100
                pay1 -= pay1 % 100
                pay[target] += pay1
                stock[target] -= pay1
                buyn[target] = (buyn[target] + 1) if target in buyn else 1
                if t[0] > 0: #配当あり？（当たり？）
                    back[target] = (back[target] + t[0]) if target in back else t[0]
                    hitn[target] = (hitn[target] + 1) if target in hitn else 1
                    back1 = pay1 * t[0]
                    stock[target] += back1
    
    print "epoch, index, buyn, horses, ret, hitn, pay, total"
    target_list = []
    ret = []
    hit = []
    bn = []
    for target in target_range:
        if target in hitn:
            target_list.append(target)
            ret1 = ((float(back[target]) / buyn[target]) * 100) if buyn[target] != 0 else 100.0
            hit1 = ((float(hitn[target]) / buyn[target]) * 100) if buyn[target] != 0 else 0.0
            print "{:d}, {:.2f}, {:6d}, {:6d}, {:6.2f}, {:6.2f}, {:10d}, {:10d}".format(
                    e,
                    float(target),
                    int(buyn[target]),
                    test.__len__(),
                    ret1,
                    hit1,
                    int(pay[target]),
                    int(stock[target]))
            ret.append(ret1)
            hit.append(hit1)
            bn.append(int(buyn[target]))
    
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
     
    ax1.grid(True)
#    ax2.grid(False)
    ax1.set_axisbelow(True)
    ax1.bar(target_list, bn, color="c", label="buy", width=0.04, align="center")
    ax2.plot(target_list, ret, color="r", label="ret")
    ax2.plot(target_list, hit, color="m", label="hit")
    for i, (x, y) in enumerate(zip(target_list, bn)):
        ax1.text(x, min(1000, y), y, ha='center', va='bottom' if i % 2 else 'top', fontsize=6)
    for i, (x, y) in enumerate(zip(target_list, hit)):
        ax2.text(x, y, "{:.1f}".format(y), ha='center', va='bottom' if i % 2 else 'top', fontsize=6)
    for i, (x, y) in enumerate(zip(target_list, ret)):
        ax2.text(x, min(250, y), "{:.1f}".format(y), ha='center', va='bottom' if i % 2 else 'top', fontsize=6)
    ax1.yaxis.set_major_locator(MaxNLocator(nbins=10))
    ax2.yaxis.set_major_locator(MaxNLocator(nbins=10))
    ax1.set_xlim([0.5, 2.0])
    ax1.set_ylim([0, 1000])
    ax2.set_ylim([0, 250])
    ax2.axhline(y = 100, color="k")
    handler1, label1 = ax1.get_legend_handles_labels()
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(handler1 + handler2, label1 + label2, loc=1, borderaxespad=0.)
    plt.title("epoch {}".format(e))
#    plt.legend()
    plt.savefig(test_dir + "/fig_{}.png".format(e), dpi=200)
    plt.show()
