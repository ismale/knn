# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import re
import sqlite3

#SQLite
dbpath = 'kdb.db'
connection = sqlite3.connect(dbpath)
cursor = connection.cursor()

#出馬表ページ取得
def get_result_data(y, p, t, d, r):
    global connection
    global cursor
    url = "http://db.netkeiba.com"
    ref = '/race/{:4d}{:02d}{:02d}{:02d}{:02d}'.format(y, p, t, d, r)
    html = urllib2.urlopen(url + ref)
    print url + ref
    soup = BeautifulSoup(html, "html.parser")
    
    #レース情報
    t = soup.find("dl", class_="racedata fc")
    if not t:
        return None
    
    #area_name
    area_names = [u"札幌", u"函館", u"福島", u"新潟", u"東京", u"中山", u"中京", u"京都", u"阪神", u"小倉"]
    area_name = area_names[p - 1]
    
    #race_number
    race_number = r

    #run_direction
    pts = t.dd.p.text
    pts = pts.split('/')
    run_direction = pts[0].strip()[1]

    #distance
    pts[0] = pts[0]
    distance = re.search('[0-9]+', pts[0])
    distance = distance.group(0) if distance else 0

    #track
    track = re.search(u'(.+):', pts[2])
    track = track.group(1) if track else u""
    
    #track_condition
    track_condition = re.search(u':(.+)', pts[2])
    track_condition = track_condition.group(1) if track_condition else u""

    #レース情報2
    t = soup.find("div", class_="data_intro")
    pts = t.find("p", class_="smalltxt").text
    pts = pts.split(" ")
    
    #date
    date = re.search(u'([0-9]+)年([0-9]+)月([0-9]+)日', pts[0])
    yyyy = date.group(1) if date else u""
    mm = date.group(2) if date else u""
    dd = date.group(3) if date else u""
    date = "{:04d}-{:02d}-{:02d}".format(int(yyyy), int(mm), int(dd))
    
    #race_name
    race_name = pts[2]

    #馬情報
    table = soup.find("table", class_="race_table_01 nk_tb_common")
    trs = table.find_all("tr")
    
    #heads_count
    heads_count = len(trs) - 1
    for i in range(heads_count):
        tr = trs[i + 1] #ヘッダーは外す
        tds = tr.find_all("td")

        #finish_order
        finish_order = tds[0].text
#        if finish_order:
#            finish_order = re.search('[0-9]+', finish_order)
#            finish_order = int(finish_order.group(0)) if finish_order else (len(trs) - 1)
#        else:
#            finish_order = len(trs) - 1

        #post_position
        post_position = tds[1].text
        if str(post_position):
            post_position = re.search('[0-9]+', post_position)
            if post_position:
                post_position = int(post_position.group(0))

        #horse_number
        horse_number = tds[2].text
        if str(horse_number):
            horse_number = re.search('[0-9]+', horse_number)
            if horse_number:
                horse_number = int(horse_number.group(0))

        #horse_name
        horse_name = tds[3].a.text
        horse_id = tds[3].a["href"]
        if horse_id:
            horse_id = re.search('[0-9]+', horse_id).group(0)
        else:
            horse_id = 0

        #horse_age
        sex_age = tds[4].text
        horse_age = re.search('[0-9]+', sex_age).group(0)

        #horse_sex
        horse_sex = re.search('[^0-9]+', sex_age).group(0)

        #load_weight
        if str(tds[5].text):
            load_weight = float(tds[5].text)
        else:
            load_weight = 0.0

        #jockey_name
        jockey_name = tds[6].text
        jockey_id = tds[6].a["href"]
        if jockey_id:
            jockey_id = re.search('[0-9]+', jockey_id).group(0)
        else:
            jockey_id = 0

        #time
        time = tds[7].text
        if str(time):
            m = re.search('([0-9]+):', time)
            s = re.search(':([0-9]+).', time)
            ms = re.search('\.([0-9]+)', time)
            m = int(m.group(1)) if m else 0
            s = int(s.group(1)) if s else 0
            ms = int(ms.group(1)) if ms else 0
            s = 60 * m + s + (ms / 10.0)
            time = s
        else:
            time = 0

        #margin
        margin = tds[8].text

        #waypoint_order
        waypoint_order = tds[10].text

        #time3F
        time3F = tds[11].text
        if str(time3F):
            time3F = float(time3F)
        else:
            time3F = 0.0

        #odds
        odds = tds[12].text
        if odds != "---":
            odds = float(odds)
        else:
            odds = 0.0
#        odds = tds[12].text
#        if str(odds):
#            odds = re.search('[0-9]+', odds)
#            odds = float(odds.group(0)) if odds else 0
#        else:
#            odds = 0
            
        #odds_order
        odds_order = tds[13].text
        if str(odds_order):
            odds_order = re.search('[0-9]+', odds_order)
            odds_order = int(odds_order.group(0)) if odds_order else (len(trs) - 1)
        else:
            odds_order = len(trs) - 1

        #horse_weight
        #dhorse_weight        
        weight_rise = tds[14].text
        if weight_rise:
            dhorse_weight = re.search('\((.+)\)', weight_rise)
            dhorse_weight = int(dhorse_weight.group(1)) if dhorse_weight else 0
            horse_weight = re.search('(.+)\(.+', weight_rise)
            horse_weight = int(horse_weight.group(1)) if horse_weight else 0
        else:
            dhorse_weight = 0
            horse_weight = 0

        #trainer_name
        trainer_name = tds[18].a.text
        trainer_id = tds[18].a["href"]
        if trainer_id:
            trainer_id = re.search('[0-9]+', trainer_id).group(0)
        else:
            trainer_id = 0

        #purse
        purse = tds[20].text
        purse = purse.replace(u',', '')
        if str(purse):
            purse = float(purse)
        else:
            purse = 0

        #データ追加
        s = []
        s.append(date)
        s.append(area_name)
        s.append(race_number)
        s.append(race_name)
        s.append(track)
        s.append(run_direction)
        s.append(distance)
        s.append(track_condition)
        s.append(purse)
        s.append(heads_count)
        s.append(finish_order)
        s.append(post_position)
        s.append(horse_number)
        s.append(horse_name)
        s.append(horse_sex)
        s.append(horse_age)
        s.append(jockey_name)
        s.append(time)
        s.append(margin)
        s.append(waypoint_order)
        s.append(time3F)
        s.append(load_weight)
        s.append(horse_weight)
        s.append(dhorse_weight)
        s.append(odds_order)
        s.append(odds)
        s.append(trainer_name)
        s.append(horse_id)
        s.append(jockey_id)
        s.append(trainer_id)

        s = [si.strip().replace(' ', '') if type(si) is unicode else si for si in s]

        sql = "\
            SELECT\
                *\
            FROM kdb\
            WHERE\
                date = ? AND\
                area_name = ? AND\
                race_number = ? AND\
                horse_number = ?"
        cursor.execute(sql, [date, area_name, race_number, horse_number])
        if cursor.fetchone():
            sql = "\
                DELETE\
                FROM kdb\
                WHERE\
                    date = ? AND\
                    area_name = ? AND\
                    race_number = ? AND\
                    horse_number = ?"
            cursor.execute(sql, [date, area_name, race_number, horse_number])

        cursor.execute('\
            INSERT INTO kdb (\
                date,\
                area_name,\
                race_number,\
                race_name,\
                track,\
                run_direction,\
                distance,\
                track_condition,\
                purse,\
                heads_count,\
                finish_order,\
                post_position,\
                horse_number,\
                horse_name,\
                horse_sex,\
                horse_age,\
                jockey_name,\
                time,\
                margin,\
                waypoint_order,\
                time3F,\
                load_weight,\
                horse_weight,\
                dhorse_weight,\
                odds_order,\
                odds,\
                trainer_name,\
                horse_id,\
                jockey_id,\
                trainer_id)\
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', s)
        update_record(connection, cursor, date, area_name, race_number, horse_number)
    return True

#出馬表ページ取得
def get_race_data(date, y, p, t, d, r, past = False):
    global connection
    global cursor
    url = "http://race.netkeiba.com"
    ref = '/?pid=race_old&id=c{:4d}{:02d}{:02d}{:02d}{:02d}'.format(y, p, t, d, r)
    html = urllib2.urlopen(url + ref)
    print url + ref
    soup = BeautifulSoup(html, "html.parser")
    
    #レース情報
    t = soup.find("dl", class_="racedata fc")
    if not t:
        return None
    
    #area_name
    area_names = [u"札幌", u"函館", u"福島", u"新潟", u"東京", u"中山", u"中京", u"京都", u"阪神", u"小倉"]
    area_name = area_names[p - 1]
    
    #race_number
    race_number = r

    #distance
    ps = t.dd.find_all("p")
    pt = ps[0].text
    distance = re.search('[0-9]+', pt)
    distance = distance.group(0) if distance else u""

    #track_condition
    pts = ps[1].text.split("/")
    track_condition = re.search(u'：(.+)', pts[1])
    track_condition = track_condition.group(1) if track_condition else u""

    #race_name
    race_name = t.dd.h1.text

    #馬情報
    table = soup.find("table", class_="race_table_old nk_tb_common")
    trs = table.find_all("tr")
    
    #heads_count
    heads_count = len(trs) - 3
    for i in range(heads_count):
        tr = trs[i + 3] #ヘッダーは外す
        tds = tr.find_all("td")
        w = True if len(tds) > 12 else False

        #post_position
        post_position = tds[0].text
        if str(post_position):
            post_position = re.search('[0-9]+', post_position)
            if post_position:
                post_position = int(post_position.group(0))

        #horse_number
        horse_number = tds[1].text
        if str(horse_number):
            horse_number = re.search('[0-9]+', horse_number)
            if horse_number:
                horse_number = int(horse_number.group(0))

        #horse_name
        horse_name = tds[3].a.text
        horse_id = tds[3].a["href"]
        if horse_id:
            horse_id = re.search('[0-9]+', horse_id).group(0)
        else:
            horse_id = 0

        #horse_age
        sex_age = tds[4].text
        horse_age = re.search('[0-9]+', sex_age).group(0)

        #horse_sex
        horse_sex = re.search('[^0-9]+', sex_age).group(0)

        #load_weight
        if str(tds[5].text):
            load_weight = float(tds[5].text)
        else:
            load_weight = 0.0

        #jockey_name
        jockey_name = tds[6].text
        jockey_id = tds[6].a["href"]
        if jockey_id:
            jockey_id = re.search('[0-9]+', jockey_id).group(0)
        else:
            jockey_id = 0

        #horse_weight
        #dhorse_weight
        dhorse_weight = 0
        horse_weight = 0
        if w:
            weight_rise = tds[8].text
            if weight_rise:
                dhorse_weight = re.search('\((.+)\)', weight_rise)
                dhorse_weight = int(dhorse_weight.group(1)) if dhorse_weight else 0
                horse_weight = re.search('(.+)\(.+', weight_rise)
                horse_weight = int(horse_weight.group(1)) if horse_weight else 0

        #trainer_name
        trainer_name = tds[7].a.text
        trainer_id = tds[7].a["href"]
        if trainer_id:
            trainer_id = re.search('[0-9]+', trainer_id).group(0)
        else:
            trainer_id = 0

        sql = "\
            SELECT\
                *\
            FROM kdb\
            WHERE\
                date = ? AND\
                area_name = ? AND\
                race_number = ? AND\
                horse_number = ?"
        cursor.execute(sql, [date, area_name, race_number, horse_number])
        if cursor.fetchone():
            sql = "\
                DELETE\
                FROM kdb\
                WHERE\
                    date = ? AND\
                    area_name = ? AND\
                    race_number = ? AND\
                    horse_number = ?"
            cursor.execute(sql, [date, area_name, race_number, horse_number])
            
        #データ追加
        s = []
        s.append(date)
        s.append(area_name)
        s.append(race_number)
        s.append(race_name)
        s.append(distance)
        s.append(track_condition)
        s.append(heads_count)
        s.append(post_position)
        s.append(horse_number)
        s.append(horse_name)
        s.append(horse_id)
        s.append(horse_sex)
        s.append(horse_age)
        s.append(jockey_name)
        s.append(jockey_id)
        s.append(load_weight)
        s.append(horse_weight)
        s.append(dhorse_weight)
        s.append(trainer_name)
        s.append(trainer_id)

        cursor.execute('\
            INSERT INTO kdb (\
                date,\
                area_name,\
                race_number,\
                race_name,\
                distance,\
                track_condition,\
                heads_count,\
                post_position,\
                horse_number,\
                horse_name,\
                horse_id,\
                horse_sex,\
                horse_age,\
                jockey_name,\
                jockey_id,\
                load_weight,\
                horse_weight,\
                dhorse_weight,\
                trainer_name,\
                trainer_id)\
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', s)
        update_record(connection, cursor, date, area_name, race_number, horse_number)
    return True

def update_record(connection, cursor, date, area_name, race_number, horse_number):

#            print "----------前５走の情報----------"
    sql = "\
        SELECT\
            (JULIANDAY(?) - JULIANDAY(K.date)) AS preSpan,\
            (K.distance / H.distance) AS preDstRt,\
            K.track_condition AS preCond,\
            (CAST(K.heads_count AS FLOAT) / H.heads_count) AS preHeadsRt,\
            K.finish_order AS preOOF,\
            K.horse_number AS preNumber,\
            (K.load_weight / H.load_weight) AS preJWeightRt,\
            (K.horse_weight / H.horse_weight) AS preHWeightRt,\
            CAST(dhorse_weight AS INT) AS preDHWeight,\
            CASE WHEN CAST(K.finish_order AS INT) = 0 THEN 0 ELSE (K.odds_order - CAST(K.finish_order AS INT)) END AS preRespond,\
            K.evaluation_by_trainer AS preEval,\
            K.purse\
        FROM kdb K\
        INNER JOIN(\
            SELECT\
                DISTINCT horse_name,\
                horse_id,\
                jockey_name,\
                jockey_id,\
                area_name,\
                distance,\
                heads_count,\
                load_weight,\
                horse_weight\
            FROM kdb\
            WHERE\
                date = ? AND\
                area_name = ? AND\
                race_number = ? AND\
                horse_number = ?) H\
        ON K.horse_id = H.horse_id\
        WHERE JULIANDAY(K.date) < JULIANDAY(?)\
        ORDER BY JULIANDAY(K.date) DESC\
        LIMIT 5"
    cursor.execute(sql, [date, date, area_name, race_number, horse_number, date])
    for i, s in enumerate(cursor.fetchall()):
        i = str(i + 1) if i != 0 else ""
        sql = "\
            UPDATE kdb\
            SET pre{}Span = ?, pre{}DstRt = ?, pre{}Cond = ?, pre{}HeadsRt = ?, pre{}OOF = ?, pre{}Number = ?, pre{}JWeightRt = ?, pre{}HWeightRt = ?, pre{}DHWeight = ?, pre{}Respond = ?, pre{}Eval = ?, pre{}Purse = ?\
            WHERE\
                date = ? AND\
                area_name = ? AND\
                race_number = ? AND\
                horse_number = ?".format(i,i,i,i,i,i,i,i,i,i,i,i)
        s = list(s)
        s.append(date);
        s.append(area_name);
        s.append(race_number);
        s.append(horse_number);
        cursor.execute(sql, s)

#            print "----------前５走の上位３着の平均タイムとの差----------"
    for i in range(5):
        sql = "\
            SELECT\
                (1.0 - (AVG(K2.time) / H2.time)) * 100 AS preDTimeTop3,\
                (1.0 - (AVG(K2.time3F) / H2.time3F)) * 100 AS preDTime3FTop3\
            FROM kdb K2\
            INNER JOIN(\
                SELECT\
                    date,\
                    area_name,\
                    race_number,\
                    time,\
                    time3F\
                FROM kdb K\
                INNER JOIN(\
                    SELECT\
                        distinct horse_name,\
                        horse_id\
                    FROM kdb\
                    WHERE\
                        date = ? AND\
                        area_name = ? AND\
                        race_number = ? AND\
                        horse_number = ?) H\
                ON K.horse_id = H.horse_id\
                WHERE\
                    JULIANDAY(K.date) < JULIANDAY(?)\
                ORDER BY JULIANDAY(K.date) DESC\
                LIMIT 1 OFFSET {}) H2\
            ON\
                K2.date = H2.date AND\
                K2.area_name = H2.area_name AND\
                K2.race_number = H2.race_number\
            WHERE\
                CAST(K2.finish_order AS INT) > 0 AND\
                CAST(K2.finish_order AS INT) <= 3".format(i)
        cursor.execute(sql, [date, area_name, race_number, horse_number, date])
        s = cursor.fetchone()
        if s[0]:
            i = str(i + 1) if i != 0 else ""
            sql = "\
                UPDATE kdb\
                SET pre{}DTimeTop3 = ?, pre{}DTime3FTop3 = ?\
                WHERE\
                    date = ? AND\
                    area_name = ? AND\
                    race_number = ? AND\
                    horse_number = ?".format(i,i)
            cursor.execute(sql, [s[0], s[1], date, area_name, race_number, horse_number])

#            print "----------過去４レースの情報----------"
    sql = "\
        SELECT\
            ((H.distance - AVG(K.distance))/ AVG(K.distance)) AS pre4AvgDstRt,\
            AVG(K.purse) AS pre4AvgPurse,\
            AVG(CASE WHEN CAST(K.finish_order AS INT) > 1 THEN 0 ELSE 1 END) AS pre4AvgVicRt,\
            AVG(CASE WHEN CAST(K.finish_order AS INT) > 3 THEN 0 ELSE 1 END) AS pre4AvgWinRt,\
            AVG(odds_order - CAST(finish_order AS INT)) AS pre4AvgRespond\
        FROM kdb K\
        INNER JOIN(\
            SELECT\
                DISTINCT horse_name,\
                horse_id,\
                distance\
            FROM kdb\
            WHERE\
                date = ? AND\
                area_name = ? AND\
                race_number = ? AND\
                horse_number = ?) H\
        ON K.horse_id = H.horse_id\
        WHERE JULIANDAY(K.date) < JULIANDAY(?)\
        GROUP BY H.horse_id\
        ORDER BY JULIANDAY(K.date) DESC\
        LIMIT 4"
    cursor.execute(sql, [date, area_name, race_number, horse_number, date])
    s = cursor.fetchone()
    if s:
        sql = "\
            UPDATE kdb\
            SET pre4AvgDstRt = ?, pre4AvgPurse = ?, pre4AvgVicRt = ?, pre4AvgWinRt = ?, pre4AvgRespond = ?\
            WHERE\
                date = ? AND\
                area_name = ? AND\
                race_number = ? AND\
                horse_number = ?"
        s = list(s)
        s.append(date);
        s.append(area_name);
        s.append(race_number);
        s.append(horse_number);
        cursor.execute(sql, s)
    
#            print "----------過去の情報----------"
    sql = "\
        SELECT\
            COUNT(*) AS enterTimes,\
            ((H.distance - AVG(K.distance))/ AVG(K.distance)) AS pstAvgDstRt,\
            AVG(K.purse) AS pstAvgPurse,\
            AVG(CASE WHEN CAST(K.finish_order AS INT) > 1 THEN 0 ELSE 1 END) AS pstAvgVicRt,\
            AVG(CASE WHEN CAST(K.finish_order AS INT) > 3 THEN 0 ELSE 1 END) AS pstAvgWinRt,\
            AVG(odds_order - CAST(finish_order AS INT)) AS pstAvgRespond\
        FROM kdb K\
        INNER JOIN(\
            SELECT\
                DISTINCT horse_name,\
                horse_id,\
                distance\
            FROM kdb\
            WHERE\
                date = ? AND\
                area_name = ? AND\
                race_number = ? AND\
                horse_number = ?) H\
        ON K.horse_id = H.horse_id\
        WHERE JULIANDAY(K.date) < JULIANDAY(?)\
        GROUP BY H.horse_id"
    cursor.execute(sql, [date, area_name, race_number, horse_number, date])
    s = cursor.fetchone()
    if s:
        sql = "\
            UPDATE kdb\
            SET enterTimes = ?, pstAvgDstRt = ?, pstAvgPurse = ?, pstAvgVicRt = ?, pstAvgWinRt = ?, pstAvgRespond = ?\
            WHERE\
                date = ? AND\
                area_name = ? AND\
                race_number = ? AND\
                horse_number = ?"
        s = list(s)
        s.append(date);
        s.append(area_name);
        s.append(race_number);
        s.append(horse_number);
        cursor.execute(sql, s)
    
#            print "----------過去の同一開催場所情報----------"
    sql = "\
        SELECT\
            AVG(K.purse) AS pre4SameAreaAvgPurse,\
            AVG(CASE WHEN CAST(K.finish_order AS INT) > 1 THEN 0 ELSE 1 END) AS pre4SameAreaAvgVicRt,\
            AVG(CASE WHEN CAST(K.finish_order AS INT) > 3 THEN 0 ELSE 1 END) AS pre4SameAreaAvgWinRt,\
            AVG(odds_order - CAST(finish_order AS INT)) AS pre4SameAreaAvgRespond\
        FROM kdb K\
        INNER JOIN(\
            SELECT\
                DISTINCT horse_name,\
                horse_id,\
                area_name\
            FROM kdb\
            WHERE\
                date = ? AND\
                area_name = ? AND\
                race_number = ? AND\
                horse_number = ?) H\
        ON K.horse_id = H.horse_id\
        WHERE JULIANDAY(K.date) < JULIANDAY(?) AND K.area_name = K.area_name\
        GROUP BY H.horse_id\
        ORDER BY JULIANDAY(K.date) DESC\
        LIMIT 4"
    cursor.execute(sql, [date, area_name, race_number, horse_number, date])
    s = cursor.fetchone()
    if s:
        sql = "\
            UPDATE kdb\
            SET pre4SameAreaAvgPurse = ?, pre4SameAreaAvgVicRt = ?, pre4SameAreaAvgWinRt = ?, pre4SameAreaAvgRespond = ?\
            WHERE\
                date = ? AND\
                area_name = ? AND\
                race_number = ? AND\
                horse_number = ?"
        s = list(s)
        s.append(date);
        s.append(area_name);
        s.append(race_number);
        s.append(horse_number);
        cursor.execute(sql, s)

#            print "----------過去の同一距離情報----------"
    sql = "\
        SELECT\
            AVG(K.purse) AS pre4SameDstAvgPurse,\
            AVG(CASE WHEN CAST(K.finish_order AS INT) > 1 THEN 0 ELSE 1 END) AS pre4SameDstAvgVicRt,\
            AVG(CASE WHEN CAST(K.finish_order AS INT) > 3 THEN 0 ELSE 1 END) AS pre4SameDstAvgWinRt,\
            AVG(odds_order - CAST(finish_order AS INT)) AS pre4SameDstAvgRespond\
        FROM kdb K\
        INNER JOIN(\
            SELECT\
                DISTINCT horse_name,\
                horse_id,\
                distance\
            FROM kdb\
            WHERE\
                date = ? AND\
                area_name = ? AND\
                race_number = ? AND\
                horse_number = ?) H\
        ON K.horse_id = H.horse_id\
        WHERE JULIANDAY(K.date) < JULIANDAY(?) AND K.distance = H.distance\
        GROUP BY H.horse_id\
        ORDER BY JULIANDAY(K.date) DESC\
        LIMIT 4"
    cursor.execute(sql, [date, area_name, race_number, horse_number, date])
    s = cursor.fetchone()
    if s:
        sql = "\
            UPDATE kdb\
            SET pre4SameDstAvgPurse = ?, pre4SameDstAvgVicRt = ?, pre4SameDstAvgWinRt = ?, pre4SameDstAvgRespond = ?\
            WHERE\
                date = ? AND\
                area_name = ? AND\
                race_number = ? AND\
                horse_number = ?"
        s = list(s)
        s.append(date);
        s.append(area_name);
        s.append(race_number);
        s.append(horse_number);
        cursor.execute(sql, s)

#            print "----------過去の同一騎手情報----------"
    sql = "\
        SELECT\
            AVG(K.purse) AS pre4SameJcyAvgPurse,\
            AVG(CASE WHEN CAST(K.finish_order AS INT) > 1 THEN 0 ELSE 1 END) AS pre4SameJcyAvgVicRt,\
            AVG(CASE WHEN CAST(K.finish_order AS INT) > 3 THEN 0 ELSE 1 END) AS pre4SameJcyAvgWinRt,\
            AVG(odds_order - CAST(finish_order AS INT)) AS pre4SameJcyAvgRespond\
        FROM kdb K\
        INNER JOIN(\
            SELECT\
                DISTINCT horse_name,\
                horse_id,\
                jockey_name,\
                jockey_id\
            FROM kdb\
            WHERE\
                date = ? AND\
                area_name = ? AND\
                race_number = ? AND\
                horse_number = ?) H\
        ON K.horse_id = H.horse_id\
        WHERE JULIANDAY(K.date) < JULIANDAY(?) AND K.jockey_id = H.jockey_id\
        GROUP BY H.horse_id\
        ORDER BY JULIANDAY(K.date) DESC\
        LIMIT 4"
    cursor.execute(sql, [date, area_name, race_number, horse_number, date])
    s = cursor.fetchone()
    if s:
        sql = "\
            UPDATE kdb\
            SET pre4SameJcyAvgPurse = ?, pre4SameJcyAvgVicRt = ?, pre4SameJcyAvgWinRt = ?, pre4SameJcyAvgRespond = ?\
            WHERE\
                date = ? AND\
                area_name = ? AND\
                race_number = ? AND\
                horse_number = ?"
        s = list(s)
        s.append(date);
        s.append(area_name);
        s.append(race_number);
        s.append(horse_number);
        cursor.execute(sql, s)

##            print "----------調教師の情報----------"
#    sql = "\
#        SELECT\
#            AVG(CASE WHEN CAST(K.finish_order AS INT) > 3 THEN 0 ELSE 1 END) AS pstAvgTrnWin,\
#            AVG(CASE WHEN CAST(K.finish_order AS INT) > 1 THEN 0 ELSE 1 END) AS pstAvgTrnVic\
#        FROM kdb K\
#        INNER JOIN(\
#            SELECT\
#                DISTINCT trainer_name\
#            FROM kdb\
#            WHERE\
#                date = ? AND\
#                area_name = ? AND\
#                race_number = ? AND\
#                horse_number = ?) H\
#        ON K.trainer_name = H.trainer_name\
#        WHERE JULIANDAY(K.date) < JULIANDAY(?)\
#        GROUP BY H.trainer_name"
#    cursor.execute(sql, [date, area_name, race_number, horse_number, date])
#    s = cursor.fetchone()
#    if s:
#        sql = "\
#            UPDATE kdb\
#            SET pstAvgTrnWin = ?, pstAvgTrnVic = ?\
#            WHERE\
#                date = ? AND\
#                area_name = ? AND\
#                race_number = ? AND\
#                horse_number = ?"
#        s = list(s)
#        s.append(date);
#        s.append(area_name);
#        s.append(race_number);
#        s.append(horse_number);
#        cursor.execute(sql, s)

    connection.commit()
    return

if __name__ == "__main__":
#    cursor.execute("DROP TABLE IF EXISTS kdb2")
#    cursor.execute("CREATE TABLE IF NOT EXISTS kdb2(\
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
#                        preJWeightRt FLOAT,\
#                        preHWeightRt FLOAT,\
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
#                        pre2JWeightRt FLOAT,\
#                        pre2HWeightRt FLOAT,\
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
#                        pre4SameJcyAvgRespond FLOAT,\
#                        odds_win FLOAT)")
#    cursor.execute("CREATE INDEX raceIdx2 on kdb2(date, area_name, race_number)")
#    cursor.execute("CREATE INDEX horseIdx2 on kdb2(date, area_name, race_number, horse_number)")
#    cursor.execute("CREATE INDEX horseNIdx2 on kdb2(horse_name)")
#    cursor.execute("CREATE INDEX jockyNIdx2 on kdb2(jockey_name)")
#    cursor.execute("CREATE INDEX trainerNIdx2 on kdb2(trainer_name)")
#    cursor.execute("CREATE INDEX dateIdx2 on kdb2(date)")
#    connection.commit()

#    for i in range(5):
#        i = str(i + 1) if i != 0 else ""
#        cursor.execute("ALTER TABLE kdb ADD COLUMN pre{}JSpan FLOAT".format(i))
#        cursor.execute("ALTER TABLE kdb ADD COLUMN pre{}JDstRt FLOAT".format(i))
#        cursor.execute("ALTER TABLE kdb ADD COLUMN pre{}JCond TEXT".format(i))
#        cursor.execute("ALTER TABLE kdb ADD COLUMN pre{}JPurse INT".format(i))
#        cursor.execute("ALTER TABLE kdb ADD COLUMN pre{}JHeadsRt FLOAT".format(i))
#        cursor.execute("ALTER TABLE kdb ADD COLUMN pre{}JOOF INT".format(i))
#        cursor.execute("ALTER TABLE kdb ADD COLUMN pre{}JNumber INT".format(i))
#        cursor.execute("ALTER TABLE kdb ADD COLUMN pre{}JJWeightRt FLOAT".format(i))
#        cursor.execute("ALTER TABLE kdb ADD COLUMN pre{}JHWeightRt FLOAT".format(i))
#        cursor.execute("ALTER TABLE kdb ADD COLUMN pre{}JDHWeight TEXT".format(i))
#        cursor.execute("ALTER TABLE kdb ADD COLUMN pre{}JRespond INT".format(i))
#        cursor.execute("ALTER TABLE kdb ADD COLUMN pre{}JEval TEXT".format(i))
#        cursor.execute("ALTER TABLE kdb ADD COLUMN pre{}JDTimeTop3 FLOAT".format(i))
#        cursor.execute("ALTER TABLE kdb ADD COLUMN pre{}JDTime3FTop3 FLOAT".format(i))
#    connection.commit()

#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre4Span FLOAT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre4DstRt FLOAT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre4Cond TEXT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre4HeadsRt FLOAT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre4OOF INT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre4Number INT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre4JWeightRt FLOAT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre4HWeightRt FLOAT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre4DHWeight TEXT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre4Respond INT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre4Eval TEXT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre4DTimeTop3 FLOAT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre4DTime3FTop3 FLOAT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre5Span FLOAT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre5DstRt FLOAT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre5Cond TEXT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre5HeadsRt FLOAT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre5OOF INT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre5Number INT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre5JWeightRt FLOAT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre5HWeightRt FLOAT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre5DHWeight TEXT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre5Respond INT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre5Eval TEXT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre5DTimeTop3 FLOAT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre5DTime3FTop3 FLOAT")

#    cursor.execute("ALTER TABLE kdb ADD COLUMN prePurse INT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre2Purse INT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre3Purse INT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre4Purse INT")
#    cursor.execute("ALTER TABLE kdb ADD COLUMN pre5Purse INT")
#    connection.commit()
#    1:札幌,2:函館,3:福島,4:新潟,5:東京,6:中山,7:中京,8:京都,9:阪神,10:小倉
    years = [2018]
    places = [5, 8, 4, 3]
    times = range(1, 6)
    days = range(1, 13)
    races = range(1, 13)

    for y in years:
        for p in places:
            for t in times:
                for d in days:
                    for r in races:
                        if not get_result_data(y, p, t, d, r):
                            if r == 1:
                                break

    connection.close()
