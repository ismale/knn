# -*- coding: utf-8 -*-
import numpy as np
import chainer
from chainer import serializers
from KReg import knn, kdataset
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def KRegSimulation(dbpath, test_start, test_end, epoch_range, target_range, param = {}, output = True):
    
    test = kdataset(train = False, dbpath = dbpath, start = test_start, end = test_end)
    
    model = {}
    for e in epoch_range:
        model[e] = knn()
        serializers.load_npz(test.result_dir + "/predictor_epoch_" + str(e), model[e])
    
    stock = param["stock"] if "stock" in param else {}
    rate = param["rate"] if "rate" in param else {}
    pay = param["pay"] if "pay" in param else {}
    back = param["back"] if "back" in param else {}
    buyn = param["buyn"] if "buyn" in param else {}
    hitn = param["hitn"] if "hitn" in param else {}
    hist = param["hist"] if "hist" in param else {}
    down = param["down"] if "down" in param else {}
    
    hppn = {}
    for i, target in enumerate(np.arange(1.00, 1.51, 0.05)):
        hppn[target] = 0.1 + 0.01 * (i + 1)
    for i, target in enumerate(np.arange(1.55, 3.01, 0.05)):
        hppn[target] = 0.21 + 0.05 * (i + 1)
    
    n = param["n"] if "n" in param else 0
    for i in range(test.__len__()):
    #for i in range(1000):
        x, t = test.get_example(i)

        y = 0.0
        l = []
        for e in epoch_range:
            with chainer.using_config('train', False):
                y = model[e].fwd(np.array([x], dtype=np.float32)).data[0][0]
                l.append(y)
#        y = np.mean(l)
#        y = np.median(l)
#        y = np.max(l)

            for target in target_range:
                hasHit = False
                hasBuy = False
                if target not in stock: stock[target] = 100000
                if target not in rate: rate[target] = 1000
                if target not in pay: pay[target] = 0
                if target not in back: back[target] = 0
                if target not in buyn: buyn[target] = 0
                if target not in hitn: hitn[target] = 0
                if target not in hist: hist[target] = []
                if target not in down: down[target] = stock[target]
                back1 = 0
                if y > target: #ターゲットおいしさ指数以上で購入
                    hasBuy = True
                    pay1 = rate[target]
                    pay1 -= pay1 % 100
                    pay[target] += pay1
                    stock[target] -= pay1
                    buyn[target] += 1
                    if t[0] > 0: #配当あり？（当たり？）
                        hasHit  = True
                        back1 = pay1 * t[0]
                        back[target] += back1
                        hitn[target] += 1
                        stock[target] += back1
                    ret1 = float(back[target]) / pay[target] * 100.0
                    hist[target].append([n + i, ret1])
                    down[target] = min(down[target], stock[target])
    #                print "{} {} {}".format(test.env.area_name.encode('utf-8'), test.env.race_number, test.env.horse_numbers[test.env.horse])
                    print "{:5d} t:{:.2f} {:6.2f}％ {:10,d} ({:6,d})".format(n + i + 1, target, ret1, int(stock[target]), int(back1)),
                    print "{} {:2s} {:2d} {:2d} y = {:4.2f}".format(
                    test.env.date.encode('utf-8'), 
                    test.env.area_name.encode('utf-8'),
                    test.env.race_number,
                    test.env.horse_numbers[test.env.horse],
                    y)
    #            if hasBuy:
    #                if not hasHit:
    #                    rate[target] += 1000
    #                else:
    #                    rate[target] = 1000

    if output:
        print "target, buyn, horses, ret, hitn, pay, total, down"
        for target in target_range:
            if target in hitn:
                ret1 = (float(back[target]) / pay[target]) * 100 if pay[target] != 0 else 100.0
                hit1 = (float(hitn[target]) / buyn[target]) * 100 if buyn[target] != 0 else 0.0
                print "{:.2f}, {:6d}, {:6d}, {:6.2f}, {:6.2f}, {:10,d}, {:10,d}, {:10,d}".format(
                        float(target),
                        int(buyn[target]),
                        test.__len__(),
                        ret1,
                        hit1,
                        int(pay[target]),
                        int(stock[target]),
                        int(down[target]))

        fig, ax1 = plt.subplots()
        cmap = plt.get_cmap("tab20")
        ylim_min = 50
        ylim_max = 200
        ax1.grid(True)
        ax1.set_axisbelow(True)
        for i, target in enumerate(target_range):
            k = []
            v = []
            if len(hist[target]) > 0:
                h = np.array(hist[target])
                k = h[:, 0]
                v = h[:, 1]
            hit1 = (float(hitn[target]) / buyn[target]) * 100 if buyn[target] != 0 else 0.0
            ax1.plot(k, v, color=cmap(i), label="{:.2f}({:4,d}|{:.1f}%)".format(target, buyn[target], hit1))
            spanx = test.__len__() / 25
            spany = 10
            x0 = 0
            y0 = 0
            for i, (x, y) in enumerate(zip(k, v)):
                if ((x - x0) > spanx) or (abs(y - y0) > spany):
        #            ax1.text(x, min(400, y), "{:.1f}".format(y), ha='center', va='bottom' if i % 2 else 'top', fontsize=4)
                    ax1.text(x, max(ylim_min, min(ylim_max, y)), "{:.1f}".format(y), ha='center', va='bottom', fontsize=4)
                    x0 = x
                    y0 = y
                    
        ax1.yaxis.set_major_locator(MaxNLocator(nbins=8))
        ax1.set_ylim([ylim_min, ylim_max])
        ax1.axhline(y = 100, color="k")
        handler1, label1 = ax1.get_legend_handles_labels()
        ax1.legend(handler1, label1, loc='upper left', borderaxespad=0., fontsize=5)
        plt.title("train:{} eval:{}".format(epoch_range[-1], test_end))
        plt.savefig("{}/{}_epoch{}.png".format(test.result_dir, test_end, epoch_range[-1]), dpi=200)
        plt.show()

    return {"stock":stock, "rate":rate, "pay":pay, "back":back, "buyn":buyn, "hitn":hitn, "hist":hist, "down":down, "n":test.__len__()}

if __name__ == "__main__":
    epoch = 1800
    target = 1.0
    start = "2018-11-17"
    end = "2018-11-18"

    KRegSimulation("kdb.db", start, end, range(epoch - 3 + 1, epoch + 1, 1), np.arange(target, 2.01, 0.05))
