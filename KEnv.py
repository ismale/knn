# -*- coding: utf-8 -*-
import gym
import random
import numpy as np
import gym.spaces

import sqlite3
from get_train_data import update_record

NONE_VALUE = -9999

def zscore(x, axis = None):
    xreal = np.array([xi for xi in x if xi != NONE_VALUE], dtype=np.float64)
    if len(xreal) == 0:
        return np.array([0] * len(x), dtype=np.float64)
    xmean = xreal.mean(axis=axis, keepdims=True)
    xstd  = np.std(xreal, axis=axis, keepdims=True)
    xzero = (x - xmean)
    xzero = [xzi if xi != NONE_VALUE else 0 for xi, xzi in zip(x, xzero)]
    if xstd != 0:
        xzero /= xstd
        
    return xzero

class KEnv(gym.Env):
    metadata = {'render.modes': ['human', 'ansi']}

    def __init__(self, train = True, dbpath = 'kdb.db', view_name = "kdb", step_offset = 0, horses = 1, start_price = 0.7, end_price = 1.35):
        super(KEnv, self).__init__()
        self.train = train
        self.kdb_name = " " + view_name + " "
        self.connection = sqlite3.connect(dbpath, isolation_level="IMMEDIATE")
        self.cursor = self.connection.cursor()
        # action_space, observation_space, reward_range を設定する
        self.action_space = gym.spaces.Discrete(2)  # 買わない、買う
        self.observation_space = gym.spaces.Discrete(62 - 1) #60
        self.reward_range = [-500, 500] #何倍になったか
        self.race_list = self.get_data("race_list")
        self.races = len(self.race_list)
        self.race = -1
        self.n = step_offset
        self.horses = horses
        self.valid_horses = 0
        self.start_price = start_price
        self.end_price = end_price
        self.R = 0
        self.B = 0
        self.done = True

    def reset(self):
        # 諸々の変数を初期化する
        if self.train:
            self.race = random.randrange(self.races) #注目RSインデックス
        else:
            self.race += 1
            self.race %= self.races
        self.date, self.area_name, self.race_number = self.race_list[self.race]
        self.done = False
        self.horse_numbers, exclude = self.get_data("horse_numbers")
        if exclude:
            return self.reset()
        self.heads = len(self.horse_numbers)

        #1レース分のデータを取得
        self.race_data = []
        for i in range(0, self.heads):
            self.horse = i #注目HSインデックス
#            print self.race, self.date, self.area_name, self.race_number, self.horse_numbers[self.horse]
            observation = self.observe() #次のHSデータ
            if len(observation) == 0:
                return self.reset()
            self.race_data.append(observation)

        #データ正規化
        self.race_data = np.array(self.race_data)
        for i in range(self.race_data.shape[1]):
            self.race_data[:,i] = zscore(self.race_data[:,i], axis = 0)
        
        #初回の観測データを返す
        self.horse = 0 #注目HSインデックス
        observation = self.race_data[self.horse] #次のHSデータ
        if len(observation) == 0:
            return self.reset()
        self.R = 0
        self.B = 0
        return observation

    def step(self, action):
        self.n += 1
        reward, back_vic, back_win, order = self.get_reward(action)
        self.R += reward
#        print action, reward
        # 1ステップ進める処理を記述。戻り値は observation, reward, done(ゲーム終了したか), info(追加の情報の辞書)
        self.horse += 1
        self.done = False
        if (self.horse < self.heads):
            observation = self.race_data[self.horse] #次のHSデータ
            if len(observation) == 0:
                self.done = True
        else:
            self.done = True

        if self.done:
            observation = [0] * self.observation_space.n
            observation = np.array(observation, dtype=np.float64)
        return observation, reward, self.done, {"back_vic":back_vic, "back_win":back_win, "order":order}

    def render(self, mode='human', close=False):
        pass

    def close(self):
        self.connection.close()

    def seed(self, seed=None):
        pass

    def get_reward(self, action):
        # 報酬を返す。
        # 何倍になったか（はずれは-1倍）
        back_vic, back_win, order = self.get_data("back")
        if action == 0: #買わない
            if self.train:
                reward = -back_vic
            else:
                reward = 0
        else: #買う
            if self.train:
#                reward = -1 * min(1, (1 * (float(self.n) / self.horses))) + back_vic / 0.732
#                reward = -0.2 * min(1, (1 * (float(self.n) / self.horses))) + back_vic / 0.732
                reward = -(self.start_price + (self.end_price - self.start_price) * float(self.n) / self.horses) + back_vic
            else:
                reward = -1.0 + back_vic
            self.B += 1
        return reward, back_vic, back_win, order
    
    def get_horses(self):
        if self.valid_horses == 0:
            for i in range(self.races):
                self.date, self.area_name, self.race_number = self.race_list[i]
                horse_numbers, exclude = self.get_data("horse_numbers")
                if not exclude:
                    self.valid_horses += len(horse_numbers)
        return self.valid_horses

    def update_records(self):
        for i in range(self.races):
            self.date, self.area_name, self.race_number = self.race_list[i]
            print self.date, self.race_number
            horse_numbers, exclude = self.get_data("horse_numbers")
            if not exclude:
                for hn in horse_numbers:
                    if hn > 0:
                        update_record(self.connection, self.cursor, self.date, self.area_name, self.race_number, hn)
            self.connection.commit()


    def observe(self):
        # 次HSの情報をDBから取得
        observation = self.get_data("hs")
        return observation

    def get_data(self, data_type=""):
        if data_type == "race_list":
#            sql = "SELECT date, area_name, race_number FROM (SELECT * FROM" + self.kdb_name + " WHERE JULIANDAY(date) >= JULIANDAY('2014-03-01') GROUP BY date, area_name, race_number ORDER BY JULIANDAY(date), race_number)"
            sql = "SELECT date, area_name, race_number FROM (SELECT * FROM" + self.kdb_name + " GROUP BY date, area_name, race_number ORDER BY JULIANDAY(date), race_number)"
            self.cursor.execute(sql)
            return self.cursor.fetchall()

        elif data_type == "horse_numbers":
            sql = "SELECT horse_number, race_name, track, finish_order FROM" + self.kdb_name + "WHERE date = ? AND area_name = ? AND race_number = ?"
            self.cursor.execute(sql, [self.date, self.area_name, self.race_number])
            s = self.cursor.fetchall()
            horse_numbers = [i[0] for i in s]
            finish_orders = [i[3] for i in s]
            exclude = False
            if str(s[0][1].encode('utf-8')).find("新馬") >= 0: exclude = True
            if str(s[0][1].encode('utf-8')).find("障害") >= 0: exclude = True
#            if str(s[0][1].encode('utf-8')).find("2歳") >= 0: exclude = True
#            if str(s[0][1].encode('utf-8')).find("２歳") >= 0: exclude = True
#            if str(s[0][1].encode('utf-8')).find("ハンデ") >= 0: exclude = True
#            if str(s[0][2].encode('utf-8')).find("芝") >= 0: exclude = True
            uorders = [unicode(i) for i in range(1, 19)]
            for order in finish_orders:
                if not order in uorders:
                    if not order is None:
                        exclude = True
            return horse_numbers, exclude

        elif data_type == "back":
            sql = "SELECT (CASE WHEN CAST(finish_order AS INT) = 1 THEN odds ELSE 0 END), CAST(finish_order AS INT) FROM" + self.kdb_name + "WHERE date = ? AND area_name = ? AND race_number = ? AND horse_number = ? AND CAST(finish_order AS INT) <> 0"
            self.cursor.execute(sql, [self.date, self.area_name, self.race_number, self.horse_numbers[self.horse]])
            s = self.cursor.fetchone()
            #odds, finish_order
            if not s:
                return 0.0, 0.0, 0;
            else:
                back_vic = float(s[0])
                back_win = 0
                return back_vic, back_win, int(s[1])

        elif data_type == "hs":

            sql = "\
                SELECT\
                    CAST(odds AS FLOAT),\
                    horse_name,\
                    horse_number,\
                    CASE WHEN horse_sex = '牡' THEN -1 WHEN horse_sex = '牝' THEN 1 ELSE 0 END,\
                    horse_age,\
                    load_weight,"
            for i in range(4):
                i = str(i + 1) if i != 0 else ""
                sql += "\
                    pre{}Span,\
                    pre{}DstRt,\
                    pre{}Purse,\
                    pre{}HeadsRt,\
                    CASE WHEN CAST(pre{}OOF AS INT) = 0 THEN NULL ELSE CAST(pre{}OOF AS INT) END,\
                    pre{}Number,\
                    CASE WHEN pre{}JWeightRt = 0 THEN 1 ELSE pre{}JWeightRt END,\
                    pre{}DTimeTop3,\
                    pre{}DTime3FTop3,".format(i,i,i,i,i,i,i,i,i,i,i)
            sql += "\
                pre4SameAreaAvgPurse,\
                pre4SameAreaAvgVicRt,\
                pre4SameAreaAvgWinRt,\
                pre4SameDstAvgPurse,\
                pre4SameDstAvgVicRt,\
                pre4SameDstAvgWinRt,\
                pre4SameJcyAvgPurse,\
                pre4SameJcyAvgVicRt,\
                pre4SameJcyAvgWinRt,"
            sql = sql[:-1]
            sql += "\
                FROM" + self.kdb_name + "\
                WHERE\
                    date = ? AND\
                    area_name = ? AND\
                    race_number = ? AND\
                    horse_number = ?"
            self.cursor.execute(sql, [self.date, self.area_name, self.race_number, self.horse_numbers[self.horse]])
            s = self.cursor.fetchone()
            s = list(s)
            for i, si in enumerate(s):
                if si == None:
                    s[i] = NONE_VALUE

            return np.array(s[2:], dtype=np.float64)

if __name__ == "__main__":
    env = KEnv(dbpath = "kdb.db", view_name = "kdb")
    env.update_records()