from base import BaseHandler
from base import BASEDIR
from base import authenticated_self
from utils.log import log

from database import db
from utils.mysqlpasswd import mysql_password
import uuid
import json
import tornado.web


class RecordAllHandler(BaseHandler):


    @authenticated_self
    def get(self):
        log.debug("RecordAllHandler get in")
        try:
            index = int(self.get_argument("index"))
        except:
            index = 1
        if index > 0:
            pass
        else:
            index = 1

        data = db.get_record_list(index)
        result = {}
        if data:
            result["result"] = "ok"
            result["maxindex"] = data["maxindex"]
            result["curruntindex"] = data["curruntindex"]
            result["data"] =[]
            for one in data["data"]:
                result["data"].append({"id" : one[0],
                                        "user_id" : one[1],
                                        "object_id" : one[3],
                                        "context": one[5],
                                        "time":one[6]
                                       })

            self.send_data(result)
        else:

            result["result"] = "error"
            result["message"] = "get alarm list failed"
            self.send_data(result)


