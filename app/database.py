import MySQLdb
from utils.log import log
import datetime
import pytz

USER = "root"
PASSWORD = "root"
DBNAME= "alarm_platform"
USERTABLE = "user"
EVENTTABLE = "td_eventforthirdpart"
MAXSIZE = 3
TIMEEXAMPLE = "%Y-%m-%d %H:%M:%S"
PERPAGENUM = 2


class DB:
    def __init__(self):
        self.conn = MySQLdb.connect(host='localhost',user=USER,passwd=PASSWORD,db=DBNAME,port=3306,charset="utf8")
        self.cur = self.conn.cursor()
        self.user_table = USERTABLE
        self.event_table = EVENTTABLE
        self.log = log

    def get_user(self, name):
        self.cur.execute('''select passwd from %s where name = "%s" ''' % (self.user_table, name))
        result = self.cur.fetchone()
        self.conn.commit()
        self.log.debug(result)
        if result :
            return result[0]
        else:
            return None

    def get_time_now(self):
        utc = pytz.utc
        now = datetime.datetime.now(utc)
        time = now.strftime(TIMEEXAMPLE)

        return time

    def get_token(self, name):
        self.cur.execute('''select token from %s where name = "%s" ''' % (self.user_table, name))
        result = self.cur.fetchone()
        self.conn.commit()
        self.log.debug(result)
        if result:
            return result[0]
        else:
            return None

    def del_token(self, name):
        time = self.get_time_now()
        sqlcmd = '''update %s set logouttime="%s" where name="%s"''' % (self.user_table, time, name)
        self.cur.execute(sqlcmd)
        sqlcmd = '''update %s set token="" where name="%s"''' % (self.user_table, name)
        self.cur.execute(sqlcmd)
        self.conn.commit()

    def set_token(self, name, token):
        time = self.get_time_now()
        log.debug("name %s token %s time %s"%(name,token,time))

        sqlcmd = '''update %s set token="%s" where name="%s"'''%(self.user_table,token, name )
        log.debug(sqlcmd)
        self.cur.execute(sqlcmd)
        sqlcmd = '''update %s set logintime="%s" where name="%s"'''%(self.user_table,time, name )
        log.debug(sqlcmd)
        self.cur.execute(sqlcmd)
        self.conn.commit()

    def insert_custumer(self, CustumerName, CustumerTelephone, CustumerEmail, CustumerRemark):
        sqlcmd = '''insert into custumer (name, telephone, email, remark, other) values('%s', '%s', '%s', '%s', '{}') '''%\
                 (CustumerName, CustumerTelephone, CustumerEmail, CustumerRemark)
        log.debug(sqlcmd)
        self.cur.execute(sqlcmd)
        self.conn.commit()

    def update_custumer(self,  CustumerId, CustumerName, CustumerTelephone, CustumerEmail, CustumerRemark, other):
        sqlcmd = '''update custumer set name='%s',telephone='%s',email='%s', remark='%s', other ='%s' where  user_id= %s '''%\
                 (CustumerName, CustumerTelephone, CustumerEmail, CustumerRemark, other, CustumerId)
        log.debug(sqlcmd)

        self.cur.execute(sqlcmd)
        self.conn.commit()
    def get_custumer(self, CustumerId):
        sqlcmd = '''select * from custumer where user_id = %s'''% CustumerId
        log.debug(sqlcmd)

        self.cur.execute(sqlcmd)
        result = self.cur.fetchone()
        self.conn.commit()

        if result:
            log.debug(result)
            return result
        else:
            return None

    def get_custumer_list(self, index):
        sqlcmd = '''select max(user_id) from custumer'''
        self.cur.execute(sqlcmd)
        maxid = self.cur.fetchone()[0]
        self.conn.commit()
        index = int(index)
        if ((PERPAGENUM * index) > maxid):
            limit = maxid/PERPAGENUM
        else:
            limit = index - 1

        sqlcmd='''select * from custumer limit %d,%d'''%(limit*PERPAGENUM, PERPAGENUM)
        self.cur.execute(sqlcmd)
        data = self.cur.fetchall()
        self.conn.commit()
        self.log.debug(data)
        result = {}
        if maxid == 0:
            maxid = 1
        result["maxindex"] = (maxid-1)/PERPAGENUM+1
        result["data"] = data
        result["curruntindex"] = limit +1

        if result:
            return result
        else:
            return None



    def close(self):
        self.cur.close()
        self.conn.close()


