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
                                        "create_time" : data[1],
                                        "zwaveid" : data[2],
                                        "deviceid": data[3],
                                        "deal_progress":data[4],
                                        "deal_user":data[5],

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
            if data.has_key("deal_progress")and data.has_key("alarmId") :
                db.update_alarm_progress(data["alarmId"],data["deal_progress"])
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
                context = ""
                eventlist = db.get_events(one[0])
                for event in eventlist:
                    context = context + event[5] + " "
                result["data"].append({"id" : one[0],
                                        "create_time" : one[1],
                                        "zwaveid": one[2],
                                        "deviceid":one[3],
                                        "deal_progress":one[4],
                                        "deal_user":one[5],
                                        "deal_user_name": db.get_username_by_id(one[5]),
                                        "deal_context": context
                                       })

            self.send_data(result)
        else:

            result["result"] = "error"
            result["message"] = "get alarm list failed"
            self.send_data(result)


class EventsHandler(BaseHandler):

    def get(self):
        log.debug("EventsHandler get in")
        try:
            alarmid = int(self.get_argument("alarmid"))
        except:
            log.debug("param alarmid is not int")
            return
        data = db.get_events(alarmid)
        result = {}
        if data:

            result["result"] = "ok"
            result["data"] = []
            for one in data:
                result["data"].append({"id": one[0],
                                        "type":one[1],
                                       "eventtime": one[4],
                                       "context": one[5]
                                       })

        else:
            result["result"] = "error"
            result["message"] = "can not find this user"

        self.send_data(result)