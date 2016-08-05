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
import os

class AudioHandler(BaseHandler):

    @authenticated_self
    def post(self):
        log.debug("AudioHandler post in")
        data = self.get_data()
        if data:
            log.debug(data)
            if data.has_key("AlarmID") and data.has_key("AlarmRemark") \
                    and data.has_key("AlarmAudio")and data.has_key("AlarmTelephone"):
                db.insert_alarm_deal(data["AlarmID"], self.login_user, data["AlarmTelephone"],data["AlarmRemark"], "%d.wav"%data["AlarmAudio"])
                db.update_alarm_progress(data["AlarmID"],1)
                result = {}
                result["result"] = "ok"
                self.send_data(result)

                return
            else:
                result = {}
                result["result"] = "error"
                result["message"] = "data is error"
                self.send_data(result)





class AudioAllHandler(BaseHandler):


    @authenticated_self
    def get(self):
        log.debug("alarmAllHandler get in")
        try:
            alarm_id = int(self.get_argument("alarm"))
        except:
            index = 1


        data = db.get_audio_list(alarm_id)
        result = {}
        result["result"] = "ok"
        result["data"] =[]

        if data:
            for one in data:
                if os.path.exists("./static/audio/%s"%one[6]):
                    has_audio=1
                else:
                    has_audio =0
                result["data"].append({
                    "deal_user":one[2],
                    "telephone":one[3],
                    "deal_time":one[4],
                    "deal_remark":one[5],
                    "audio":one[6],
                    "has_audio":has_audio

                })

            self.send_data(result)
        else:
            self.send_data(result)


