#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import MySQLdb
from utils.log import log
import datetime
from httpclient import HttpsClient

from utils.config import DB_USER
from utils.config import DB_PASSWORD
from utils.config import DB_NAME
from utils.config import WEBSOCKET


TIMEEXAMPLE = "%Y-%m-%d %H:%M:%S"
PERPAGENUM = 10


class DB:
    def __init__(self):
        self.log = log
#        self.connect()

    def connect(self):
        self.conn = MySQLdb.connect(host='localhost',user=DB_USER,passwd=DB_PASSWORD,db=DB_NAME,port=3306,charset="utf8")
        self.cur = self.conn.cursor()

    def execute(self, sqlcmd, ret):
        result = None
        try:
            self.connect()
            self.log.debug(sqlcmd)
            self.cur.execute(sqlcmd)
            self.conn.commit()
        except:
            self.close()
            self.connect()
            self.log.error("error connect and reconnect")
            raise

        if ret == "one":
            result = self.cur.fetchone()
        elif ret == "all":
            result =  self.cur.fetchall()

        self.close()
        return result

    def get_user_by_passwd(self, name):
        sqlcmd = '''select * from user where name = "%s" ''' % name
        result = self.execute(sqlcmd,"one")

        if result :
            return result
        else:
            return None

    def get_user_by_token(self, token):
        sqlcmd = '''select name from user where token = "%s" ''' % token

        result = self.execute(sqlcmd, "one")
        if result:
            return result[0]
        else:
            return None

    def get_username_by_id(self, id):
        sqlcmd = '''select name from user where id = "%s" ''' % id
        result = self.execute(sqlcmd, "one")

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
        sqlcmd = '''select * from user where name = "%s" ''' %  name
        result = self.execute(sqlcmd, "one")
        if result:
            return result
        else:
            return None

    def del_token(self, name):
        time = self.get_time_now()
        sqlcmd = '''update user set logouttime="%s", token=null where name="%s"''' % ( time, name)
        self.execute(sqlcmd, None)

    def set_token(self, name, token):
        time = self.get_time_now()
        sqlcmd = '''update user set token="%s", logintime="%s" where name="%s"'''%(token, time, name )
        self.execute(sqlcmd, None)

    def insert_custumer(self, CustumerName, CustumerTelephone, CustumerEmail, CustumerRemark, CustumerDeviceid):
        sqlcmd = '''insert into custumer (name, telephone, email, remark, other, deviceid) values('%s', '%s', '%s', '%s', '{}', '%s') '''%\
                 (CustumerName, CustumerTelephone, CustumerEmail, CustumerRemark,CustumerDeviceid)
        self.execute(sqlcmd, None)

    def update_custumer(self,  CustumerId, CustumerName, CustumerTelephone, CustumerEmail, CustumerRemark, other, CustumerDeviceid, \
                        CustumerPhone,CustumerState,CustumerCity,CustumerStreet,CustumerPostelCode,Monleave,Monreturn,Tueleave, \
                        Tuereturn,Wedleave,Wedreturn,Thuleave,Thureturn,Frileave,Frireturn,Satleave,Satreturn,Sunleave,Sunreturn,\
                        Holleave,Holreturn):
        sqlcmd = '''update custumer set name='%s',telephone='%s',email='%s', remark='%s', other ='%s', deviceid = '%s', \
phone = '%s',state = '%s',city = '%s',street = '%s',postelcode = '%s',monleave = '%s',monreturn = '%s',
tueleave = '%s',tuereturn = '%s',wedleave = '%s',wedreturn = '%s',thuleave = '%s',thureturn = '%s',frileave = '%s',
frireturn = '%s',satleave = '%s',satreturn = '%s',sunleave = '%s',sunreturn = '%s',holleave = '%s',holreturn = '%s'
where  id= %s '''%\
                 (CustumerName, CustumerTelephone, CustumerEmail, CustumerRemark, other, CustumerDeviceid, CustumerPhone,CustumerState,CustumerCity,CustumerStreet,CustumerPostelCode,Monleave,Monreturn,Tueleave, \
                        Tuereturn,Wedleave,Wedreturn,Thuleave,Thureturn,Frileave,Frireturn,Satleave,Satreturn,Sunleave,Sunreturn,\
                        Holleave,Holreturn,CustumerId)
        self.execute(sqlcmd, None)

    def get_custumer(self, deviceid):
        sqlcmd = '''select * from custumer where deviceid =  "%s" '''% deviceid

        result = self.execute(sqlcmd, "one")

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

        self.execute(sqlcmd, None)

    def get_alarm_unallocat(self):
        sqlcmd = '''select * from alarm where deal_progress = 0 and deal_user is NULL limit 0, 5'''

        result = self.execute(sqlcmd, "all")

        if result:
            log.debug(result)
            return result
        else:
            return None

    def get_alarm_unprogress(self, id):
        sqlcmd = '''select count(id) from alarm where deal_progress = 0 and deal_user = %d'''%id
        result = self.execute(sqlcmd, "one")

        if result:
            log.debug(result)
            return result
        else:
            return None


    def get_online_manage(self):
        
        sqlcmd = '''select * from user where token is not NULL and id != 1 '''
        result = self.execute(sqlcmd, "all")

        if result:
            log.debug(result)
            return result
        else:
            return None

    def allocat_alarm(self, id, deal_user):
        sqlcmd = '''update alarm set deal_user=%d where  id= %s ''' % \
                 (deal_user, id)
        self.execute(sqlcmd, None)

    def update_alarm_deal_user(self, id, deal_user):
        sqlcmd = '''update alarm set deal_user = %d where  id= %s ''' % \
                 (deal_user, id)

        self.execute(sqlcmd, None)

    def update_alarm_progress(self, id, deal_progress):
        sqlcmd = '''update alarm set deal_progress = %d where  id= %s and deal_progress != 2 ''' % \
                 (deal_progress, id)

        self.execute(sqlcmd, None)

    def get_alarm(self, id):
        sqlcmd = '''select * from alarm where id = %s''' % id
        result = self.execute(sqlcmd, "one")

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

        self.execute(sqlcmd, None)

    def insert_alarm_deal(self, AlarmID, AlarmManage, AlarmTelephone, AlarmRemark, AlarmAudio):
        sqlcmd = '''insert into alarm_deal (alarm_id, deal_manage, telephone, deal_time, deal_remark, audio ) values(%s, '%s','%s', '%s', '%s', '%s') ''' % \
                 (AlarmID, AlarmManage, AlarmTelephone, self.get_time_now(),  AlarmRemark, AlarmAudio)
        self.execute(sqlcmd, None)

    def get_audio_list(self, alarm_id):
        sqlcmd = '''select * from alarm_deal where alarm_id = %s''' % alarm_id

        result = self.execute(sqlcmd, "all")

        if result:
            log.debug(result)
            return result
        else:
            return None

    def get_split_page(self, index, table, sql ):
        sqlcmd = '''select count(*) from %s'''% table
        maxid = self.execute(sqlcmd, "one")[0]
        index = int(index)
        if maxid == 0:
            return None

        if ((PERPAGENUM * index) > maxid):
            limit = (maxid - 1) / PERPAGENUM
        else:
            limit = index - 1


        sqlcmd = '''select * from %s %s limit  %d,%d''' % (table, sql, limit * PERPAGENUM, PERPAGENUM)
        data = self.execute(sqlcmd, "all")
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
        result = self.execute(sqlcmd, "one")

        if result:
            log.debug(result)
            return result
        else:
            return None

    def update_manage(self, ManageId, ManageName, ManageTelephone):
        sqlcmd = '''update user set name='%s',telephone='%s' where  id= %s ''' % \
                 (ManageName, ManageTelephone, ManageId)
        self.execute(sqlcmd, None)

    def update_manage_passwd(self, ManageId, ManagePassword, ):
        sqlcmd = '''update user set passwd=password('%s') where  id= %s ''' % \
                 (ManagePassword, ManageId)
        self.execute(sqlcmd, None)

    def save_record(self, user, obj, obj_id, action, context):
        time = self.get_time_now()
        print  (user, obj, obj_id, action,context, time)
        sqlcmd = '''insert into record (user_name, object, object_id, action, context, time) values('%s', '%s', %d, '%s', '%s','%s') ''' % \
                 (user, obj, obj_id, action,context, time)

        self.execute(sqlcmd, None)

    def get_progress_alarmid_from_zaveid(self, zwaveid):
        sqlcmd = '''select id from alarm where zwaveid =%d and deal_progress != 2 ''' % zwaveid
        result = self.execute(sqlcmd, "one")
        if result:
            return result[0]
        else:
            return None

    def get_last_alarmid_from_zaveid(self, zwaveid):
        sqlcmd = '''select * from alarm where zwaveid =%d  order by id desc''' % zwaveid
        result = self.execute(sqlcmd, "one")
        if result:
            return result
        else:
            return None

    def save_event(self, id, type, deviceid, zwaveid, eventtime, objparam ):

        if type.startswith("unalarm"):
            alarm = self.get_last_alarmid_from_zaveid(zwaveid)
            if alarm == None:
                alarmid = 0
                log.error("not want unalarm %d", zwaveid)
            else:
                alarmid = alarm[0]
                if alarm[0] :
                    self.update_alarm_progress(alarmid, 2)
                    if objparam.has_key("phonenumber"):
                        self.update_alarm_deal_user(alarmid, 0)
                    HttpsClient("https://127.0.0.1:%d"%WEBSOCKET).sync_alarm(alarm[5])
                else:
                    return

        else:
            alarmid = self.get_progress_alarmid_from_zaveid(zwaveid)
            if alarmid:
                self.update_alarm_progress(alarmid,0)
            else:
                self.insert_alarm(zwaveid, deviceid)
                alarmid = self.get_progress_alarmid_from_zaveid(zwaveid)
             
        if objparam.has_key("content"):
            context = objparam["content"]
        elif objparam.has_key("phonenumber"):
            context = "Reset Phone".encode('utf-8')+objparam["phonenumber"]
        elif objparam.has_key("employeename"):
            context = "Reset ".encode('utf-8')+objparam["employeename"]
        else:
            context = ""
            
        sqlcmd = '''insert into sync_event (id, type, deviceid, zwaveid, eventtime, context, alarmid) values( %d, '%s', '%s', %d, '%s', '%s','%s') ''' % \
                 (id, type, deviceid, zwaveid, eventtime, context, alarmid)

        self.execute(sqlcmd, None)

    def get_sync_id(self):
        sqlcmd = '''select max(id) from sync_event '''

        result = self.execute(sqlcmd, "one")

        if result:
            return result[0]
        else:
            return None


    def get_record_list(self, index):
        return self.get_split_page(index, "record","order by id desc")

    def get_events(self, alarmid):
        sqlcmd = '''select * from sync_event where alarmid =%d ''' % alarmid
        result = self.execute(sqlcmd, "all")
        if result:
            return result
        else:
            return None

    def get_zwaveid_from_alarm(self, alarmid):
        sqlcmd = '''select zwaveid from alarm where id = %s ''' % alarmid
        result = self.execute(sqlcmd, "one")
        if result:
            return result[0]
        else:
            return None
    def close(self):
        self.cur.close()
        self.conn.close()

db = DB()
