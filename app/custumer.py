#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import BaseHandler
from base import BASEDIR
from utils.log import log

from database import db
from utils.mysqlpasswd import mysql_password
import uuid
import json
from utils.record import save_record

from base import authenticated_self

class CustumerHandler(BaseHandler):

    @authenticated_self
    def get(self):
        log.debug("CustumerHandler get in")

        deviceid = self.get_argument("id")

        data = db.get_custumer(deviceid)
        result = {}
        if data:

            result["result"] = "ok"
            result["data"] = {"custumerid" : data[0],
                                        "custumername" : data[1],
                                        "custumertelephone" : data[2],
                                        "custumeremail" : data[3],
                                        "custumerremark": data[4],
                                        "other":json.loads(data[5]),
                                        "deviceid":data[6]
                                       }

        else:
            result["result"] = "error"
            result["message"] = "can not find this user"

        self.send_data(result)

    @authenticated_self
    def post(self):
        log.debug("CustumerHandler post in")
        data = self.get_data()
        if data:
            log.debug(data)
            if data.has_key("CustumerTelephone") and data.has_key("CustumerEmail") \
                    and data.has_key("CustumerName") and data.has_key("CustumerRemark")\
                    and data.has_key("CustumerDeviceid"):

                if data["CustumerName"] == "":
                    log.error("CustumerName is NULL")
                else:
                    db.insert_custumer(data["CustumerName"], data["CustumerTelephone"],
                                   data["CustumerEmail"],data["CustumerRemark"], data["CustumerDeviceid"])


                    result ={}
                    result["result"] = "ok"
                    self.send_data(result)
                    str = "添加用户 姓名 %s 电话 %s 邮箱 %s 备注 %s 设备id %s" % (
                        data["CustumerName"].encode('utf-8'), data["CustumerTelephone"].encode('utf-8'),\
                        data["CustumerEmail"].encode('utf-8'),data["CustumerRemark"].encode('utf-8'),\
                        data["CustumerDeviceid"].encode('utf-8'))
                    save_record(self.login_user,"custumer", 0, "add", str)

                    return

            else:
                log.error("custumer data key is not right")
        else:
            log.error("data is none")

        result = {}
        result["result"] = "error"
        result["message"] = "custumer info is error"
        self.send_data(result)

    @authenticated_self
    def put(self):
        log.debug("CustumerHandler put in")
        data = self.get_data()
        if data:
            log.debug(data)
            if data.has_key("CustumerTelephone") and data.has_key("CustumerEmail") \
                    and data.has_key("CustumerName") and data.has_key("CustumerRemark")\
                    and data.has_key("CustumerId")and data.has_key("other"):
                db.update_custumer(data["CustumerId"],data["CustumerName"], data["CustumerTelephone"],
                                   data["CustumerEmail"],data["CustumerRemark"],json.dumps(data["other"]),
                                   data["CustumerDeviceid"])
                result = {}
                result["result"] = "ok"
                self.send_data(result)
                str = "修改用户 姓名 %s 电话 %s 邮箱 %s 备注 %s 其他 %s" % (
                    data["CustumerName"].encode('utf-8'), data["CustumerTelephone"].encode('utf-8'), \
                    data["CustumerEmail"].encode('utf-8'), data["CustumerRemark"].encode('utf-8'), json.dumps(data["other"]))
                save_record(self.login_user, "custumer", data["CustumerId"], "update",str)
                return
            else:
                result = {}
                result["result"] = "error"
                result["message"] = "data is error"
                self.send_data(result)





class CustumerAllHandler(BaseHandler):
    @authenticated_self
    def get(self):
        log.debug("CustumerAllHandler get in")
        try:
            index = int(self.get_argument("index"))
        except:
            index = 1
        if index > 0:
            pass
        else:
            index = 1

        data = db.get_custumer_list(index)
        result = {}
        if data:
            result["result"] = "ok"
            result["maxindex"] = data["maxindex"]
            result["curruntindex"] = data["curruntindex"]
            result["data"] =[]
            for one in data["data"]:
                result["data"].append({"custumerid" : one[0],
                                        "custumername" : one[1],
                                        "custumertelephone" : one[2],
                                        "custumerdeviceid":one[6],
                                       })

            self.send_data(result)

        else:

            result["result"] = "error"
            result["message"] = "get custumer list failed"
            self.send_data(result)


