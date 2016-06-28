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
PERPAGENUM = 3


class DB:
    def __init__(self):
        self.conn = MySQLdb.connect(host='localhost',user=USER,passwd=PASSWORD,db=DBNAME,port=3306,charset="utf8")
        self.cur = self.conn.cursor()
        self.user_table = USERTABLE
        self.event_table = EVENTTABLE
        self.log = log

    def get_user_by_passwd(self, name):
        self.cur.execute('''select * from %s where name = "%s" ''' % (self.user_table, name))
        result = self.cur.fetchone()
        self.conn.commit()
        self.log.debug(result)
        if result :
            return result
        else:
            return None

    def get_user_by_token(self, token):
        self.cur.execute('''select id from %s where token = "%s" ''' % (self.user_table, token))
        result = self.cur.fetchone()
        self.conn.commit()
        self.log.debug(result)
        if result:
            return result[0]
        else:
            return None

    def get_time_now(self):
        #utc = pytz.utc
        now = datetime.datetime.now()
        time = now.strftime(TIMEEXAMPLE)

        return time

    def get_token(self, name):
        self.cur.execute('''select * from %s where name = "%s" ''' % (self.user_table, name))
        result = self.cur.fetchone()
        self.conn.commit()
        self.log.debug(result)
        if result:
            return result
        else:
            return None

    def del_token(self, name):
        time = self.get_time_now()
        sqlcmd = '''update %s set logouttime="%s" where name="%s"''' % (self.user_table, time, name)
        self.cur.execute(sqlcmd)
        sqlcmd = '''update %s set token=null where name="%s"''' % (self.user_table, name)
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
        sqlcmd = '''update custumer set name='%s',telephone='%s',email='%s', remark='%s', other ='%s' where  id= %s '''%\
                 (CustumerName, CustumerTelephone, CustumerEmail, CustumerRemark, other, CustumerId)
        log.debug(sqlcmd)

        self.cur.execute(sqlcmd)
        self.conn.commit()

    def get_custumer(self, custumerId):
        sqlcmd = '''select * from custumer where id = %s'''% custumerId
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
        return self.get_split_page(index, "custumer", "order by id")

    def insert_alarm(self, level, obj, content, custumer):
        sqlcmd = '''insert into alarm (alarm_level, create_time,alarm_obj, alarm_content,alarm_custumer) values(%s, '%s', '%s', '%s', %s) ''' % \
                 (level, self.get_time_now(), obj, content, custumer)
        self.cur.execute(sqlcmd)
        self.conn.commit()

    def get_alarm_unallocat(self):
        sqlcmd = '''select * from alarm where deal_progress = 0 and deal_user is NULL limit 0, 5'''
        log.debug(sqlcmd)

        self.cur.execute(sqlcmd)
        result = self.cur.fetchall()
        self.conn.commit()

        if result:
            log.debug(result)
            return result
        else:
            return None

    def get_alarm_unprogress(self):
        sqlcmd = '''select * from alarm where deal_progress = 0 and deal_user is not NULL'''
        log.debug(sqlcmd)

        self.cur.execute(sqlcmd)
        result = self.cur.fetchall()
        self.conn.commit()

        if result:
            log.debug(result)
            return result
        else:
            return None


    def get_online_manage(self):
        
        sqlcmd = '''select * from user where token is not NULL and id != 1 '''
        log.debug(sqlcmd)

        self.cur.execute(sqlcmd)
        result = self.cur.fetchall()
        self.conn.commit()

        if result:
            log.debug(result)
            return result
        else:
            return None

    def allocat_alarm(self, id, deal_user):
        sqlcmd = '''update alarm set deal_user=%d where  id= %s ''' % \
                 (deal_user, id)
        log.debug(sqlcmd)

        self.cur.execute(sqlcmd)
        self.conn.commit()

    def update_alarm_progress(self, id, deal_progress):
        sqlcmd = '''update alarm set deal_progress = %d where  id= %s ''' % \
                 (deal_progress, id)
        log.debug(sqlcmd)

        self.cur.execute(sqlcmd)
        self.conn.commit()

    def get_alarm(self, id):
        sqlcmd = '''select * from alarm where id = %s''' % id
        log.debug(sqlcmd)

        self.cur.execute(sqlcmd)
        result = self.cur.fetchone()
        self.conn.commit()

        if result:
            log.debug(result)
            return result
        else:
            return None

    def get_alarm_list(self, index):
        return self.get_split_page(index,"alarm", "order by deal_progress , id desc")


    def insert_manage(self, ManageName, ManageTelephone, ManagePassword):
        sqlcmd = '''insert into user (name, telephone, passwd ) values('%s', '%s', password('%s')) '''%\
                 (ManageName, ManageTelephone, ManagePassword)
        log.debug(sqlcmd)
        self.cur.execute(sqlcmd)
        self.conn.commit()

    def insert_alarm_deal(self, AlarmID,AlarmManage, AlarmTelephone, AlarmRemark, AlarmAudio):
        sqlcmd = '''insert into alarm_deal (alarm_id, deal_manage, telephone, deal_time, deal_remark, audio ) values(%s, %s,'%s', '%s', '%s', '%s') ''' % \
                 (AlarmID,AlarmManage, AlarmTelephone, self.get_time_now(),  AlarmRemark, AlarmAudio)
        log.debug(sqlcmd)
        self.cur.execute(sqlcmd)
        self.conn.commit()

    def get_audio_list(self, alarm_id):
        sqlcmd = '''select * from alarm_deal where alarm_id = %s''' % alarm_id
        log.debug(sqlcmd)

        self.cur.execute(sqlcmd)
        result = self.cur.fetchall()
        self.conn.commit()

        if result:
            log.debug(result)
            return result
        else:
            return None

    def get_split_page(self, index, table, sql ):
        sqlcmd = '''select max(id) from %s'''% table
        self.cur.execute(sqlcmd)
        maxid = self.cur.fetchone()[0]
        self.conn.commit()
        index = int(index)

        if ((PERPAGENUM * index) > maxid):
            limit = (maxid - 1) / PERPAGENUM
        else:
            limit = index - 1


        sqlcmd = '''select * from %s %s limit  %d,%d''' % (table, sql, limit * PERPAGENUM, PERPAGENUM)
        self.cur.execute(sqlcmd)
        data = self.cur.fetchall()
        self.conn.commit()
        self.log.debug(data)
        result = {}
        if maxid == 0:
            maxid = 1
        result["maxindex"] = (maxid - 1) / PERPAGENUM + 1
        result["data"] = data
        result["curruntindex"] = limit + 1

        if result:
            return result
        else:
            return None

    def get_manage_list(self, index):
        return self.get_split_page(index, "user", "order by id")

    def get_manage(self, ManageId):
        sqlcmd = '''select * from user where id = %s''' % ManageId
        log.debug(sqlcmd)

        self.cur.execute(sqlcmd)
        result = self.cur.fetchone()
        self.conn.commit()

        if result:
            log.debug(result)
            return result
        else:
            return None

    def update_manage(self, ManageId, ManageName, ManageTelephone):
        sqlcmd = '''update user set name='%s',telephone='%s' where  id= %s ''' % \
                 (ManageName, ManageTelephone, ManageId)
        log.debug(sqlcmd)

        self.cur.execute(sqlcmd)
        self.conn.commit()

    def update_manage_passwd(self, ManageId, ManagePassword, ):
        sqlcmd = '''update user set passwd=password('%s') where  id= %s ''' % \
                 (ManagePassword, ManageId)
        log.debug(sqlcmd)

        self.cur.execute(sqlcmd)
        self.conn.commit()

    def save_record(self,user, obj, obj_id, action, context):
        time = self.get_time_now()
        sqlcmd = '''insert into record (user_id, object, object_id, action, context, time) values(%d, '%s', %d, '%s', '%s','%s') ''' % \
                 (user, obj, obj_id, action,context, time)

        log.debug(sqlcmd)

        self.cur.execute(sqlcmd)
        self.conn.commit()

    def get_record_list(self, index):
        return self.get_split_page(index, "record","order by id desc")

    def close(self):
        self.cur.close()
        self.conn.close()

db = DB()
