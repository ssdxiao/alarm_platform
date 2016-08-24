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
            result["data"] = {"custumerid": data[0],
                              "custumername": data[1],
                              "custumertelephone": data[2],
                              "custumeremail": data[3],
                              "custumerremark": data[4],
                              "other": json.loads(data[5]),
                              "deviceid":data[6],
                              "phone": data[7],
                              "state": data[8],
                              "city": data[9],
                              "street": data[10],
                              "postelcode": data[11],
                              "monleave": data[12],
                              "monreturn": data[13],
                              "tueleave": data[14],
                              "tuereturn": data[15],
                              "wedleave": data[16],
                              "wedreturn": data[17],
                              "thuleave": data[18],
                              "thureturn": data[19],
                              "frileave": data[20],
                              "frireturn": data[21],
                              "satleave": data[22],
                              "satreturn": data[23],
                              "sunleave": data[24],
                              "sunreturn": data[25],
                              "holleave": data[26],
                              "holreturn": data[27],
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
                    and data.has_key("CustumerName") and data.has_key("CustumerRemark") \
                    and data.has_key("CustumerDeviceid"):

                if data["CustumerName"] == "" or data["CustumerDeviceid"]=="":
                    log.error("CustumerName is NULL")
                else:
                    db.insert_custumer(data["CustumerName"], data["CustumerTelephone"],
                                       data["CustumerEmail"], data["CustumerRemark"], data["CustumerDeviceid"])

                    result = {}
                    result["result"] = "ok"
                    self.send_data(result)
                    str = "添加用户 姓名 %s 电话 %s 邮箱 %s 备注 %s 设备id %s" % (
                        data["CustumerName"].encode('utf-8'), data["CustumerTelephone"].encode('utf-8'), \
                        data["CustumerEmail"].encode('utf-8'), data["CustumerRemark"].encode('utf-8'), \
                        data["CustumerDeviceid"].encode('utf-8'))
                    save_record(self.login_user, "用户", 0, "add", str)

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
                    and data.has_key("CustumerName") and data.has_key("CustumerRemark") \
                    and data.has_key("CustumerId") and data.has_key("other"):
                if data["CustumerState"] == None:
                   data["CustumerState"] = 0
                if data["CustumerCity"] == None:
                   data["CustumerCity"] = 0
                db.update_custumer(data["CustumerId"], data["CustumerName"], data["CustumerTelephone"],
                                   data["CustumerEmail"], data["CustumerRemark"], json.dumps(data["other"],ensure_ascii=False),
                                   data["CustumerDeviceid"],data["CustumerPhone"],data["CustumerState"],
                                   data["CustumerCity"], data["CustumerStreet"], data["CustumerPostelCode"],
                                   data["Monleave"], data["Monreturn"], data["Tueleave"],
                                   data["Tuereturn"], data["Wedleave"], data["Wedreturn"],
                                   data["Thuleave"], data["Thureturn"], data["Frileave"],
                                   data["Frireturn"], data["Satleave"], data["Satreturn"],
                                   data["Sunleave"], data["Sunreturn"], data["Holleave"],
                                   data["Holreturn"]
                                   )
                result = {}
                result["result"] = "ok"
                self.send_data(result)
                str = "修改用户 姓名 %s 电话 %s 邮箱 %s 备注 %s 其他 %s" % (
                    data["CustumerName"].encode('utf-8'), data["CustumerTelephone"].encode('utf-8'), \
                    data["CustumerEmail"].encode('utf-8'), data["CustumerRemark"].encode('utf-8'),
                    json.dumps(data["other"]))
                save_record(self.login_user, "用户", data["CustumerId"], "update", str)
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
            result["data"] = []
            for one in data["data"]:
                result["data"].append({"custumerid": one[0],
                                       "custumername": one[1],
                                       "custumertelephone": one[2],
                                       "custumerdeviceid": one[6],
                                       })

            self.send_data(result)

        else:

            result["result"] = "error"
            result["message"] = "get custumer list failed"
            self.send_data(result)
