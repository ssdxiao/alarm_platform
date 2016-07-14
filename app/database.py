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

    def insert_custumer(self, CustumerName, CustumerTelephone, CustumerEmail, CustumerRemark, CustumerDeviceid):
        sqlcmd = '''insert into custumer (name, telephone, email, remark, other, deviceid) values('%s', '%s', '%s', '%s', '{}', '%s') '''%\
                 (CustumerName, CustumerTelephone, CustumerEmail, CustumerRemark,CustumerDeviceid)
        log.debug(sqlcmd)
        self.cur.execute(sqlcmd)
        self.conn.commit()

    def update_custumer(self,  CustumerId, CustumerName, CustumerTelephone, CustumerEmail, CustumerRemark, other, CustumerDeviceid):
        sqlcmd = '''update custumer set name='%s',telephone='%s',email='%s', remark='%s', other ='%s', deviceid = '%s' where  id= %s '''%\
                 (CustumerName, CustumerTelephone, CustumerEmail, CustumerRemark, other, CustumerDeviceid, CustumerId)
        log.debug(sqlcmd)

        self.cur.execute(sqlcmd)
        self.conn.commit()

    def get_custumer(self, deviceid):
        sqlcmd = '''select * from custumer where deviceid =  "%s" '''% deviceid
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

    def insert_alarm(self, zwaveid, deviceid):
        sqlcmd = '''insert into alarm ( create_time,zwaveid, deviceid) values( '%s', %s, '%s') ''' % \
                 (self.get_time_now(), zwaveid, deviceid)
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
        sqlcmd = '''select count(*) from %s'''% table
        self.cur.execute(sqlcmd)
        maxid = self.cur.fetchone()[0]
        self.conn.commit()
        index = int(index)
        if maxid == 0:
            return None

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

    def get_progress_alarmid_from_zaveid(self, zwaveid):
        sqlcmd = '''select id from alarm where zwaveid =%d and deal_progress != 2 ''' % zwaveid
        self.cur.execute(sqlcmd)
        result = self.cur.fetchone()
        self.conn.commit()
        log.debug(result)
        if result:
            return result[0]
        else:
            return None

    def get_last_alarmid_from_zaveid(self, zwaveid):
        sqlcmd = '''select id from alarm where zwaveid =%d  order by id desc''' % zwaveid
        self.cur.execute(sqlcmd)
        result = self.cur.fetchone()
        self.conn.commit()
        log.debug(result)
        if result:
            return result[0]
        else:
            return None

    def save_event(self, id, type, deviceid, zwaveid, eventtime, context ):

        if type.startswith("unalarm"):
            alarmid = self.get_last_alarmid_from_zaveid(zwaveid)
            if alarmid :
                self.update_alarm_progress(alarmid, 2)
            else:
                return

        else:
            alarmid = self.get_progress_alarmid_from_zaveid(zwaveid)
            if alarmid:
                self.update_alarm_progress(alarmid,0)
            else:
                self.insert_alarm(zwaveid, deviceid)
                alarmid = self.get_progress_alarmid_from_zaveid(zwaveid)


        sqlcmd = '''insert into sync_event (id, type, deviceid, zwaveid, eventtime, context, alarmid) values( %d, '%s', '%s', %d, '%s', '%s','%s') ''' % \
                 (id, type, deviceid, zwaveid, eventtime, context, alarmid)

        log.debug(sqlcmd)

        self.cur.execute(sqlcmd)
        self.conn.commit()

    def get_sync_id(self):
        sqlcmd = '''select value from config where name = "sync_id" '''

        self.cur.execute(sqlcmd)
        result = self.cur.fetchone()
        self.conn.commit()

        log.debug(result)
        if result:
            return result[0]
        else:
            return None

    def save_sync_id(self, id):
        sqlcmd = '''update config set value= %d where   name = "sync_id" ''' % id

        log.debug(sqlcmd)

        self.cur.execute(sqlcmd)
        self.conn.commit()

    def get_record_list(self, index):
        return self.get_split_page(index, "record","order by id desc")

    def get_events(self, alarmid):
        sqlcmd = '''select * from sync_event where alarmid =%d ''' % alarmid
        self.cur.execute(sqlcmd)
        result = self.cur.fetchall()
        self.conn.commit()
        log.debug(result)
        if result:
            return result
        else:
            return None

    def close(self):
        self.cur.close()
        self.conn.close()

db = DB()
