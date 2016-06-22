#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import BaseHandler
from base import BASEDIR
from base import authenticated_self
from utils.log import log

from database import db
from utils.mysqlpasswd import mysql_password
import uuid
import json
import tornado.web

class AlarmHandler(BaseHandler):

    def get(self):
        log.debug("AlarmHandler get in")
        try:
            id = int(self.get_argument("id"))
        except:
            log.debug("param id is not int")
            return
        data = db.get_alarm(id)
        result = {}
        if data:

            result["result"] = "ok"
            result["data"] = {"id" : data[0],
                                        "alarm_level" : data[1],
                                        "create_time" : data[2],
                                        "alarm_obj": data[3],
                                        "alarm_content":data[4],
                                        "alarm_custumer":data[5],
                                        "deal_progress":data[6],
                                        "deal_user":data[7],

                                       }

        else:
            result["result"] = "error"
            result["message"] = "can not find this user"

        self.send_data(result)

    @authenticated_self
    def put(self):
        log.debug("alarmHandler put in")
        data = self.get_data()
        if data:
            log.debug(data)
            if data.has_key("alarmTelephone") and data.has_key("alarmEmail") \
                    and data.has_key("alarmName") and data.has_key("alarmRemark")\
                    and data.has_key("alarmId")and data.has_key("other"):
                db.update_alarm(data["alarmId"],data["alarmName"], data["alarmTelephone"],
                                   data["alarmEmail"],data["alarmRemark"],json.dumps(data["other"]))
                result = {}
                result["result"] = "ok"
                self.send_data(result)

                return
            else:
                result = {}
                result["result"] = "error"
                result["message"] = "data is error"
                self.send_data(result)





class AlarmAllHandler(BaseHandler):


    @authenticated_self
    def get(self):
        log.debug("alarmAllHandler get in")
        try:
            index = int(self.get_argument("index"))
        except:
            index = 1
        if index > 0:
            pass
        else:
            index = 1

        data = db.get_alarm_list(index)
        result = {}
        if data:
            result["result"] = "ok"
            result["maxindex"] = data["maxindex"]
            result["curruntindex"] = data["curruntindex"]
            result["data"] =[]
            for one in data["data"]:
                result["data"].append({"id" : one[0],
                                        "alarm_level" : one[1],
                                        "create_time" : one[2],
                                        "alarm_obj": one[3],
                                        "alarm_content":one[4],
                                        "alarm_custumer":one[5],
                                        "deal_progress":one[6]
                                       })

            self.send_data(result)
        else:

            result["result"] = "error"
            result["message"] = "get alarm list failed"
            self.send_data(result)


