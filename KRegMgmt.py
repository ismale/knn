# -*- coding: utf-8 -*-
import os
import numpy as np
import pickle
from KRegTrain import KRegTrain
from KRegPred import KRegPredict
from KRegSimu import KRegSimulation
import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

if __name__ == "__main__":

    dbpath = "kdb.db"
    last_epoch = 1920
    pre_epoch = 240
    each_epoch = 60
    use_models = 5
    target_range = np.arange(1.00, 2.21, 0.05)
#    target_range = np.arange(1.00, 1.51, 0.05)
    train_start_date = datetime.date(2004, 1, 1)
    train_end_date = datetime.date(2011, 12, 31)

    #初回学習
    train_start_str = train_start_date.strftime("%Y-%m-%d")
    train_end_str = train_end_date.strftime("%Y-%m-%d")
    KRegTrain(dbpath, train_start_str, train_end_str, pre_epoch, last_epoch)
    
    #ローリングウィンドウ法
    dir_name = 'Mgmt4Same28y60'
    param_file = dir_name + '/history.pkl'
    param = {}
#    if os.path.exists(param_file):
#        with open(param_file, mode='rb') as fi:
#            param = pickle.load(fi)
            
    epoch = pre_epoch
    last_epoch = max(last_epoch, epoch)
    while train_end_date < datetime.date(2018, 10, 1):
        #データ取得＆レコード作成
        test_start_date = train_end_date + relativedelta(days=1)
        test_end_date = test_start_date + relativedelta(months=3) - relativedelta(days=1)
        test_start_str = test_start_date.strftime("%Y-%m-%d")
        test_end_str = test_end_date.strftime("%Y-%m-%d")
        
        epoch_range = range(max(1, epoch - use_models + 1), epoch + 1, 1)
        n = param["n"] if "n" in param else 0
#        KRegPredict("kdb.db", train_start_str, train_end_str, satday, sunday, epoch_range, target_range)
#        if epoch >= last_epoch:
        if True:
            param = KRegSimulation(dbpath, test_start_str, test_end_str, epoch_range, target_range, param, output = False)
            param["n"] += n
            with open(param_file, mode='wb+') as fo:
                pickle.dump(param, fo)
            
        #追加学習
        m = test_start_date.strftime("%m")
        nm = (test_start_date + relativedelta(months=3)).strftime("%m")
#        if (int(m) != int(nm)) & (int(m) % 3 == 0): #QEnd
        if True:
#            if epoch >= last_epoch:
            if True:
                #結果表示
                stock = param["stock"] if "stock" in param else {}
                rate = param["rate"] if "rate" in param else {}
                pay = param["pay"] if "pay" in param else {}
                back = param["back"] if "back" in param else {}
                buyn = param["buyn"] if "buyn" in param else {}
                hitn = param["hitn"] if "hitn" in param else {}
                hist = param["hist"] if "hist" in param else {}
                down = param["down"] if "down" in param else {}
    
                print "target, buyn, horses, ret, hitn, pay, total, down"
                for target in target_range:
                    if target in hitn:
                        ret1 = (float(back[target]) / pay[target]) * 100 if pay[target] != 0 else 100.0
                        hit1 = (float(hitn[target]) / buyn[target]) * 100 if buyn[target] != 0 else 0.0
                        print "{:.2f}, {:6d}, {:6d}, {:6.2f}, {:6.2f}, {:10,d}, {:10,d}, {:10,d}".format(
                                float(target),
                                int(buyn[target]),
                                param["n"],
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
                    spanx = param["n"] / 25
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
                plt.title("train:{} eval:{}".format(train_end_date, test_end_date))
                plt.savefig("{}/{}_epoch{}.png".format(dir_name, test_end_date, epoch_range[-1]), dpi=200)
                plt.show()

                #rate再計算
#                if int(m) % 12 == 0: #YearEnd
#                    for target in target_range:
#                        param["rate"][target] = max(1000, min(300000, param["stock"][target] / 100))
    
            #学習
            train_start_date = train_start_date + relativedelta(months=3)
            train_end_date = train_start_date + relativedelta(years=8) - relativedelta(days=1)
            train_start_str = train_start_date.strftime("%Y-%m-%d")
            train_end_str = train_end_date.strftime("%Y-%m-%d")
            if epoch + each_epoch > last_epoch:
                KRegTrain(dbpath, train_start_str, train_end_str, epoch + each_epoch, last_epoch)
            epoch += each_epoch
            last_epoch = max(last_epoch, epoch)
        