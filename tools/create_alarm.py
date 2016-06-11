#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import datetime
import pytz
import time

USER = "root"
PASSWORD = "root"
DBNAME= "alarm_platform"
USERTABLE = "user"
ALARMTABLE = "alarm"
MAXSIZE = 3
TIMEEXAMPLE = "%Y-%m-%d %H:%M:%S"
PERPAGENUM = 2


class DB:
    def __init__(self):
        self.conn = MySQLdb.connect(host='localhost',user=USER,passwd=PASSWORD,db=DBNAME,port=3306,charset="utf8")
        self.cur = self.conn.cursor()
        self.user_table = USERTABLE

    def get_time_now(self):
        utc = pytz.utc
        now = datetime.datetime.now(utc)
        time = now.strftime(TIMEEXAMPLE)

        return time

    def insert_alarm(self, level, obj, content, custumer):
        sqlcmd = '''insert into alarm (alarm_level, create_time,alarm_obj, alarm_content,alarm_custumer) values(%s, '%s', '%s', '%s', %s) '''%\
                 (level, self.get_time_now(), obj, content, custumer)
        self.cur.execute(sqlcmd)
        self.conn.commit()


    def close(self):
        self.cur.close()
        self.conn.close()

if __name__ == "__main__":
    db = DB()
    for i in range(1,10):
        db.insert_alarm( i%3, "lock", "锁被打开", i%2)
        time.sleep(2)



