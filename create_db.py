# coding: utf-8
import sqlite3
import csv

#SQLite
dbpath = 'kdb2.db'
connection = sqlite3.connect(dbpath)
class Median:
    def __init__(self):
        self.values = []

    def step(self, value):
        self.values.append(value)

    def finalize(self):
        srtd = sorted(self.values)
        alen = len(srtd)
        return 0.5*(srtd[(alen-1)//2] + srtd[alen//2])
connection.create_aggregate("median", 1, Median)

class FakeModeValue:
    def __init__(self):
        self.freq_dict = {}
    def step(self, value):
        self.freq_dict[value] = self.freq_dict.get(value, 0) + 1
    def finalize(self):
        if not self.freq_dict:
            return None
        return sorted(self.freq_dict.items(), key=lambda x: x[1], reverse=True)[0][0]

connection.create_aggregate('mode', 1, FakeModeValue)
cursor = connection.cursor()

#MySql
#connection = mysql.connector.connect(
#        host='localhost',
#        port='3306',
#        db='kdb',
#        user='root',
#        password='eos-b210607',
#        charset='utf8'
#    )
#cursor = connection.cursor(buffered=True)
#
#try:
#    cursor.execute("DROP TABLE IF EXISTS kdb")
#    cursor.execute("CREATE TABLE IF NOT EXISTS kdb(\
#                        date DATE,\
#                        area_name TEXT,\
#                        race_number INT,\
#                        race_name TEXT,\
#                        track TEXT,\
#                        run_direction TEXT,\
#                        distance INT,\
#                        track_condition TEXT,\
#                        purse INT,\
#                        heads_count INT,\
#                        finish_order TEXT,\
#                        post_position INT,\
#                        horse_number INT,\
#                        horse_name TEXT,\
#                        horse_sex TEXT,\
#                        horse_age INT,\
#                        jockey_name TEXT,\
#                        time FLOAT,\
#                        margin TEXT,\
#                        waypoint_order TEXT,\
#                        time3F FLOAT,\
#                        load_weight INT,\
#                        horse_weight INT,\
#                        dhorse_weight TEXT,\
#                        odds_order INT,\
#                        odds FLOAT,\
#                        is_blinkers TEXT,\
#                        trainer_name TEXT,\
#                        comments_by_trainer TEXT,\
#                        evaluation_by_trainer TEXT,\
#                        preSpan FLOAT,\
#                        preDstRt FLOAT,\
#                        preCond TEXT,\
#                        preHeadsRt FLOAT,\
#                        preOOF INT,\
#                        preNumber INT,\
#                        preJWeight INT,\
#                        preHWeight INT,\
#                        preDHWeight TEXT,\
#                        preRespond INT,\
#                        preEval TEXT,\
#                        preDTimeTop3 FLOAT,\
#                        preDTime3FTop3 FLOAT,\
#                        pre2Span FLOAT,\
#                        pre2DstRt FLOAT,\
#                        pre2Cond TEXT,\
#                        pre2HeadsRt FLOAT,\
#                        pre2OOF INT,\
#                        pre2Number INT,\
#                        pre2JWeight INT,\
#                        pre2HWeight INT,\
#                        pre2DHWeight TEXT,\
#                        pre2Respond INT,\
#                        pre2Eval TEXT,\
#                        pre2DTimeTop3 FLOAT,\
#                        pre2DTime3FTop3 FLOAT,\
#                        pre4AvgDstRt FLOAT,\
#                        pre4AvgPurse FLOAT,\
#                        pre4AvgVicRt FLOAT,\
#                        pre4AvgWinRt FLOAT,\
#                        pre4AvgRespond FLOAT,\
#                        enterTimes INT,\
#                        pstAvgDstRt FLOAT,\
#                        pstAvgPurse FLOAT,\
#                        pstAvgVicRt FLOAT,\
#                        pstAvgWinRt FLOAT,\
#                        pstAvgRespond FLOAT,\
#                        pre4AvgJcyPurse FLOAT,\
#                        pre4AvgJcyWin FLOAT,\
#                        pre4AvgJcyVic FLOAT,\
#                        pstAvgJcyPurse FLOAT,\
#                        pstAvgJcyVic FLOAT,\
#                        pstAvgJcyWin FLOAT,\
#                        pstAvgTrnWin FLOAT,\
#                        pstAvgTrnVic FLOAT,\
#                        pre4SameAreaAvgPurse FLOAT,\
#                        pre4SameAreaAvgVicRt FLOAT,\
#                        pre4SameAreaAvgWinRt FLOAT,\
#                        pre4SameAreaAvgRespond FLOAT,\
#                        pre4SameDstAvgPurse FLOAT,\
#                        pre4SameDstAvgVicRt FLOAT,\
#                        pre4SameDstAvgWinRt FLOAT,\
#                        pre4SameDstAvgRespond FLOAT,\
#                        pre4SameCondAvgPurse FLOAT,\
#                        pre4SameCondAvgVicRt FLOAT,\
#                        pre4SameCondAvgWinRt FLOAT,\
#                        pre4SameCondAvgRespond FLOAT,\
#                        pre4SameJcyAvgPurse FLOAT,\
#                        pre4SameJcyAvgVicRt FLOAT,\
#                        pre4SameJcyAvgWinRt FLOAT,\
#                        pre4SameJcyAvgRespond FLOAT)")
#    cursor.execute("CREATE INDEX raceIdx on kdb(date, area_name, race_number)")
#    cursor.execute("CREATE INDEX horseIdx on kdb(date, area_name, race_number, horse_number)")
#    cursor.execute("CREATE INDEX horseNIdx on kdb(horse_name)")
#    cursor.execute("CREATE INDEX jockyNIdx on kdb(jockey_name)")
#    cursor.execute("CREATE INDEX trainerNIdx on kdb(trainer_name)")
#    cursor.execute("CREATE INDEX dateIdx on kdb(date)")
#
#    with open('jra_race_resultNN.csv', 'rU') as f:
#        b = csv.reader(f)
#        header = next(b)
#        for t in b:
#            # tableに各行のデータを挿入する。
#            t = [unicode(s, "utf8") for s in t]
#            t = tuple(t)
#            cursor.execute('INSERT INTO kdb (\
#                        date,\
#                        area_name,\
#                        race_number,\
#                        race_name,\
#                        track,\
#                        run_direction,\
#                        distance,\
#                        track_condition,\
#                        purse,\
#                        heads_count,\
#                        finish_order,\
#                        post_position,\
#                        horse_number,\
#                        horse_name,\
#                        horse_sex,\
#                        horse_age,\
#                        jockey_name,\
#                        time,\
#                        margin,\
#                        waypoint_order,\
#                        time3F,\
#                        load_weight,\
#                        horse_weight,\
#                        dhorse_weight,\
#                        odds_order,\
#                        odds,\
#                        is_blinkers,\
#                        trainer_name,\
#                        comments_by_trainer,\
#                        evaluation_by_trainer\
#                        )VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', t)
#        
#except sqlite3.Error as e:
#    print e.args[0]
#
#connection.commit()

print "----------全頭購入時の回収率----------"
sql = "SELECT count(*), AVG(case when finish_order = 1 then odds else 0 end) * 100.0 FROM kdb where cast(finish_order as int) <> 0"
cursor.execute(sql)
for s in cursor.fetchall():
    print "{:6d}点 回収率={:5.1f}％".format(s[0], s[1])

print "----------全頭購入時の複勝回収率----------"
sql = "SELECT count(*), AVG(case when CAST(finish_order AS INT) <= 3 then odds_win else 0 end) * 100.0 FROM kdb where cast(finish_order as int) <> 0"
cursor.execute(sql)
for s in cursor.fetchall():
    print "{:6d}点 回収率={:5.1f}％".format(s[0], s[1])

print "----------平均頭数----------"
sql = "SELECT AVG(heads_count) FROM kdb"
cursor.execute(sql)
for s in cursor.fetchall():
    print s[0]

feat = []
unit = []

feat.append("odds_order")
unit.append("人気")
feat.append("horse_age")
unit.append("才")
#feat.append("CAST(load_weight AS INT)")
#unit.append("kg")
#feat.append("CAST((horse_weight / 8) AS INT)")
#unit.append("kg")
#feat.append("CAST((dhorse_weight / 4) AS INT)")
#unit.append("kg")
#feat.append("CAST(preSpan / 7 AS INT)")
#unit.append("週")
#feat.append("CAST(preDstRt * 10 AS INT)")
#unit.append("")
#feat.append("CAST((preHeadsRt * 10) AS INT)")
#unit.append("")
#feat.append("preOOF")
#unit.append("着")
#feat.append("preRespond")
#unit.append("UP")
#feat.append("CAST((preDTimeTop3 * 2) AS INT)")
#unit.append("％")
#feat.append("CAST((preDTime3FTop3 * 2) AS INT)")
#unit.append("％")
feat.append("evaluation_by_trainer")
unit.append("")

for f, u in zip(feat, unit):
    print "--------" + f
    sql = "SELECT " + f + " as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order <= 3 then 1 else 0 end) * 100.0 as hit2, AVG(case when finish_order = 1 then odds else 0 end) * 100.0, AVG(case when finish_order <= 3 then odds_win else 0 end) * 100.0 FROM kdb where cast(finish_order as int) <> 0 group by a having c > 1000"
    cursor.execute(sql)
    for s in cursor.fetchall():
        print "{}{} {:6d}点 勝率={:5.1f}％/{:5.1f}％ 回収率={:5.1f}％/{:5.1f}％".format(s[0], u, s[1], s[2], s[3], s[4], s[5])


#print "----------preSpan"
#sql = "SELECT CAST((preSpan / 7.0) AS INT) as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a having c > 1000"
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print "{:3d}週 {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0] if s[0] else 999, s[1], s[2], s[3])
#
##print "----------preDstRt"
##sql = "SELECT CAST(preDstRt * 10 AS INT) as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a having c > 1000"
##cursor.execute(sql)
##for s in cursor.fetchall():
##    print "{} {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0], s[1], s[2], s[3])
##
#print "----------pre2HeadsRt"
#sql = "SELECT CAST((pre2HeadsRt * 10) AS INT) as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a having c > 1000"
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print "{:5.1f}％ {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0] / 10.0 if s[0] else 999, s[1], s[2], s[3])
#
#print "----------pre2OOF"
#sql = "SELECT pre2OOF as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a having c > 1000"
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print "{}着 {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0], s[1], s[2], s[3])
#
#print "----------pre2Respond"
#sql = "SELECT pre2Respond as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a having c > 1000"
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print "{:+2d}UP {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0] if s[0] else 99, s[1], s[2], s[3])
#
##print "----------pre2Eval"
##sql = "SELECT pre2Eval as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a having c > 1000"
##cursor.execute(sql)
##for s in cursor.fetchall():
##    print "{} {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0], s[1], s[2], s[3])
##
#print "----------pre2DTimeTop3"
#sql = "SELECT CAST((pre2DTimeTop3 * 2) AS INT) as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a having c > 100"
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print "{:5.1f}％ {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0] / 2.0 if s[0] else 999, s[1], s[2], s[3])
#
#print "----------pre2DTime3FTop3"
#sql = "SELECT CAST((pre2DTime3FTop3 * 2) AS INT) as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a having c > 1000"
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print "{:5.1f}％ {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0] / 2.0 if s[0] else 999, s[1], s[2], s[3])
#
#print "----------pre4AvgDstRt"
#sql = "SELECT CAST(pre4AvgDstRt * 10 AS INT) * 100 as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a having c > 500"
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print "{:5.1f}％ {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0] / 10.0 if s[0] else 999, s[1], s[2], s[3])
#
#print "----------pre4AvgPurse"
#sql = "SELECT CAST((pre4AvgPurse / 250 ) AS INT) as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a having c > 100"
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print "{:6.1f}万円 {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0] * 250.0 if s[0] else 999, s[1], s[2], s[3])
#
#print "----------pre4AvgVicRt"
#sql = "SELECT CAST((pre4AvgVicRt * 10) AS INT) * 100 as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a having c > 10"
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print "{:5.1f}％ {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0] / 10.0 if s[0] else 999, s[1], s[2], s[3])
#
#print "----------pre4AvgWinRt"
#sql = "SELECT CAST((pre4AvgWinRt * 10) AS INT) * 100 as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a having c > 10"
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print "{:5.1f}％ {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0] / 10.0 if s[0] else 999, s[1], s[2], s[3])
#
#print "----------pre4AvgRespond"
#sql = "SELECT CAST(pre4AvgRespond AS INT) as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a having c > 100"
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print "{:+2d}UP {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0] if s[0] else 99, s[1], s[2], s[3])
#
#print "----------enterTimes"
#sql = "SELECT enterTimes as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a having c > 1000"
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print "{}回 {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0], s[1], s[2], s[3])
#
##print "----------pstAvgDstRt"
##sql = "SELECT CAST(pstAvgDstRt * 10 AS INT) as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a having c > 1000"
##cursor.execute(sql)
##for s in cursor.fetchall():
##    print "{} {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0], s[1], s[2], s[3])
##
#print "----------pstAvgPurse"
#sql = "SELECT CAST((pstAvgPurse / 250 ) AS INT) as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a having c > 100"
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print "{:6.1f}万円 {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0] * 250.0 if s[0] else 999, s[1], s[2], s[3])
#
#print "----------pstAvgVicRt"
#sql = "SELECT CAST((pstAvgVicRt * 10 ) AS INT) * 100 as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a having c > 10"
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print "{:5.1f}％ {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0] / 10.0 if s[0] else 999, s[1], s[2], s[3])
#
#print "----------pstAvgWinRt"
#sql = "SELECT CAST((pstAvgWinRt * 10) AS INT) * 100 as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a having c > 10"
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print "{:5.1f}％ {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0] / 10.0 if s[0] else 999, s[1], s[2], s[3])
#
#print "----------pstAvgRespond"
#sql = "SELECT CAST(pstAvgRespond AS INT) as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a having c > 100"
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print "{:+5d}UP {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0] if s[0] else 99, s[1], s[2], s[3])
#
#print "----------pre4AvgJcyPurse"
#sql = "SELECT CAST(pre4AvgJcyPurse / 250 AS INT) as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a having c > 100"
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print "{:6.1f}万円 {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0] * 250.0 if s[0] else 999, s[1], s[2], s[3])
#
#print "----------pre4AvgJcyVic"
#sql = "SELECT CAST(pre4AvgJcyVic * 10 AS INT) * 100 as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a"
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print "{:5.1f}％ {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0] / 10.0 if s[0] else 999, s[1], s[2], s[3])
#
#print "----------pre4AvgJcyWin"
#sql = "SELECT CAST(pre4AvgJcyWin * 10 AS INT) * 100 as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a"
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print "{:5.1f}％ {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0] / 10.0 if s[0] else 999, s[1], s[2], s[3])
#
#print "----------pstAvgJcyPurse"
#sql = "SELECT CAST(pstAvgJcyPurse / 250 AS INT) as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a"
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print "{:6.1f}万円 {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0] * 250.0 if s[0] else 999, s[1], s[2], s[3])
#
#print "----------pstAvgJcyVic"
#sql = "SELECT CAST(pstAvgJcyVic * 10 AS INT) * 100 as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a"
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print "{:5.1f}％ {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0] / 10.0 if s[0] else 999, s[1], s[2], s[3])
#
#print "----------pstAvgJcyWin"
#sql = "SELECT CAST(pstAvgJcyWin * 10 AS INT) * 100 as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a"
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print "{:5.1f}％ {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0] / 10.0 if s[0] else 999, s[1], s[2], s[3])
#
#print "----------pstAvgTrnVic"
#sql = "SELECT CAST(pstAvgTrnVic * 10 AS INT) * 100 as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a"
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print "{:5.1f}％ {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0] / 10.0 if s[0] else 999, s[1], s[2], s[3])
#
#print "----------pstAvgTrnWin"
#sql = "SELECT CAST(pstAvgTrnWin * 10 AS INT) * 100 as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a"
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print "{:5.1f}％ {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0] / 10.0 if s[0] else 999, s[1], s[2], s[3])
#
##print "----------調教師コメント別----------"
##sql = " SELECT\
##            comments_by_trainer as a,\
##            count(*) as c,\
##            AVG(case when CAST(finish_order AS INT) > 1 then 0 else 1 end) * 100.0 as vicRt,\
##            AVG(case when CAST(finish_order AS INT) > 3 then 0 else 1 end) * 100.0 as winRt,\
##            AVG(case when CAST(finish_order AS INT) > 1 then 0 else odds end) * 100.0 as ret\
##        FROM kdb\
##        where\
##            cast(finish_order as unsigned) <> 0\
##            AND JULIANDAY(date) BETWEEN JULIANDAY('2013-01-01') AND JULIANDAY('2016-12-31')\
##        group by a\
##        having c > 500 AND ret > 90\
##        order by ret desc"
##cursor.execute(sql)
##for s in cursor.fetchall():
##    print "{:10s} {:6d}点 優勝率={:5.1f}％ 入賞率={:5.1f}％ 回収率={:5.1f}％".format(s[0].encode('utf-8'), s[1], s[2], s[3], s[4])
##
#print "----------騎手別回収率----------"
#sql = "SELECT jockey_name as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a having c > 1000 AND ret > 90"
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print "{} {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0].encode('utf-8'), s[1], s[2], s[3])
#
#print "----------調教師別----------"
#sql = "SELECT trainer_name as a, count(*) as c, AVG(case when finish_order = 1 then 1 else 0 end) * 100.0 as hit, AVG(case when finish_order = 1 then odds else 0 end) * 100.0 as ret FROM kdb where cast(finish_order as int) <> 0 group by a having c > 1000 AND ret > 90"
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print "{} {:6d}点 勝率={:5.1f}％ 回収率={:5.1f}％".format(s[0].encode('utf-8'), s[1], s[2], s[3])

#print "----------過去の情報----------"
#sql = "\
#    SELECT *\
#    FROM kdb K\
#    INNER JOIN(\
#        SELECT\
#            DISTINCT horse_name\
#        FROM kdb\
#        WHERE\
#            date = ? AND\
#            area_name = ? AND\
#            race_number = ? AND\
#            horse_number = ?) H\
#    ON K.horse_name = H.horse_name\
#    WHERE JULIANDAY(K.date) < JULIANDAY(?)\
#    GROUP BY H.horse_name\
#    ORDER BY JULIANDAY(K.date) DESC\
#    LIMIT 4"
#
#cursor.execute(sql, [u"2016-05-01", u"京都", 11, 17, u"2016-05-01"])
#for s in cursor.fetchall():
#    print str(s).encode('utf-8')


#print "----------過去の情報----------"
#sql = "\
#    SELECT\
#        MAX(odds), AVG(odds), median(odds), mode(odds)\
#    FROM kdb\
#    WHERE\
#        CAST(finish_order AS INT) == 1"
#
#cursor.execute(sql)
#for s in cursor.fetchall():
#    print str(s).encode('utf-8')
#
connection.close()

